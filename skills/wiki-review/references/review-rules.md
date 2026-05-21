# wiki-review 规则

## 标准问题类型

- `contradiction`
- `ambiguous-named-item`
- `missing-reference-note`
- `ambiguous-argument-fit`
- `missing-entrance-fit`
- `weak-source-evidence`
- `possible-synthesis-opportunity`
- `theme-rank-issue`
- `theme-concept-boundary`

## 标准动作集

- `Update Existing`
- `Create New`
- `Defer`
- `Needs Judgment`

## 输出模板

```md
---REVIEW-ITEM---
Type: ...
Decision: Update Existing | Create New | Defer | Needs Judgment
Subject: ...
Affected files:
- ...
Reason:
- ...
Next step:
- ...
---END REVIEW-ITEM---
```

## 判断原则

- 先确认它是否真的阻塞当前流程
- 能稳定自动解决的，不要升级成 review
- 普通 open question 不等于 review item
- 如果只是缺信息而不影响当前落库，可标记为 `Defer`
- 若 review 指向主题或 `argument-note` 的边界问题，先运行 `wiki-rank`，再借用其四个判据做结构判断：
  - 先问“这个主题概念本身的秩是什么”，不要先看现成目录长什么样
  - 再问“它与相邻旧主题/母问题到底差在哪个生成器上”
  - 最后再落到“因此这个主题应该覆盖哪些 argument，不该覆盖哪些 argument”
  - `生成性`：这个主题/母问题还能否稳定生成并解释其下的论据，而不只是收纳它们
  - `最小性`：删掉或合并其中一个相邻母问题后，是否真的会损失不可替代的解释力
  - `独立性`：两个母问题能否在真实案例中独立变化，而不是换词重复
  - `预测力`：面对新材料时，这个主题/母问题是否能自然吸纳新笔记，而不是持续制造边界争议
- 这些判据只用于帮助判断是否应合并、改名、拆分或收紧主题，不单独产出“秩分析”正文
- 对“新主题概念是否成立”的 review，优先输出：
  - 该概念的最小解释骨架
  - 它和最近邻旧主题的差异
  - 应覆盖的 argument 范围
  - 不应覆盖的 argument 范围

## 参考 prompt 要点

从参考项目迁移的重点不是固定按钮，而是：

- 用窄类型归类问题
- 只保留真正需要人或后续任务判断的问题
- 给出明确的下一步，而不是泛泛描述问题
- 对主题和母问题的审核，优先找“真正独立的生成器”，不要把多个同义父问题并列保留
- 主题边界不是先看现有材料再凑名字，而是先解释概念，再反推边界与 argument 范围
