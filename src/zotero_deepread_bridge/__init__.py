"""Zotero Deep Read Bridge — export PDFs from Zotero collections into AI deep-reading pipelines."""

__version__ = "0.2.0"

from .cli import (
    Collection,
    PdfAttachment,
    ExportResult,
    connect_zotero,
    collection_tree,
    resolve_collection,
    list_collections,
    pdfs_for_collection,
    export_pdfs,
    main,
)
