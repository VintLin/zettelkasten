# source-analysis 输出模板

按下面的结构写 `.cache/<source-id>-analysis.md`。

## 命名规则

- `source-id` = 原始 source 文件名去掉扩展名后的结果
- 保留原文件名中的中文、英文、数字和常规连接符
- 不额外翻译标题
- 例子：
  - `raw/AI/20260413-测试材料.md` -> `.cache/20260413-测试材料-analysis.md`
  - `raw/paper/foo-bar.pdf` -> `.cache/foo-bar-analysis.md`

```md
---
id: <source-id>-analysis
type: source-analysis
source_path: raw/...
created: YYYY-MM-DD
---

# <source title> 分析

## Source identity

- Source path:
- File name:
- Folder context:
- Source language:
- Source type:

## Source summary

- 3-8 条，说明 source 在讲什么、重要性在哪里

## Source map

- Thesis:
- Argument skeleton:
- Core sections:
- Support sections:
- Ignored or de-weighted sections:
- Reopening cues:

## Key concepts

- 概念名
  - 定义：
  - 在本文中的作用：
  - 可能关联的现有笔记：

## Key claims

- 主张：
  - 证据：
  - 强度判断：
  - 备注：

## Named items needing reference-notes

- 名称：
  - 是什么：
  - 为什么应建立或更新 `wiki/reference-notes/`：
  - 关联的 permanent note 候选：

## Candidate permanent notes

- 标题建议：
  - 原始笔记单元：
  - 核心内容：
  - 现有笔记检查：new | update | split | merge-candidate
  - 涉及的现有 permanent note：
  - 判断理由：
  - 应保留的来源链接：
  - 应保留的图片：
  - 相关 argument 候选：
  - 若都不合适，是否可能需要新 argument：

## Candidate argument targets

- `[[argument-note-id|标题]]`
  - 关系：strengthens | extends | challenges | answers
  - 原因：

## Key tensions

- 张力：
  - 为什么重要：
  - 对生成的影响：

## Contradictions with existing notes

- 冲突或张力：
  - 涉及的现有笔记：
  - 处理建议：

## Open questions

- 尚未能稳定判断的问题

## Recommended generation scope

- Create:
- Update:
- Defer:

## Preserved source links

- [标题](https://...)

## Preserved source images

![[image-1.png]]
![[image-2.jpg]]
```

## 额外要求

- `Source summary`、`Key claims`、`Candidate permanent notes` 不能留空；没有内容时写 `- 无`
- `Source map` 不能留空；若 source 很短，也至少写出 `Thesis` 和 `Core sections`
- `Argument skeleton` 只有在能显著帮助下游理解论证推进时才写；否则写 `- 无`
- `Preserved source links` 和 `Preserved source images` 只收真正有助于后续笔记生成的内容
- 图片名必须与项目内可被 Obsidian 识别的文件同名
- `Candidate argument targets` 只写“相关性判断”，不写最终插入位置
- 不单独输出 `Candidate structure targets`；结构挂接由 `wiki-generation` 根据最终 argument 结果决定
- `Candidate permanent notes` 必须显式判断现有笔记是否能承接；若只是同一论点的新证据、例子、限制、反例、来源或更好表述，优先标为 `update`，不要默认标为 `new`
- 只有当候选内容承担新的判断、方法、区分、问题或 argument 位置时，才标为 `new`
- 若判断可能需要新 argument，标题建议默认写成更短、更上位的母问题，不预先把限定条件、结论方向或方法细分写进标题
- 若判断可能需要新 argument，标题建议必须优先写成读者会自然提出的人话问题，不写分析腔、机制腔或解释句式标题
- 默认优先更直接的题法，例如 `如何提升编程能力？`、`如何沉淀经验？`、`创作如何发生？`，不要先写成 `如何…真正长出来`、`如何…稳定沉淀`、`如何…并被约束`
- `Source summary`、`Key claims`、`Candidate permanent notes` 的文字必须直接进入事实、判断或候选内容，不先解释“这一段在回答什么”
- 不使用“这条笔记回答的问题是：”“回答：”“这条链处理……”这类低信息量模板开头
- 对下游会直接进入 `argument-note Summary` 的内容，优先写成可直接复用的判断句，而不是说明性套话
- 若 source 混入目录、相关推荐、产品操作文档或剪藏噪音，必须在 `Ignored or de-weighted sections` 中明确排除，不得默认混入主文结论
- `Reopening cues` 优先写能帮助下游快速回到原文关键位置的短提示，如段落标题、开头句、指标所在段，而不是泛泛备注
- `Key tensions` 只写会影响可信度、适用边界、生成取舍或 argument placement 的 1-3 条张力；没有就写 `- 无`
- `Contradictions with existing notes` 只在 source 判断与仓库现有笔记存在需要显式处理的冲突时填写；没有就写 `- 无`
- 不输出开放式长问题清单，不做读者对话设计，不复制 `ljg-read` 的伴读交互层

## 参考 prompt 要点

从参考项目迁移时，保留这些工作习惯：

- 先做分析，再做生成
- 明确区分 entities / concepts / arguments / contradictions / recommendations
- 结合 folder context 判断主题归属
- 结论要“充分但简洁”，只保留真正重要的内容

## 风格示例

- 不推荐：`这条笔记回答的问题是：为什么 RAG 评测会失真。`
- 不推荐：`这条链处理检索优化问题。`
- 推荐：`RAG 评测结果常被基础设施噪声显著扰动，因此不能把分数差直接解释为能力差。`
- 推荐：`检索优化应从失败模式反推动作，再用准确率、延迟与成本共同筛选方案。`
- 不推荐：`为什么要学编程，以及编程能力是如何长出来的？`
- 推荐：`编程能力如何长出来？`
- 更推荐：`如何提升编程能力？`
- 不推荐：`什么是战略，战略与管理有何不同？`
- 推荐：`什么是战略？`
- 不推荐：`创作如何发生并被约束？`
- 推荐：`创作如何发生？`
- 不推荐：`如何把想法写成可传播的作品？`
- 推荐：`如何提升作品的传播度？`
