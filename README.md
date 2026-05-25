# Zotero Deep Read Bridge

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![中文版本](https://img.shields.io/badge/README-%E4%B8%AD%E6%96%87%E7%89%88-green)](README.zh-CN.md)

**Export PDFs from a Zotero collection, then run AI-powered deep-reading to
create Obsidian-ready literature notes — in one command.**

> Pairs with [phd-deepread-workflow](https://github.com/heleninsights-dot/phd-deepread-workflow) — use `deepread` to run the full pipeline: Zotero → PDFs → AI deep-reading → Obsidian notes + canvases.

## What You'll Get

### 1. Traceable PDFs, named by Zotero key

Each PDF filename starts with its Zotero key — a permanent, unique ID that
never changes, even if you rename the item or move it between collections.
Type the key into Zotero's search bar and you're back at the original entry.

```text
[ABC123] Smith - 2023 - Functional analysis of reward circuitry.pdf
[DEF456] Chen - 2024 - 方法论研究.pdf
```

### 2. A traceable manifest

Every export writes `zotero-pdf-manifest.csv` (and `.json`) alongside the
PDFs. Each row records the key, collection path, title, and authors — open it
in Excel or Obsidian to trace any file back to Zotero.

### 3. AI deep-reading (optional)

Run `deepread` instead of `export` and you also get structured Markdown
literature notes and `.canvas` critical-thinking maps, ready for Obsidian.

## Here's what lands in your Obsidian vault:

```text
Research/
  Zotero PDF Inbox/
    YourCollection/
      [ABC123] Smith - 2023 - Functional analysis.pdf
      [DEF456] Chen - 2024 - 方法论研究.pdf
      zotero-pdf-manifest.csv
      zotero-pdf-manifest.json
  Deep Read Output/          ← if you run deepread
    YourCollection/
      structured_literature_notes/
      YourCollection.canvas
```

Without the bridge, dragging PDFs out of Zotero gives you files with random
names and no connection back. With the bridge, every file is named, organized,
and traceable.

## Why This Exists

**Obsidian Zotero Integration** pulls citation metadata into your vault but
doesn't materialize PDF files. The bridge fills that gap:

```text
Zotero collection  →  PDF folder + manifest  →  AI deep-reading  →  Obsidian notes + canvases
```

| Without the bridge | With the bridge |
|---|---|
| Drag PDFs out one by one | One command for the whole collection |
| Random filenames (`A7X93K2F.pdf`) | `[ZoteroKey] Author - Year - ShortTitle.pdf` |
| No link back to Zotero | Manifest CSV + key in filename |
| Manual per-paper processing | Batch AI deep-reading in one step |

This tool complements Obsidian Zotero Integration — use both.

## Choose Your Installation

Three ways to get started. Pick the one that fits your comfort level — each
gives you the exact same tool.

---

### Tier 1: Claude Code Skill (no terminal needed)

**Who it's for.** Researchers who already use Claude Code alongside Obsidian.
You describe what you want in plain language — Chinese or English — and Claude
Code runs the right commands.

**How to install.**

```bash
mkdir -p ~/.claude/skills/zotero-deepread-bridge && \
curl -o ~/.claude/skills/zotero-deepread-bridge/SKILL.md \
  https://raw.githubusercontent.com/heleninsights-dot/zotero-deepread-bridge/main/SKILL.md
```

That's it. Restart Claude Code and the skill activates automatically.

**How to use.** Talk to Claude Code in English or Chinese — both work. 用中文或英文跟 Claude Code 说都可以：

```
Export my Zotero collection "YourCollection" and deep-read all the papers

导出我的 Zotero 收藏夹「YourCollection」并 deep-read 所有论文
```

> Already have the **phd-deepread** skill? This is its companion. Install both
> and Claude Code handles the full pipeline: Zotero → PDFs → deep-read →
> Obsidian notes + canvases.

---

### Tier 2: pip install (one command, global CLI)

**Who it's for.** Researchers comfortable with the terminal who want
`zotero-deepread` available everywhere — like `git` or `python3`.

**How to install.**

```bash
# Requires Python 3.10+
pip install git+https://github.com/heleninsights-dot/zotero-deepread-bridge.git
```

**How to use.** Commands are in English (like any terminal tool — `git`, `pip`,
etc.), but collection names work in any language including Chinese.

```bash
zotero-deepread list
zotero-deepread export "YourCollection" -o "Research/Zotero PDF Inbox/YourCollection"
zotero-deepread deepread "YourCollection" \
  --pdf-output "Research/Zotero PDF Inbox/YourCollection" \
  --deepread-output "Research/Deep Read Output/YourCollection"
```

```bash
zotero-deepread list
zotero-deepread export "你的收藏夹" -o "研究/Zotero PDF 收件箱/你的收藏夹"
zotero-deepread deepread "你的收藏夹" \
  --pdf-output "研究/Zotero PDF 收件箱/你的收藏夹" \
  --deepread-output "研究/Deep Read 输出/你的收藏夹"
```
---

### Tier 3: Single script (zero install)

**Who it's for.** Anyone with Python 3.10+ on their machine. No pip, no git
clone, no package manager. One file, one command.

**How to install.**

```bash
# Download the standalone script
curl -O https://raw.githubusercontent.com/heleninsights-dot/zotero-deepread-bridge/main/tools/zotero_collection_pdfs.py
```

That's it. The script has zero dependencies beyond Python itself.


**How to use.** Same as Tier 2 — commands are English, collection names work in
any language.

```bash
python3 zotero_collection_pdfs.py list
python3 zotero_collection_pdfs.py export "YourCollection" -o "Research/Zotero PDF Inbox/YourCollection"
python3 zotero_collection_pdfs.py deepread "YourCollection" \
  --pdf-output "Research/Zotero PDF Inbox/YourCollection" \
  --deepread-output "Research/Deep Read Output/YourCollection"
```

```bash
python3 zotero_collection_pdfs.py list
python3 zotero_collection_pdfs.py export "你的收藏夹" -o "研究/Zotero PDF 收件箱/你的收藏夹"
python3 zotero_collection_pdfs.py deepread "你的收藏夹" \
  --pdf-output "研究/Zotero PDF 收件箱/你的收藏夹" \
  --deepread-output "研究/Deep Read 输出/你的收藏夹"
```

---

## Quick Usage (all tiers)

### 1. See your Zotero collections

```bash
zotero-deepread list
```

Output:

```text
12345   Research/YourCollection
12346   Research/Methods
12347   Teaching/Intro-Psych
```

### 2. Preview before committing

```bash
zotero-deepread export "YourCollection" -o "Research/Inbox/YourCollection" --dry-run
```

Always dry-run first — see what will happen before it happens.

### 3. Export PDFs

```bash
zotero-deepread export "YourCollection" -o "Research/Zotero PDF Inbox/YourCollection"
```

Each file is named like:

```text
[ABC123] Smith - 2023 - Functional analysis of reward circuitry.pdf
```

A manifest (`zotero-pdf-manifest.csv` + `.json`) is written alongside the PDFs
so you can trace every file back to its Zotero item.

### 4. Export and deep-read in one step

```bash
zotero-deepread deepread "YourCollection" \
  --pdf-output "Research/Zotero PDF Inbox/YourCollection" \
  --deepread-output "Research/Deep Read Output/YourCollection"
```

This exports the PDFs and then runs `phd-deepread batch` on the folder,
producing Markdown literature notes and `.canvas` files ready for Obsidian.

## How It Works

The tool opens your local Zotero SQLite database in **read-only** mode. It
never writes to Zotero, never syncs, and never requires an API key.

```
Zotero SQLite DB  ──►  Collection resolver  ──►  PDF attachment finder
                                                        │
                                                        ▼
                                               PDF staging folder
                                               + CSV/JSON manifest
                                                        │
                                                        ▼
                                               phd-deepread batch
                                               (optional)
                                                        │
                                                        ▼
                                               Obsidian notes + canvases
```

## Requirements

- **Python 3.10+** (the only requirement — zero pip dependencies)
- **Zotero** with local file storage (the default paths are `~/Zotero/zotero.sqlite`
  and `~/Zotero/storage/`)
- **phd-deepread** (optional, only needed for the `deepread` subcommand)

Works on macOS, Linux, and Windows.

## Full Command Reference

### `list`

```bash
zotero-deepread list [--db ~/path/to/zotero.sqlite]
```

Prints every Zotero collection as `ID  Full/Path`.

### `export`

```bash
zotero-deepread export COLLECTION -o OUTPUT_DIR [options]
```

| Option | Default | Description |
|---|---|---|
| `-o`, `--output` | *(required)* | Destination folder for PDFs |
| `--zotero-data` | `~/Zotero` | Zotero data directory |
| `--linked-attachments-base` | — | Base directory for linked-file attachments |
| `--mode` | `copy` | `copy`, `symlink`, or `hardlink` |
| `--include-subcollections` / `--no-include-subcollections` | `--include-subcollections` | Whether to include child collections |
| `--dry-run` | off | Preview without making changes |

### `deepread`

```bash
zotero-deepread deepread COLLECTION --pdf-output PDF_DIR --deepread-output OUT_DIR [options]
```

All `export` options above, plus:

| Option | Default | Description |
|---|---|---|
| `--deepread-output` | *(required)* | Destination for Deep Read output |
| `--phd-deepread-bin` | `phd-deepread` | Path to the phd-deepread binary |
| `--create-canvases` / `--no-create-canvases` | `--create-canvases` | Generate .canvas files |

## Copy Modes

| Mode | When to use |
|---|---|
| `copy` (default) | Safest. Works across drives. Use for Obsidian and AI pipelines. |
| `symlink` | Save disk space. Original stays in Zotero storage. |
| `hardlink` | Save disk space on the same filesystem. Behaves like a real file. |

## Pairing with Obsidian

If you use an Obsidian shell-command plugin, you can trigger the bridge from
inside your vault:

```bash
zotero-deepread deepread "{{collection}}" \
  --pdf-output "Research/Zotero PDF Inbox/{{collection}}" \
  --deepread-output "Research/Deep Read Output/{{collection}}"
```

See [docs/obsidian-shell-command.md](docs/obsidian-shell-command.md) for details.

## Suggested Daily Workflow

1. Collect and organize papers in Zotero.
2. When a collection is ready for deeper reading, run `zotero-deepread export`
   or `zotero-deepread deepread`.
3. Review the generated Markdown notes and canvases in Obsidian.
4. The manifest stays beside the PDFs — you can always trace a note back to
   its source in Zotero.

## Notes and Limitations

- Let Zotero finish syncing before exporting.
- The script uses read-only SQLite access and can usually run while Zotero is
  open.
- Very recent Zotero writes may not appear until the database settles.
- Linked attachments (Zotero's "linked file" feature) need
  `--linked-attachments-base`.
- Better BibTeX is useful for your Obsidian citation workflow, but this
  exporter does not require it.

## Development

```bash
git clone https://github.com/heleninsights-dot/zotero-deepread-bridge.git
cd zotero-deepread-bridge
pip install -e "."

# Run from the clone without installing
python3 -m zotero_deepread_bridge list
```

## License

MIT — see [LICENSE](LICENSE).
