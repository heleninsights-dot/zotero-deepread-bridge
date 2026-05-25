# Obsidian Shell Command Example

If you use an Obsidian shell-command plugin, you can create a command that runs
the bridge from inside your vault.

Example command:

```bash
cd "/Users/qingqingwang/Dropbox (Personal)/Git/Obsidian and Zotero" && \
python3 tools/zotero_collection_pdfs.py deepread "{{collection}}" \
  --pdf-output "Research/Zotero PDF Inbox/{{collection}}" \
  --deepread-output "Research/Deep Read Output/{{collection}}" \
  --create-canvases
```

Replace `{{collection}}` with however your shell-command plugin accepts prompt
input.

For a safer first run, add:

```bash
--dry-run
```

