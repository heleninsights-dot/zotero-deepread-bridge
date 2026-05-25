# Zotero Deep Read Bridge（Zotero 深度阅读桥接工具）

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![English](https://img.shields.io/badge/README-English-blue)](README.md)

**从 Zotero 合集中导出 PDF，然后运行 AI 深度阅读，生成可直接在 Obsidian 中使用的文献笔记——一条命令搞定。**

> 配套 [phd-deepread-workflow](https://github.com/heleninsights-dot/phd-deepread-workflow) 使用 — 通过 `deepread` 命令运行完整流水线：Zotero → PDF → AI 深度阅读 → Obsidian 笔记 + 画布。

## 你会得到什么

### 1. 以 Zotero 密钥命名、可追溯的 PDF

每个 PDF 文件名都以 Zotero 密钥开头——这是一个永久的、独一无二的标识符，即使你重命名条目或在合集之间移动，它也永远不会改变。在 Zotero 搜索框中输入密钥，即可瞬间定位回原始条目。

```text
[ABC123] Smith - 2023 - Functional analysis of reward circuitry.pdf
[DEF456] Chen - 2024 - 方法论研究.pdf
```

### 2. 可追溯的清单文件

每次导出都会在 PDF 旁边生成 `zotero-pdf-manifest.csv`（及 `.json`）。每一行记录了密钥、合集路径、标题和作者——用 Excel 或 Obsidian 打开，即可追溯任何文件回 Zotero。

### 3. AI 深度阅读（可选）

使用 `deepread` 而非 `export`，你还会获得结构化的 Markdown 文献笔记和 `.canvas` 批判性思维导图，可直接在 Obsidian 中打开。

以下是你的 Obsidian vault 中会新增的内容：

```text
Research/
  Zotero PDF Inbox/
    YourCollection/
      [ABC123] Smith - 2023 - Functional analysis.pdf
      [DEF456] Chen - 2024 - 方法论研究.pdf
      zotero-pdf-manifest.csv
      zotero-pdf-manifest.json
  Deep Read Output/          ← 如果运行了 deepread
    YourCollection/
      structured_literature_notes/
      YourCollection.canvas
```

没有桥接工具时，从 Zotero 拖出 PDF 只能得到随机文件名，且无法追溯来源。有了桥接工具，每个文件都命名规范、组织清晰且可追溯。

## 为什么需要这个工具

**Obsidian Zotero Integration** 插件可以将引用元数据拉入你的 vault，但不会将 PDF 文件实体化。这个桥接工具填补了这一空白：

```text
Zotero 合集  →  PDF 文件夹 + 清单  →  AI 深度阅读  →  Obsidian 笔记 + 画布
```

| 没有桥接工具 | 有桥接工具 |
|---|---|
| 逐个手动拖出 PDF | 一条命令处理整个合集 |
| 随机文件名 (`A7X93K2F.pdf`) | `[ZoteroKey] 作者 - 年份 - 短标题.pdf` |
| 无法追溯回 Zotero | 清单 CSV + 文件名中的密钥 |
| 逐篇手动处理 | 一键批量 AI 深度阅读 |

此工具与 Obsidian Zotero Integration 互补——两者可以同时使用。

## 选择你的安装方式

三种方式任选其一。选择最适合你的方式——每种方式提供的工具完全一致。

---

### 方式一：Claude Code Skill（无需终端）

**适合人群。** 已经在使用 Claude Code 配合 Obsidian 的研究者。用中文或英文描述你想做什么，Claude Code 会运行相应的命令。

**安装方法。**

```bash
mkdir -p ~/.claude/skills/zotero-deepread-bridge && \
curl -o ~/.claude/skills/zotero-deepread-bridge/SKILL.md \
  https://raw.githubusercontent.com/heleninsights-dot/zotero-deepread-bridge/main/SKILL.md
```

就这些。重启 Claude Code，技能会自动激活。

**使用方法。** 用中文或英文跟 Claude Code 说都可以：

```
Export my Zotero collection "YourCollection" and deep-read all the papers

导出我的 Zotero 收藏夹「YourCollection」并 deep-read 所有论文
```

> 已经安装了 **phd-deepread** 技能？这是它的配套工具。同时安装两者，Claude Code 会为你处理完整的流水线：Zotero → PDF → 深度阅读 → Obsidian 笔记 + 画布。

---

### 方式二：pip 安装（一条命令，全局 CLI）

**适合人群。** 习惯使用终端的研究者，希望 `zotero-deepread` 像 `git` 或 `python3` 一样随处可用。

**安装方法。**

```bash
# 需要 Python 3.10+
pip install git+https://github.com/heleninsights-dot/zotero-deepread-bridge.git
```

**使用方法。** 命令本身是英文的（和任何终端工具一样——`git`、`pip` 等），但合集名称支持包括中文在内的任何语言。

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

### 方式三：单脚本（零安装）

**适合人群。** 任何电脑上有 Python 3.10+ 的人。不需要 pip、不需要 git clone、不需要包管理器。一个文件，一条命令。

**安装方法。**

```bash
# 下载独立脚本
curl -O https://raw.githubusercontent.com/heleninsights-dot/zotero-deepread-bridge/main/tools/zotero_collection_pdfs.py
```

就这些。该脚本除了 Python 本身外零依赖。

**使用方法。** 与方式二相同——命令是英文的，合集名称支持任何语言。

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

## 快速上手（所有方式通用）

### 1. 查看你的 Zotero 合集

```bash
zotero-deepread list
```

输出示例：

```text
12345   Research/YourCollection
12346   Research/Methods
12347   Teaching/Intro-Psych
```

### 2. 执行前先预览

```bash
zotero-deepread export "YourCollection" -o "Research/Inbox/YourCollection" --dry-run
```

始终先执行 dry-run——在实际操作之前看清楚会发生什么。

### 3. 导出 PDF

```bash
zotero-deepread export "YourCollection" -o "Research/Zotero PDF Inbox/YourCollection"
```

每个文件命名如下：

```text
[ABC123] Smith - 2023 - Functional analysis of reward circuitry.pdf
```

清单文件（`zotero-pdf-manifest.csv` + `.json`）会写入 PDF 所在目录，方便你追溯每个文件到其 Zotero 条目。

### 4. 导出 + 深度阅读一步到位

```bash
zotero-deepread deepread "YourCollection" \
  --pdf-output "Research/Zotero PDF Inbox/YourCollection" \
  --deepread-output "Research/Deep Read Output/YourCollection"
```

这将导出 PDF，然后对文件夹运行 `phd-deepread batch`，生成 Markdown 文献笔记和 `.canvas` 文件，可直接在 Obsidian 中使用。

## 工作原理

该工具以**只读**模式打开你的本地 Zotero SQLite 数据库。它永远不会写入 Zotero、永远不会同步、也永远不需要 API 密钥。

```
Zotero SQLite 数据库  ──►  合集解析器  ──►  PDF 附件查找器
                                                    │
                                                    ▼
                                           PDF 暂存文件夹
                                           + CSV/JSON 清单文件
                                                    │
                                                    ▼
                                           phd-deepread batch
                                           （可选）
                                                    │
                                                    ▼
                                           Obsidian 笔记 + 画布
```

## 运行要求

- **Python 3.10+**（唯一要求——零 pip 依赖）
- **Zotero** 使用本地文件存储（默认路径为 `~/Zotero/zotero.sqlite` 和 `~/Zotero/storage/`）
- **phd-deepread**（可选，仅 `deepread` 子命令需要）

支持 macOS、Linux 和 Windows。

## 完整命令参考

### `list`

```bash
zotero-deepread list [--db ~/path/to/zotero.sqlite]
```

打印所有 Zotero 合集，格式为 `ID  Full/Path`。

### `export`

```bash
zotero-deepread export COLLECTION -o OUTPUT_DIR [options]
```

| 选项 | 默认值 | 说明 |
|---|---|---|
| `-o`, `--output` | *(必填)* | PDF 目标文件夹 |
| `--zotero-data` | `~/Zotero` | Zotero 数据目录 |
| `--linked-attachments-base` | — | 链接文件附件的基础目录 |
| `--mode` | `copy` | `copy`、`symlink` 或 `hardlink` |
| `--include-subcollections` / `--no-include-subcollections` | `--include-subcollections` | 是否包含子合集 |
| `--dry-run` | 关闭 | 预览操作而不实际修改 |

### `deepread`

```bash
zotero-deepread deepread COLLECTION --pdf-output PDF_DIR --deepread-output OUT_DIR [options]
```

包含上述所有 `export` 选项，外加：

| 选项 | 默认值 | 说明 |
|---|---|---|
| `--deepread-output` | *(必填)* | Deep Read 输出的目标目录 |
| `--phd-deepread-bin` | `phd-deepread` | phd-deepread 二进制文件路径 |
| `--create-canvases` / `--no-create-canvases` | `--create-canvases` | 是否生成 .canvas 文件 |

## 复制模式

| 模式 | 使用场景 |
|---|---|
| `copy`（默认） | 最安全。跨驱动器可用。推荐用于 Obsidian 和 AI 流水线。 |
| `symlink` | 节省磁盘空间。原始文件保留在 Zotero 存储中。 |
| `hardlink` | 在同一文件系统上节省磁盘空间。行为与真实文件一致。 |

## 与 Obsidian 配合使用

如果你使用 Obsidian 的 shell-command 插件，可以从 vault 内部触发桥接工具：

```bash
zotero-deepread deepread "{{collection}}" \
  --pdf-output "Research/Zotero PDF Inbox/{{collection}}" \
  --deepread-output "Research/Deep Read Output/{{collection}}"
```

详见 [docs/obsidian-shell-command.md](docs/obsidian-shell-command.md)。

## 建议的日常工作流

1. 在 Zotero 中收集和整理论文。
2. 当某个合集准备好进行深度阅读时，运行 `zotero-deepread export` 或 `zotero-deepread deepread`。
3. 在 Obsidian 中查看生成的 Markdown 笔记和画布。
4. 清单文件始终保存在 PDF 旁边——你可以随时将笔记追溯回 Zotero 中的原文。

## 注意事项与限制

- 导出前确保 Zotero 已完成同步。
- 脚本使用只读 SQLite 访问，通常可以在 Zotero 打开时同时运行。
- 最近写入 Zotero 的内容可能需要等数据库稳定后才能看到。
- 链接附件（Zotero 的"链接文件"功能）需要使用 `--linked-attachments-base`。
- Better BibTeX 对 Obsidian 引用工作流很有用，但本导出工具不需要它。

## 开发

```bash
git clone https://github.com/heleninsights-dot/zotero-deepread-bridge.git
cd zotero-deepread-bridge
pip install -e "."

# 从克隆仓库直接运行，无需安装
python3 -m zotero_deepread_bridge list
```

## 许可证

MIT — 详见 [LICENSE](LICENSE)。
