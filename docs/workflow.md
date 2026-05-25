# Workflow Design

## Goal

Create a repeatable bridge between a Zotero collection and an Obsidian-based
PDF-to-literature-note workflow.

The bridge does not replace Obsidian Zotero Integration. It complements it by
materializing the original PDFs from selected Zotero collections so external AI
and CLI workflows can process them.

## Architecture

```text
Zotero local database
        |
        v
Collection resolver
        |
        v
PDF attachment resolver
        |
        v
PDF staging folder + manifest
        |
        v
phd-deepread batch
        |
        v
Obsidian literature notes + canvases
```

## Commands

### List

Reads `collections` from `zotero.sqlite` and prints full collection paths.

```bash
python3 tools/zotero_collection_pdfs.py list
```

### Export

Finds parent Zotero items in a collection, resolves their PDF attachments, and
copies or links them to a folder.

```bash
python3 tools/zotero_collection_pdfs.py export "Collection Name" \
  --output "Research/Zotero PDF Inbox/Collection Name"
```

### Deep Read

Runs export first, then runs:

```bash
phd-deepread batch <pdf-output> -o <deepread-output> --create-canvases
```

## Data Flow

The exporter reads these Zotero SQLite tables:

- `collections`
- `collectionItems`
- `itemAttachments`
- `items`
- `itemData`
- `itemDataValues`
- `fieldsCombined`
- `itemCreators`
- `creators`
- `creatorTypes`

It never writes to Zotero.

## Filename Strategy

Output PDFs use:

```text
FirstAuthor - Year - Title [ZoteroParentKey].pdf
```

The Zotero parent key is included because:

- titles can collide,
- filenames can be truncated,
- the manifest can map each file back to Zotero,
- external tools can process readable filenames.

## Error Handling

Missing source PDFs are recorded as `missing-source` in the manifest.

Ambiguous collection names produce a list of matching collection IDs and full
paths. Users can rerun with the ID or full path.

If the Deep Read handoff exports zero PDFs, the script stops before running
`phd-deepread`.

## GitHub Packaging Path

The next natural step is to package this as a small Python CLI:

```text
zotero-deepread-bridge/
  pyproject.toml
  src/zotero_deepread_bridge/
    cli.py
    zotero.py
    export.py
    deepread.py
  tests/
  README.md
```

For now, the single-file script is easier to inspect, modify, and share.

