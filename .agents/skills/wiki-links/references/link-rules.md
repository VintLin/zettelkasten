# wiki-links 规则

## 审计范围

- `[[wikilink]]` target 是否能解析到实际文件
- 是否误指向隐藏目录，例如 `archive/.cache/*`
- `structure-note -> argument-note -> permanent-note` 层级是否干净
- `supports` / `next` 是否和 argument 链一致
- permanent-note 是否 orphan
- permanent-note `References` 格式是否合规

## 修复范围

- 可确定修复的 `supports` / `next`
- 可确定清理的 `Links` 残留
- 可确定归一化的 `References`

## 不自动修复的内容

- argument 边界是否该合并
- 缺失桥接笔记
- 文献笔记或永久笔记的语义改写
- 不确定该指向哪一条现有笔记的空链接

## 执行原则

- 同一套规则，分 `audit` 和 `fix` 两种模式
- `audit` 优先，`fix` 随后
- 如果问题需要人工判断，保留为审计结果，不强行自动修
