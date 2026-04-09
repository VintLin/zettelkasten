# Note Schema

## Goal
Define the minimum usable schema for a permanent note.

## Required fields

### id
- must be unique
- default to `timestamp-title` ID unless the user specifies another scheme
- use `YYYYMMDD-中文标题` as the repository default
- must exactly match the note filename without the `.md` suffix
- if `created` is present, derive the `YYYYMMDD` part from that date
- never change an existing ID just to make it prettier unless the repository is being intentionally migrated to a new canonical scheme

### title
- must expose the actual thought
- should usually be written in Chinese in this repository
- prefer a declarative statement, distinction, or question
- if the note includes a named framework, book, acronym, or metaphor, the title must help the reader identify what that thing is instead of leaving it as unexplained shorthand
- avoid broad labels such as:
  - AI
  - productivity
  - thoughts
  - chapter 3 notes

### summary
- required section header: `## Summary`
- 1-2 short paragraphs or a compact equivalent
- should let the future reader decide in seconds whether the note is relevant

### note body
- required section header: `## Note`
- should stand on its own
- should be written in the user's own words
- should contain one knowledge building block
- can include examples, conditions, exceptions, and consequences
- should not depend on reopening the source
- if the note is about a named item, the opening paragraph should disambiguate the referent, origin, and core components or thesis

### links
- every link must carry a reason
- if no real links are available, do not fabricate them
- use valid Obsidian wikilinks
- when linking by canonical ID with a readable label, use `[[id|title]]`
- do not use invalid mixed syntax such as `[[id title]]`

### references
- include enough metadata to trace the source
- if the note captures an original thought, leave the reference section minimal but present

## Optional fields

### tags
Use sparingly.
Prefer precise tags over broad categories.

### aliases
Only add when the user already uses alias-heavy conventions.

### status
Optional. Example:
- seed
- stable
- tentative

## Repository-specific types

- `permanent-notes`: reusable knowledge claims in `wiki/permanent-notes/`
- `structure-notes`: navigation and map notes in `wiki/structure-notes/`
- `reference-notes`: literature and reference notes in `references/`
