# zettelkasten

面向个人知识库的 Codex skills 集合，用于把原始资料处理成可复用、可链接、可持续演化的 Zettelkasten 笔记。

这个仓库不再维护单一的根级 `SKILL.md`，而是把技能按目录放在根目录 `skills/` 下。每个技能负责一个明确阶段，避免把资料分析、正式成文、链接修复和结构复审混在同一次操作里。

## 目录结构

```text
skills/
  source-analysis/
  wiki-generation/
  wiki-links/
  wiki-rank/
  wiki-review/
  wiki-writes/
```

## Skills

### source-analysis

分析单个原始资料文件，并生成 `.cache/<source-id>-analysis.md` 交接文档。

它只负责提取资料结构、主要论点、候选笔记、证据、来源链接和可能的放置位置，不直接写入正式 wiki 笔记。

### wiki-generation

读取 `.cache/<source-id>-analysis.md`，生成或更新正式 wiki 笔记。

它负责永久笔记、参考笔记、论点笔记和主题笔记的写入与归档，并输出 `outputs/processing/<source-id>-report.md`。

### wiki-links

审计和修复 wiki 链接结构。

它覆盖 `argument-notes` 到 `permanent-notes` 的链接同步、`supports` / `next` 检查、坏链检测、结构层级规则检查，以及永久笔记和参考笔记的链接块清理。

### wiki-rank

对主题或领域概念做降秩分析。

它用于判断一个主题背后的最小生成因素，帮助区分相邻概念，并为主题边界、论点范围和结构调整提供依据。

### wiki-review

复审 `wiki-generation` 留下的 unresolved items，或复审主题概念、论点边界和入口笔记形态。

它把开放问题转成明确动作：更新、创建、合并、拆分、重命名、延后，或需要人工判断。

### wiki-writes

基于知识库中的结构化笔记写文章。

它优先从 `structure-notes`、`argument-notes` 和 `permanent-notes` 取材，输出到 `outputs/writes/`，用于把已经沉淀的判断组织成可读文本。

## 推荐工作流

1. 把待处理资料放入知识库的 `raw/`。
2. 使用 `source-analysis` 分析单个资料文件，生成 `.cache/<source-id>-analysis.md`。
3. 使用 `wiki-generation` 从交接文档生成或更新正式笔记。
4. 使用 `wiki-links` 审计链接结构，并在确定性问题上执行修复。
5. 遇到主题边界不清时，先用 `wiki-rank` 做概念降秩，再用 `wiki-review` 决定结构动作。
6. 需要写作时，使用 `wiki-writes` 从已有 wiki 结构中取材。

## 适用场景

- 把文章、读书摘录、会议记录、转录稿或零散想法整理成长期笔记
- 维护 Obsidian 风格的 Markdown 知识库
- 将来源资料拆解成永久笔记、参考笔记、论点笔记和主题笔记
- 审计并修复 wiki 链接结构
- 复审主题边界和论点链条
- 基于已沉淀笔记生成写作草稿

## 设计原则

- 单个资料文件逐个处理，避免批量混合导致来源和判断边界变模糊
- 先分析资料，再生成正式笔记
- 永久笔记承载可复用判断，参考笔记保留稳定命名对象的来源上下文
- 论点笔记负责组织推理链，主题笔记只作为主题入口
- 链接必须表达结构关系，不能只依赖关键词相似
- 自动修复只处理确定性链接问题，语义判断保留给人工复审或专门技能

## 使用方式

在支持 Codex 项目 skills 的环境中克隆本仓库，或把 `skills/` 复制到目标知识库根目录。

```bash
git clone https://github.com/VintLin/zettelkasten.git
```

如果要在现有 Obsidian 知识库中使用，推荐只同步 `skills/`，并让 `raw/`、`.cache/`、`wiki/`、`outputs/` 和 `archive/` 保持在知识库项目内。
