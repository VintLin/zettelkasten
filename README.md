# zettelkasten

一个给 Codex 用的 Zettelkasten 技能，用来把原始素材整理成可复用、可链接、可持续演化的 Markdown 笔记。

它适合处理读书摘录、原始想法、会议记录、文章片段、零散高亮和已有阅读笔记。目标不是保存原文，而是把素材压缩成能够独立成立的永久笔记、结构笔记和参考笔记。

## 这个 skill 做什么

- 把原始文本转换成永久笔记
- 按知识单元拆分原始材料，而不是按来源机械搬运
- 为命名框架、方法、书名、缩写和隐喻做显式消歧
- 为笔记补上 `Summary`、`Note`、链接理由和来源追踪
- 在需要时推荐或生成结构笔记
- 让新笔记能和已有 Obsidian 知识库形成有效连接

## 适用场景

- 把一篇文章或一组摘录转成 evergreen notes
- 把长笔记拆成多个原子化笔记
- 为新笔记确定标题、ID 和链接目标
- 维护以 Obsidian 为前端的 Markdown 知识库
- 将 source-oriented notes 压缩成 future-oriented notes

## 核心原则

- 一条永久笔记只承载一个主要知识构件
- 标题要暴露实际观点，而不是保留模糊标签
- 命名对象必须说明它是什么、来自哪里、为什么重要
- 链接必须有关系理由，不能只靠关键词碰撞
- 默认先做单源处理，再决定是否需要跨源综合
- 结构笔记是入口和地图，不是信息堆积区

## 输入

这个 skill 预期接收以下一种或多种输入：

- 原始文本
- 阅读笔记或摘录
- 会议纪要或转录
- 来源元数据，如作者、标题、年份、URL、页码、时间戳
- 已有永久笔记或结构笔记
- 用户偏好，如语言、标题风格、笔记粒度、ID 规则

## 输出

默认输出会围绕以下内容组织：

- 转换摘要
- 笔记清单
- 永久笔记 Markdown
- 参考笔记 Markdown
- 结构笔记更新建议
- 链接关系与理由

仓库约束里要求所有相关笔记至少包含：

- `## Summary`
- `## Note`

## 工作流

1. 判断当前输入是文章、摘录、粗糙想法、会议记录还是混合材料。
2. 提取候选知识单元，如定义、主张、原则、方法、对比、命名对象。
3. 先聚类，再决定哪些内容应该合并成一条笔记，哪些应该拆开。
4. 生成可独立理解的永久笔记标题、ID、摘要、正文、链接和来源。
5. 遇到框架、书籍、方法、缩写或隐喻时，补建或更新对应参考笔记。
6. 如果主题已经形成可导航区域，再考虑创建或更新结构笔记。

## 仓库内容

- [`SKILL.md`](./SKILL.md): 技能主说明，定义触发条件、工作流和输出顺序
- [`references/note-schema.md`](./references/note-schema.md): 永久笔记和参考笔记的最小结构要求
- [`references/linking-rules.md`](./references/linking-rules.md): 链接关系和链接理由规则
- [`references/structure-note-rules.md`](./references/structure-note-rules.md): 结构笔记的创建与维护规则
- [`references/examples.md`](./references/examples.md): 输入输出示例
- [`evals/evals.json`](./evals/evals.json): 评估样例

## 适合的知识库形态

这个 skill 更适合：

- Markdown 原生知识库
- Obsidian 为主要浏览界面的仓库
- 希望保留来源追踪、又希望笔记可独立复用的工作流
- 由 LLM 持续维护的个人研究或写作知识库

## GitHub 项目简介

建议的 About 描述为：

`Codex skill for converting raw source material into linked Zettelkasten-style Markdown notes.`
