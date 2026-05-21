# wiki-generation 规则与模板

## 生成顺序

按这个顺序处理：

1. permanent notes
2. reference notes
3. argument notes
4. structure notes
5. processing report
6. review blocks

## 关键要求

- 新 permanent note 必须进入至少一个 argument note
- 新建 permanent note 前必须检查是否已有笔记可更新；同一可复用论点的新证据、例子、限制、反例、来源或更好表述，优先更新已有笔记
- 只有当候选内容承担新的判断、方法、区分、问题或 argument 位置时，才新建 permanent note
- 新或更新的 argument note 必须进入至少一个 structure note
- `structure-notes` 只收 `argument-notes`
- `structure-notes` 不与其他 `structure-notes` 建立主题层关系
- `structure-notes` 不直接收 `permanent-notes`
- `reference-notes` 主要服务 `permanent-notes`
- `reference-notes` 是稳定命名对象的源头语境页，不是主题层、argument 容器或摘抄堆
- 保留原文显式链接
- 保留必要配图
- 使用 `**加粗**`、`_斜体_`、`==高亮==` 改善可读性，但不要滥用
- `source-analysis` 只提供候选原始笔记与候选 argument 关联；最终 argument 插入、`supports` / `next`、structure 挂接均由 `wiki-generation` 决定

## 最小笔记约束

- 文件名使用 `timestamp-title` 格式
- frontmatter `id` 必须与文件名一致，不含 `.md`
- `type` 只能是：
  - `permanent-notes`
  - `reference-notes`
  - `argument-notes`
  - `structure-notes`
- 所有 canonical notes 必须包含：
  - `## Summary`
  - `## Note`
- 标题要直接暴露实际观点、方法、问题或区分，不要只保留模糊标签
- 若涉及书、框架、方法、模型、缩写或隐喻名称，开头必须明确它是什么、来自哪里、为何重要

## 链接规则

- 链接要保留“为什么要连”，不是只因主题相近
- 只有当关系可以被命名、理由可以用一句话说清、且跟随链接能推进理解时才创建链接
- 默认使用有效 Obsidian 语法：
  - `[[id|title]]`
- 不要使用无效格式：
  - `[[id title]]`

常用关系：

- `supports`
- `next`

链接注释格式：

```md
- <relation> [[<id>|<title>]] — <一句话说明关系理由>
```

结构层硬规则：

- `structure-note` 只与 `argument-note` 关联
- `argument-note` 只与 `structure-note` 和 `permanent-note` 发生结构性关联
- `permanent-note` 用 `supports` 指向 argument，用 `next` 指向同一链路中的下一条 permanent
- 不使用 `related`、`related_pattern` 或其他横向关系充当结构性链接
- 若某对象本质上是书、框架、方法、模型或稳定命名对象，应优先作为 `reference-note` 被引用，而不是作为主题层节点

## 推荐模板

### permanent note

```md
---
id: YYYYMMDD-标题
type: permanent-notes
created: YYYY-MM-DD
---

# 标题

## Summary

一句到两句说明笔记核心价值。

## Note

正文。必要时使用：

- `**加粗**` 标出关键判断
- `_斜体_` 标出限定条件
- `==高亮==` 标出需要特别记住的结论
- `![[image.ext]]` 放入理解所需配图

## Links

- supports [[...|...]] — 指向至少一个 argument note
- next [[...|...]] — 仅在该原子笔记于某条 argument 链中确有稳定后继时保留

## References

- from [[文件名|标题]]
- references [[文献笔记文件名|标题]]
- 若有原始网页，再补 `url: https://...`
```

### reference note

```md
---
id: YYYYMMDD-标题
type: reference-notes
created: YYYY-MM-DD
---

# 标题

## Summary

说明这个框架 / 方法 / 书 / benchmark / 术语是什么，以及为什么要保留这页作为源头语境。

## Note

建议按下面四类信息组织，而不是写成松散摘要：

- 它是什么：
- 来源与语境：
- 核心定义 / 组成 / 边界：
- 与哪些 permanent notes 相关：

重点是保留 stable named object 的源头展开，帮助后续回看语境，而不是重复 argument 链或替 permanent note 下结论。

## Links

- [[permanent-note-id|标题]] — 这条原子笔记提炼了该对象的哪一部分
- [[permanent-note-id|标题]] — 若有第二条原子笔记，说明它提炼了另一条可复用判断

## References

- from [[来源文件名|标题]]
- 若该页还依赖其他参考对象，再补 `references [[reference-note-id|标题]]`
- 若原始网页仍重要，再补 `url: https://...`
```

要求：

- `reference-note` 的主要职责是保存稳定命名对象的源头语境，不承担主题导航职责
- `Summary` 先回答“它是什么，为什么值得保留”，不要直接写成永久结论
- `## Note` 应优先保留定义、组成、边界、典型场景、来源语境，而不是堆大量逐条摘抄
- `## Links` 只用于指向由该对象提炼出的相关 `permanent-notes`
- 不在 `reference-note` 中使用 `supports` / `next`
- 不使用 `related_pattern`、`related` 等伪结构关系
- 不把 `argument-notes` 或 `structure-notes` 作为 `reference-note` 的主要链接对象
- `## References` 统一使用 `from` / `references` / `url`
- 不写 `来源文件：`、`来源链接：`、`主题来源：` 这类自然语言标签
- 对 vault 内文件优先使用 filename-only wikilink；不要在 `from` 中写长路径说明文本

### argument note

```md
---
id: YYYYMMDD-标题
type: argument-notes
created: YYYY-MM-DD
---

# 标题

## Summary

完整说明该论点或问题在回答什么，并把下方 `### 论据` 的总体推进关系、结论方向与限制条件压成一段总体推论。不能只改写标题，也不能脱离下方论据另写一套说法。

## Note

### 论点 / 问题

...

### 论据

1. [[...|...]]：说明这条笔记在论证链中的起点作用。
2. [[...|...]]：说明这条笔记如何承接上一条，而不是只重复本条内容。

> 分叉原因：...

**分叉 A**

3. [[...|...]]
4. [[...|...]]
5. [[...|...]]

> 分叉原因：...

**分叉 B**

3. [[...|...]]
4. [[...|...]]

---

1. [[...|...]]
2. [[...|...]]
```

要求：

- 标题必须直接写成元论点或元问题，不要写成流程说明、操作步骤标题或任务清单标题
- 一个 `argument-note` 标题只表达一个母问题，不要把并列子问题、边界条件、具体技术分支一起塞进标题
- 标题优先保持短、自然、可扩展；默认先选更简单的母问题标题，再把复杂限定放进 `Summary`
- 标题必须像读者会自然提出的问题，不能像作者对链路的解释句、机制句或压缩后的摘要句
- 标题要在自然和精确之间取中间带，不要为了口语化而改成过强口语句、结果解释句或聊天式提问
- 优先使用“如何建立产品优势”“如何判断消费是否值得”“招聘方如何判断岗位匹配度”这类自然但保留概念精度的标题
- 避免把标题写成“这笔钱该不该花”“产品为什么能长期赢”“招聘方到底在看什么”这类虽然口语但边界变松、概念变虚的表达
- 不把阶段、限制条件、评测口径、方法细分、结论方向直接塞进标题，除非删掉它就会变成另一个问题
- 不把“真正 / 稳定 / 长出来 / 被约束 / 并形成 / 并提高 / 可用且可维护 / 可操作性层级”这类解释腔修饰默认塞进标题
- `argument-note` 只与 `structure-notes` 和 `permanent-notes` 发生结构性关联，不建立 `argument -> argument` 关系
- `argument-note` 的 Summary 必须完整基于下方论据，对问题给出总体推论、限制条件和链路说明
- `argument-note` 的 Summary 必须直接进入问题与结论，不使用“这条论点笔记回答的问题是：”“回答：”“这条链处理……”这类低信息量模板开头
- `argument-note` 的 Summary 第一字就应进入判断，不先解释“这篇笔记在回答什么”或“这条链在处理什么”
- `argument-note` 的职责是回答一个稳定母问题，并把一组原子笔记组织成可阅读、可扩展、可继续插入的推理骨架
- 对主题层 argument，优先使用高层母问题标题，例如“如何知识管理？”“如何学习？”“如何调研？”“如何复盘？”“如何优化RAG提升检索质量？”
- 若某个具体判断只是母问题下的一个子判断，例如 “何时采用 GraphRAG”，应写进论据，不应与母问题并列写进标题
- 标题应足够稳定，能容纳后续新增笔记；若新笔记只是补充同一问题，不要频繁改成更长的标题
- 如果两个标题都能成立，优先选择更短、更上位、读起来像自然问题的那个
- 不要写“先确立 / 再指出 / 继续细化 / 最后落地”这类连接词
- 每条编号直接写该条论据承担的作用或提供的证据
- 从第 `2.` 条开始，描述中必须显式写出它与前一条为何能衔接，例如它是前提展开、设计推论、执行细化、边界补充、限制条件或结果
- 不要把论据写成只有主题相近的并列清单；读者应能仅靠编号说明看懂链条为什么往下走
- 不要使用“既然上一条”“上一条已经明确”“接着”“然后”等元叙述口吻；只陈述当前条目的关键信息与它在链中的推进作用
- 分叉标题使用 `**分叉 A**`、`**分叉 B**`
- 每个分叉前先用 `> 分叉原因：...` 说明为何从这里分出不同路径
- 没有分叉时，只保留连续编号的 `### 论据`
- 若属于同一母问题但暂时不在同一逻辑链路下，允许使用 `---` 分隔断连链
- `---` 前后分别从 `1.` 重新编号
- 断连链表示“同题不同链”，不是分叉

高质量标准：

- 读者只看标题，就能知道这条笔记在回答哪个母问题
- 读者只看 `## Summary`，就能把握整条论证链的方向、结论与限制
- 读者只看 `### 论据` 的编号说明，也能看懂各条之间为什么这样排序
- 读者应先从标题看到“主题地图”，而不是先读到已经压缩好的答案
- 新原子笔记进来时，通常应能插入现有链路，而不是迫使整条母问题重写
- 若两条 argument 的边界长期高度重叠，应合并或重写边界，不用 `argument -> argument` 关系补缝

argument 标题取名逻辑：

1. 先问：这页到底在回答哪个母问题？
2. 再问：如果把标题里的限定词去掉，这页还是同一个问题吗？
3. 若是同一个问题，删掉限定词，把限定放进 `Summary`
4. 若删掉后会变成另一个问题，才把该限定保留在标题

简单判断法：

- 标题像目录入口、能挂后续新笔记：通常是对的
- 标题像压缩后的结论句：通常太细
- 标题里出现两个以上并列限定：通常太复杂
- 标题必须读完后半句才知道在问什么：通常太复杂
- 标题是“飞轮 / 闭环 / 框架 / 模型”这类抽象机制名，但正文真正回答的是更具体的人类问题：通常不是合格母问题
- 标题像“分析者在解释这页干了什么”，而不像“读者在问什么”：通常不合格

正反例：

- 不推荐：`如何区分Agent评测中的能力变化与基础设施噪声？`
- 推荐：`如何评测Agent？`
  噪声隔离、资源披露、3x 分界写进 `Summary` 和论据

- 不推荐：`如何建立面向交付的Agent学习路径？`
- 推荐：`如何学习Agent？`
  面向交付、PoC 驱动、简单工作流优先写进 `Summary` 和论据

- 不推荐：`如何把经验编码成可调用的外部记忆？`
- 推荐：`如何构建外部记忆？`
  可调用、可重组、再次触发这些是链路结论，不必全塞进标题

- 不推荐：`如何把知识转成可验证行动？`
- 推荐：`如何把知识转成行动？`
  “可验证”是行动质量要求，写进 `Summary`

- 不推荐：`神话如何借象征解释人和世界？`
- 推荐：`神话如何解释人和世界？`
  “借象征”是解释机制，放进 `Summary` 和论据

- 不推荐：`为什么要学编程，以及编程能力是如何长出来的？`
- 推荐：`编程能力如何长出来？`
  “为什么值得学”可以写进 `Summary` 作为背景与意义，不必和母问题并列写进标题

- 不推荐：`什么是战略，战略与管理有何不同？`
- 推荐：`什么是战略？`
  与管理的边界差异是关键论据，不必和定义问题并列占据标题

- 不推荐：`如何把阅读组织成可持续的高质量实践？`
- 推荐：`如何进行高质量阅读？`
  可持续、实践化属于执行条件，写进 `Summary` 和论据

- 不推荐：`理解与记忆如何在认知系统中被长期巩固？`
- 推荐：`如何让记忆与理解稳定沉淀？`
  认知系统、长期巩固属于机制说明，放进 `Summary` 更自然

- 不推荐：`编程能力如何长出来？`
- 推荐：`如何提升编程能力？`
  优先写人会问的问题，不写分析者视角的成长机制句

- 不推荐：`如何让记忆与理解稳定沉淀？`
- 推荐：`如何沉淀经验？`
  如果更短的人话问题仍覆盖同一页，就优先用更短题法

- 不推荐：`创作如何发生并被约束？`
- 推荐：`创作如何发生？`
  “被约束”属于机制说明，放进 `Summary` 和论据

- 不推荐：`如何把想法写成可传播的作品？`
- 推荐：`如何提升作品的传播度？`
  优先使用读者会直接关心的结果性问题

- 不推荐：`如何设计真正可用且可维护的知识管理系统？`
- 推荐：`如何设计知识管理系统？`
  “真正可用且可维护”是判断标准，不是母问题本体

- 不推荐：`如何提升工程协作质量并形成健康团队文化？`
- 推荐：`如何做好工程协作？`
  标题不要把手段、效果和延伸结果一起并列写满

- 不推荐：`如何校准判断并减少偏误？`
- 推荐：`如何校准判断？`
  “减少偏误”是校准的结果，不需要与母问题并列占标题

- 不推荐：`如何形成稳定的评价能力？`
- 推荐：`如何形成判断力？`
  术语感过重时，优先换成更自然的人话表达

- 不推荐：`如何形成学习思考创作飞轮？`
- 推荐：`如何打磨作品？` / `如何构建长期有效的学习系统？`
  “飞轮”更适合作为链路机制说明，而不是独立母问题；应回到读者真正关心的人类问题

- 不推荐：`如何做好 RAG 检索优化并判断何时采用 GraphRAG？`
- 推荐：`如何优化RAG提升检索质量？`
  `GraphRAG` 采用边界属于子判断，写进论据

Summary 写法示例：

- 不推荐：`这条论点笔记回答的问题是：如何让学习长期有效。核心结论是，学习系统需要...`
- 不推荐：`这条链处理学习系统的总目标、方向与能力组合。`
- 推荐：`长期有效的学习系统，不是围绕信息囤积，而是围绕知识体系、反馈闭环、方向选择和能力组合来设计。`
- 推荐：`消费和支出判断应服务长期生活结构，而不是服务短期刺激；关键在于节制、时间自由、容错空间，以及支出是否通过价值观与目标审查。`

反例：

- 不推荐：`如何做好 RAG 检索优化并判断何时采用 GraphRAG？`
- 推荐：`如何优化RAG提升检索质量？`
  `GraphRAG` 的采用边界写进后续论据链

### 链路整理阶段的 permanent note links

当某组 `permanent-note` 正在被整理进某个 `argument-note` 时，默认只保留最小链接集：

- 每条保留：
  - `supports [[argument-note-id|标题]]`
- 若顺序已经稳定，再额外保留：
  - 指向下一条原子笔记的 `next [[next-note-id|标题]]`
- 链条最后一条只保留 `supports [[argument-note-id|标题]]`
- 暂不保留与当前 argument 无关的横向链接、扩展链接、related links；等整组 argument 稳定后再补
- 不以 `related`、`related_pattern` 或其他替代字段表达结构性关系
- 原子笔记至少要有一个 `supports [[argument-note-id|标题]]`
- 若发现原子笔记还没有接入任何 argument，不能直接跳过，必须由 agent 判断应插入哪条 argument；若现有 argument 都不合适，则新建或改写 argument 后再接入
- `## References` 统一优先使用：
  - `from [[文件名|标题]]`
  - `references [[文献笔记文件名|标题]]`
  - 若原始网页仍重要，再补 `url: ...`
- 不要在 `from` 中写 `archive/.../...` 这类整段相对路径；对 archive 文件只保留可跳转的文件名 wikilink

### structure note

```md
---
id: YYYYMMDD-标题主题
type: structure-notes
created: YYYY-MM-DD
---

# 标题主题

## Summary

说明该主题覆盖什么问题，以及不覆盖什么问题。

## Note

- [[argument-id-1|论点 1]]：为什么这是进入该主题的第一条母问题
- [[argument-id-2|论点 2]]：它和上一条母问题的边界区别是什么
```

要求：

- `structure-note` 是主题笔记，只负责定义主题边界并列出该主题下最值得先进入的 `argument-notes`
- `structure-note` 只作为主题层，正文只列 `argument-notes`
- 不写 `Related entrances` 去连接别的 `structure-note`
- 不直接挂 `permanent-notes`
- 若某个主题本质上是一本书、一个框架、一个方法或一个稳定命名对象，应优先改为 `reference-note`，再把相关原子笔记接入合适的 argument
- 同一条 argument 不要在同一页重复罗列多次；如需分组，分组必须提供新的边界信息，而不是重复目录
- `Summary` 说明的是主题结构与边界，不是对整个主题下结论
- `Open questions` 仅在确实影响后续拆分、合并或挂接决策时保留；没有就不写

高质量标准：

- 读者一眼就能知道这个主题处理什么，不处理什么
- 读者能看出各条 argument 之间的分工与进入顺序
- 页面足够短，主要承担导航而不是展开论证
- 后续新增笔记时，大多数情况是补进已有 argument，而不是不断给主题页加重复分组

## Processing Report

默认写到 `outputs/processing/<source-id>-report.md`。

用这个格式输出本次处理总结：

```md
## Processing Report

- Source:
- Source ID:
- Analysis file:
- Created notes:
- Updated notes:
- Argument changes:
- Structure changes:
- Preserved links:
- Preserved images:
- Remaining review items:
```

如本轮已完成归档，可再补两行：

```md
- Archived source: `archive/...`
- Archived analysis: `archive/.cache/<source-id>-analysis.md`
```

## Review Block

默认追加在同一个 `outputs/processing/<source-id>-report.md` 文件中。仅在无法稳定自动裁决时输出：

```md
---REVIEW---
Type: ambiguous-argument-fit | missing-entrance-fit | ambiguous-named-item | contradiction | missing-reference-note | weak-source-evidence | possible-synthesis-opportunity
Subject: ...
Affected files:
- ...
Why unresolved:
- ...
Recommended next step: Update Existing | Create New | Defer | Needs Judgment
---END REVIEW---
```

## 参考 prompt 要点

从参考项目迁移这些习惯：

- 先依据分析结果生成，不直接从原文跳到正式笔记
- 明确哪些内容应创建、哪些内容应更新
- 如果发现与现有笔记有连接，要显式写出 cross-reference
- 只为真正需要人工判断的问题输出 review
- 生成阶段结束后要把活跃工作产物收口，不把已完成 source 留在 `raw/` 或 `.cache/`
