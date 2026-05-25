"""Export PDF attachments from a Zotero collection into a normal folder.

Zero-dependency bridge from Zotero to AI deep-reading workflows. Read-only
access to the local Zotero SQLite database — never writes, never syncs.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import sqlite3
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_DB = Path("~/Zotero/zotero.sqlite").expanduser()
DEFAULT_ZOTERO_DATA = Path("~/Zotero").expanduser()


@dataclass(frozen=True)
class Collection:
    collection_id: int
    name: str
    parent_id: int | None
    path: str


@dataclass(frozen=True)
class PdfAttachment:
    parent_item_id: int
    parent_key: str
    attachment_item_id: int
    attachment_key: str
    attachment_path: str
    title: str
    date: str
    first_author: str


@dataclass(frozen=True)
class ExportResult:
    collection: Collection
    output: Path
    pdfs_found: int
    exported: int
    missing: int
    manifest_csv: Path
    manifest_json: Path


def connect_zotero(db_path: Path) -> sqlite3.Connection:
    uri = f"file:{db_path}?mode=ro&immutable=1"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def slugify(value: str, max_len: int = 140) -> str:
    value = re.sub(r"[\\/:*?\"<>|]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    value = value.strip(". ")
    if len(value) > max_len:
        value = value[:max_len].rstrip()
    return value or "untitled"


def year_from_date(value: str) -> str:
    match = re.search(r"(18|19|20)\d{2}", value or "")
    return match.group(0) if match else "n.d"


def collection_tree(conn: sqlite3.Connection) -> list[Collection]:
    rows = conn.execute(
        "select collectionID, collectionName, parentCollectionID from collections"
    ).fetchall()
    by_parent: dict[int | None, list[sqlite3.Row]] = {}
    for row in rows:
        by_parent.setdefault(row["parentCollectionID"], []).append(row)

    collections: list[Collection] = []

    def visit(parent_id: int | None, prefix: str) -> None:
        for row in sorted(
            by_parent.get(parent_id, []), key=lambda r: r["collectionName"].lower()
        ):
            name = row["collectionName"]
            path = f"{prefix}/{name}" if prefix else name
            collections.append(Collection(row["collectionID"], name, parent_id, path))
            visit(row["collectionID"], path)

    visit(None, "")
    return collections


def resolve_collection(conn: sqlite3.Connection, value: str) -> Collection:
    collections = collection_tree(conn)
    if value.isdigit():
        matches = [c for c in collections if c.collection_id == int(value)]
    elif "/" in value:
        matches = [c for c in collections if c.path == value]
    else:
        matches = [c for c in collections if c.name == value]

    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise SystemExit(
            f"No collection matched {value!r}. Run the list command first."
        )

    choices = "\n".join(f"  {c.collection_id}: {c.path}" for c in matches)
    raise SystemExit(
        f"Collection name {value!r} is ambiguous. Use an ID or full path:\n{choices}"
    )


def list_collections(conn: sqlite3.Connection) -> None:
    for collection in collection_tree(conn):
        print(f"{collection.collection_id}\t{collection.path}")


def pdfs_for_collection(
    conn: sqlite3.Connection, collection_id: int, include_subcollections: bool
) -> list[PdfAttachment]:
    if include_subcollections:
        collection_cte = """
        with recursive selected(collectionID) as (
          select collectionID from collections where collectionID = :collection_id
          union all
          select c.collectionID
          from collections c
          join selected s on c.parentCollectionID = s.collectionID
        ),
        """
    else:
        collection_cte = """
        with selected(collectionID) as (
          select collectionID from collections where collectionID = :collection_id
        ),
        """

    query = (
        collection_cte
        + """
    selected_items as (
      select distinct itemID from collectionItems
      where collectionID in (select collectionID from selected)
    ),
    parent_items as (
      select itemID from selected_items
      union
      select ia.parentItemID
      from itemAttachments ia
      join selected_items si on si.itemID = ia.itemID
      where ia.parentItemID is not null
    ),
    metadata as (
      select
        d.itemID,
        max(case when f.fieldName = 'title' then v.value end) as title,
        max(case when f.fieldName = 'date' then v.value end) as date
      from itemData d
      join fieldsCombined f on f.fieldID = d.fieldID
      join itemDataValues v on v.valueID = d.valueID
      where f.fieldName in ('title', 'date')
      group by d.itemID
    ),
    ranked_creators as (
      select
        ic.itemID,
        coalesce(nullif(c.lastName, ''), c.firstName, '') as first_author,
        row_number() over (
          partition by ic.itemID
          order by case when ct.creatorType = 'author' then 0 else 1 end, ic.orderIndex
        ) as creator_rank
      from itemCreators ic
      join creators c on c.creatorID = ic.creatorID
      join creatorTypes ct on ct.creatorTypeID = ic.creatorTypeID
    ),
    first_creators as (
      select itemID, first_author
      from ranked_creators
      where creator_rank = 1
    )
    select distinct
      pi.itemID as parent_item_id,
      pi.key as parent_key,
      ai.itemID as attachment_item_id,
      ai.key as attachment_key,
      ia.path as attachment_path,
      coalesce(m.title, '') as title,
      coalesce(m.date, '') as date,
      coalesce(fc.first_author, '') as first_author
    from parent_items p
    join itemAttachments ia on ia.parentItemID = p.itemID or ia.itemID = p.itemID
    join items ai on ai.itemID = ia.itemID
    left join items pi on pi.itemID = coalesce(ia.parentItemID, ia.itemID)
    left join metadata m on m.itemID = pi.itemID
    left join first_creators fc on fc.itemID = pi.itemID
    where ia.contentType = 'application/pdf'
    order by lower(first_author), date, lower(title), attachment_key
    """
    )

    rows = conn.execute(query, {"collection_id": collection_id}).fetchall()
    return [
        PdfAttachment(
            parent_item_id=row["parent_item_id"],
            parent_key=row["parent_key"],
            attachment_item_id=row["attachment_item_id"],
            attachment_key=row["attachment_key"],
            attachment_path=row["attachment_path"],
            title=row["title"],
            date=row["date"],
            first_author=row["first_author"],
        )
        for row in rows
    ]


def resolve_attachment_path(
    attachment: PdfAttachment,
    zotero_data: Path,
    linked_attachments_base: Path | None,
) -> Path:
    raw_path = attachment.attachment_path
    if raw_path.startswith("storage:"):
        filename = raw_path.removeprefix("storage:")
        return zotero_data / "storage" / attachment.attachment_key / filename
    if raw_path.startswith("attachments:"):
        if not linked_attachments_base:
            raise FileNotFoundError(
                f"{raw_path} uses Zotero's linked attachment base directory; pass "
                "--linked-attachments-base."
            )
        return linked_attachments_base / raw_path.removeprefix("attachments:")
    return Path(raw_path).expanduser()


def output_name(attachment: PdfAttachment, seen: set[str]) -> str:
    author = slugify(attachment.first_author or "Unknown", 40)
    year = year_from_date(attachment.date)
    title = slugify(attachment.title or attachment.parent_key, 95)
    base = f"{author} - {year} - {title} [{attachment.parent_key}]"
    name = f"{base}.pdf"
    counter = 2
    while name in seen:
        name = f"{base} ({counter}).pdf"
        counter += 1
    seen.add(name)
    return name


def copy_or_link(src: Path, dst: Path, mode: str) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        return
    if mode == "copy":
        shutil.copy2(src, dst)
    elif mode == "symlink":
        dst.symlink_to(src)
    elif mode == "hardlink":
        dst.hardlink_to(src)
    else:
        raise ValueError(f"Unknown export mode: {mode}")


def write_manifest(output: Path, rows: list[dict[str, str]]) -> None:
    json_path = output / "zotero-pdf-manifest.json"
    csv_path = output / "zotero-pdf-manifest.csv"
    json_path.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=list(rows[0].keys()) if rows else ["message"]
        )
        writer.writeheader()
        if rows:
            writer.writerows(rows)
        else:
            writer.writerow({"message": "No PDFs found"})


def export_pdfs(
    db: Path,
    collection_value: str,
    output: Path,
    zotero_data: Path,
    linked_attachments_base: Path | None,
    mode: str,
    include_subcollections: bool,
    dry_run: bool,
) -> ExportResult:
    conn = connect_zotero(db)
    collection = resolve_collection(conn, collection_value)
    attachments = pdfs_for_collection(
        conn, collection.collection_id, include_subcollections
    )
    output = output.expanduser()
    output.mkdir(parents=True, exist_ok=True)

    seen_names: set[str] = set()
    manifest: list[dict[str, str]] = []
    missing = 0
    exported = 0

    for attachment in attachments:
        try:
            source = resolve_attachment_path(
                attachment, zotero_data.expanduser(), linked_attachments_base
            )
        except FileNotFoundError as exc:
            source = Path(str(exc))

        dest_name = output_name(attachment, seen_names)
        dest = output / dest_name
        status = "dry-run"

        if not source.exists():
            status = "missing-source"
            missing += 1
        elif not dry_run:
            copy_or_link(source, dest, mode)
            status = "exported" if dest.exists() else "failed"
            exported += int(status == "exported")

        manifest.append(
            {
                "status": status,
                "collection": collection.path,
                "output_file": str(dest),
                "source_file": str(source),
                "zotero_parent_key": attachment.parent_key,
                "zotero_attachment_key": attachment.attachment_key,
                "title": attachment.title,
                "first_author": attachment.first_author,
                "date": attachment.date,
            }
        )

    manifest_csv = output / "zotero-pdf-manifest.csv"
    manifest_json = output / "zotero-pdf-manifest.json"
    if not dry_run:
        write_manifest(output, manifest)

    return ExportResult(
        collection=collection,
        output=output,
        pdfs_found=len(attachments),
        exported=exported,
        missing=missing,
        manifest_csv=manifest_csv,
        manifest_json=manifest_json,
    )


def print_export_result(result: ExportResult, dry_run: bool) -> None:
    print(f"Collection: {result.collection.path} ({result.collection.collection_id})")
    print(f"PDFs found: {result.pdfs_found}")
    if dry_run:
        print(f"Dry run output folder: {result.output}")
    else:
        print(f"Exported: {result.exported}")
        print(f"Missing sources: {result.missing}")
        print(f"Manifest: {result.manifest_csv}")


def export_collection(args: argparse.Namespace) -> None:
    result = export_pdfs(
        db=args.db,
        collection_value=args.collection,
        output=args.output,
        zotero_data=args.zotero_data,
        linked_attachments_base=args.linked_attachments_base,
        mode=args.mode,
        include_subcollections=args.include_subcollections,
        dry_run=args.dry_run,
    )
    print_export_result(result, args.dry_run)


def deepread_collection(args: argparse.Namespace) -> None:
    result = export_pdfs(
        db=args.db,
        collection_value=args.collection,
        output=args.pdf_output,
        zotero_data=args.zotero_data,
        linked_attachments_base=args.linked_attachments_base,
        mode=args.mode,
        include_subcollections=args.include_subcollections,
        dry_run=args.dry_run,
    )
    print_export_result(result, args.dry_run)

    command = [
        args.phd_deepread_bin,
        "batch",
        str(result.output),
        "-o",
        str(args.deepread_output.expanduser()),
    ]
    if args.create_canvases:
        command.append("--create-canvases")

    if args.dry_run:
        print("Deep Read command:")
        print(" ".join(command))
        return

    if result.exported == 0:
        raise SystemExit("No PDFs were exported, so Deep Read was not run.")

    subprocess.run(command, check=True)


def add_export_arguments(
    parser: argparse.ArgumentParser, output_arg: str = "--output"
) -> None:
    parser.add_argument(
        "collection", help="Collection ID, exact name, or full path"
    )
    parser.add_argument(
        "-o", output_arg, type=Path, required=True, help="Destination PDF folder"
    )
    parser.add_argument(
        "--zotero-data",
        type=Path,
        default=DEFAULT_ZOTERO_DATA,
        help="Zotero data directory",
    )
    parser.add_argument(
        "--linked-attachments-base",
        type=Path,
        help="Base directory for Zotero linked attachments using attachments: paths",
    )
    parser.add_argument(
        "--mode",
        choices=["copy", "symlink", "hardlink"],
        default="copy",
        help="How to materialize PDFs in the output folder",
    )
    parser.add_argument(
        "--include-subcollections",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Include PDFs from child collections",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be exported"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="List Zotero collections, export PDFs, or hand them to PhD Deep Read."
    )
    parser.add_argument(
        "--db", type=Path, default=DEFAULT_DB, help="Path to zotero.sqlite"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List Zotero collection IDs and paths")

    export = subparsers.add_parser(
        "export", help="Export PDFs from one Zotero collection"
    )
    add_export_arguments(export, "--output")
    export.set_defaults(func=export_collection)

    deepread = subparsers.add_parser(
        "deepread",
        help="Export PDFs and run phd-deepread batch on the export folder",
    )
    add_export_arguments(deepread, "--pdf-output")
    deepread.add_argument(
        "--deepread-output",
        type=Path,
        required=True,
        help="Destination for Deep Read output",
    )
    deepread.add_argument(
        "--phd-deepread-bin",
        default="phd-deepread",
        help="Path or command name for phd-deepread",
    )
    deepread.add_argument(
        "--create-canvases",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Pass --create-canvases to phd-deepread batch",
    )
    deepread.set_defaults(func=deepread_collection)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "list":
        conn = connect_zotero(args.db)
        list_collections(conn)
        return 0
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
