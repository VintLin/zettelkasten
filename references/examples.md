# Examples

## Example 1: one source -> one permanent note

Input:
A paragraph arguing that full-text search cannot replace intentional links because search gives unsorted similarity, while links preserve reasoning paths.

Output title:
Manual links preserve reasoning paths that search alone cannot recover

Reason:
The note captures one claim that can stand on its own.

## Example 2: one source -> overview note + detail notes

Input:
A long article explaining:
- what atomic notes are
- why they matter
- how to judge note scope
- how structure notes differ from atomic notes

Output:
1. Atomic notes aim at one knowledge building block
2. Atomicity is a heuristic, not a rigid law
3. Structure notes provide higher-level entry points

Reason:
The source contains multiple separable claims with different reuse value.

## Example 3: link rationale

Source note:
Manual links preserve reasoning paths that search alone cannot recover

Target note:
Structure notes reduce navigation cost in dense topic areas

Link:
- related_pattern [[202604091410 Structure notes reduce navigation cost in dense topic areas]] — Both notes address why explicit navigational structure outperforms raw retrieval when the archive becomes dense.

## Example 4: named framework disambiguation

Input:
A source file titled `七个习惯` that summarizes ideas from Stephen Covey's book.

Bad output title:
七个习惯是一套成长框架

Better output title:
史蒂芬·柯维的七个习惯把个人成长拆成主动性目标优先级协作理解统合与更新

Reason:
The better title tells the future reader what `七个习惯` refers to and exposes the core structure instead of assuming prior familiarity.

## Example 5: metaphorical method disambiguation

Input:
A source file titled `吃掉那只青蛙`.

Bad output opening:
吃掉那只青蛙说明要先吃青蛙。

Better output opening:
`吃掉那只青蛙`是 Brian Tracy 用来表达优先级管理的比喻，意思是先处理当天最重要也最容易拖延的任务。

Reason:
Metaphorical source labels must be translated into the concrete method or claim they point to.

## Example 6: required sections

Bad output:
The note body starts immediately after the title and omits explicit `Summary` and `Note` sections.

Better output:
Use:
- `## Summary`
- `## Note`
- `## Links`
- `## References`

Reason:
This repository requires stable section anchors so future agents can lint and enrich notes consistently.

## Example 7: named item needs a paired reference note

Input:
A source file titled `六项精进` with a detailed list of principles and background explanation.

Better output package:
- one permanent note in `wiki/` explaining the reusable claim
- one reference note in `references/` preserving the fuller source framing, principle list, and source path
- bidirectional links between the two

Reason:
The permanent note should stay compressed, while the reference note keeps the fuller source-side context available for future reading and synthesis.
