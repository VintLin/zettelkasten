# Linking Rules

## Goal
Create links that preserve reasoning, not just topical overlap.

## Link eligibility test

A proposed link is valid only if:
1. the relation can be named
2. the rationale can be stated in one sentence
3. the relation would still make sense without keyword similarity
4. following the link advances understanding

If any of these fail, do not create the link.

## Preferred relation types

- supports
- extends
- contrasts
- refines
- prerequisite_for
- consequence_of
- example_of
- application_of
- related_pattern
- open_question_from

## Linking heuristics

### supports
Use when the target note gives evidence, grounding, or basis.

### extends
Use when the target note develops the same idea into a broader or deeper direction.

### contrasts
Use when the target note presents a tension, limitation, or opposing framing.

### refines
Use when the target note makes the current note more precise.

### prerequisite_for
Use when the current note cannot be fully understood without the target concept.

### consequence_of
Use when the current note is better read as an outcome of the target note.

### example_of
Use when the current note concretizes an abstraction in the target note.

### application_of
Use when the current note applies a general principle from the target note.

### related_pattern
Use when the notes share a useful structural analogy.

### open_question_from
Use when one note naturally raises the question handled by another note.

## Direction rule

Pick the direction that is most useful for future traversal.
Ask:
- if I am reading note A, would note B be the natural next move?

## Anti-patterns

Do not link:
- because both notes share a noun
- because both notes belong to the same topic folder
- because the model "feels" they are similar
- because backlinks look nice

## Link annotation format

- <relation-type> [[<id>|<title>]] — <one-sentence rationale>

## Repository-specific note

For this repository:
- treat the note `id` as the canonical link target
- prefer Chinese note titles
- keep filename and `id` identical aside from the `.md` suffix
- never use `[[id title]]`, because it is not valid Obsidian alias syntax
