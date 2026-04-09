---
name: zettelkasten
description: Convert raw source text, highlights, reading notes, excerpts, meeting notes, or rough thoughts into permanent Zettelkasten-style notes. Use this skill whenever the user wants to turn source material into evergreen notes, permanent notes, atomic notes, literature notes, note links, structure notes, or asks how a new note should connect to existing notes. Also use this skill when the user provides raw text plus an existing note corpus and wants note splitting, note titles, IDs, relationship suggestions, structure-note updates, or a Markdown note package ready to save.
compatibility:
  - Works best when raw text, source metadata, and existing notes are available.
  - If existing notes are large, search them first and only load the most relevant notes into working context.
---

# Zettelkasten

Turn source material into reusable permanent notes.

Your job is not to preserve the source verbatim.
Your job is to convert source material into notes that can stand on their own, connect to other notes, and help future writing and thinking.

## Core principles

- Treat the note system as a web of thoughts, not a bucket of excerpts.
- Prefer one knowledge building block per permanent note.
- Start with the most general concept per cluster, then split details only when needed.
- Write in the user's own knowledge language: simple, direct, reusable phrasing.
- If the source contains a named framework, book title, coined term, acronym, or metaphor, make the referent explicit instead of preserving the name as unexplained shorthand.
- Every note in this repository must contain `## Summary` and `## Note`.
- Create links intentionally and explain why each link exists.
- Do not force top-down categories.
- Use structure notes as entry points, maps, or thinking canvases when a topic needs navigation.
- When multiple source files are provided, process them sequentially, one source file at a time.
- Do not compile multiple source files into multiple note batches simultaneously unless the user explicitly asks for a combined synthesis pass.

## When this skill should trigger

Use this skill when the user asks to:
- convert raw text into permanent notes
- turn reading notes / literature notes / highlights into evergreen notes
- split notes into atomic notes
- link a new note to old notes
- generate structure notes or hub notes
- organize note Markdown structure
- decide whether a source should become one note or many
- preserve source references while rewriting in the user's own words

## Inputs

You may receive any of these:

1. Raw source text
2. Reading notes / highlights / excerpts
3. Optional source metadata
   - title
   - author
   - year
   - url / publisher
   - page / chapter / timestamp
4. Optional existing note corpus
5. Optional existing structure notes
6. Optional user preferences
   - note ID style
   - Markdown format
   - preferred title style
   - desired granularity
   - language

If something is missing, proceed with reasonable defaults and explicitly mark assumptions.

## Required workflow

Follow this workflow in order.

### Pre-step: Decide processing scope

If the input contains multiple source files:
- pick one source file as the active unit of work
- finish its extraction, note drafting, linking, and file updates before moving to the next file
- do not draft notes for several files in parallel
- only perform cross-file synthesis after the single-file compilation pass is complete, or when the user explicitly asks for synthesis first

### Step 1: Identify the source mode

Classify the input source as one of:
- article / book / paper excerpt
- meeting / lecture / transcript
- rough thought dump
- existing reading notes
- mixed material

Then infer the likely note conversion mode:
- direct concept extraction
- claim extraction
- argument mapping
- process / framework extraction
- observation to principle
- multi-note cluster conversion

### Step 2: Extract candidate knowledge units

From the raw material, extract candidate units such as:
- concept
- definition
- claim
- argument
- counterargument
- fact / observation
- principle
- method / workflow
- distinction / contrast
- named entity that needs disambiguation
- framework components
- source metaphor and its concrete meaning

Do not copy large source passages.
Compress the material into candidate knowledge units in your own words.

### Step 3: Cluster before writing

Group candidate units into clusters by shared purpose or idea.

For each cluster:
- identify the central claim or concept
- list prerequisites
- list possible supporting details
- decide whether the cluster can stand as one note
- if not, split it into:
  - one concept overview note
  - zero or more detail notes

Default rule:
- start with one general note per cluster
- split only when prerequisites, exceptions, or supporting mechanisms make the note too dense
- if a cluster contains a named framework, book, method, acronym, or metaphor that future notes will reference, consider producing one `wiki/` note plus one paired `references/` note

### Step 4: Decide note scope

A permanent note is valid only if:
- it can be understood at first glance
- it can be given a precise title
- it can stand on its own with minimal extra context
- it suggests a next intellectual move
- it does not hide multiple unrelated claims in one body

If the note fails these checks, split or rewrite it.

### Step 5: Draft permanent notes

For every permanent note, generate:

1. unique ID
2. title
3. `## Summary`
4. `## Note`
5. links section
6. references section
7. optional tags
8. optional structure-note recommendation

Always write clear, short paragraphs.
Prefer declarative titles over vague topic labels.

Additional repository rule for named items:
- if the note centers on a named framework, book, method, acronym, or metaphor, the note must become self-explanatory without reopening the source
- state early what the thing is, where it comes from, and what its core parts or core claim are
- do not title or summarize the note in a way that assumes prior familiarity with the source label alone
- if the original label is metaphorical, include the concrete meaning in the title or first paragraph
- create or update a paired `references/` note when the fuller source-side introduction, outline, or component list is worth preserving
- connect the `wiki/` note and `references/` note with bidirectional links
- prefer `references/` for stable names such as books, frameworks, methods, models, acronyms, and long-lived coined terms
- do not create a `references/` note merely for a one-off source article title unless that page will genuinely serve as a hub for multiple permanent notes

### Step 6: Find and justify links

If existing notes are available, inspect them and propose only meaningful links.

For each proposed link:
- identify the target note
- classify the relationship
- write one sentence explaining why the link exists

Allowed relationship types:
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

Do not create links only because of keyword overlap.
A link is valid only if the relation would still make sense to the future reader.

### Step 7: Consider structure notes

If the new notes open or expand a navigable topic area, decide whether to:
- add the note to an existing structure note
- recommend creating a new structure note
- skip structure-note work if the topic is still too small

Use structure notes for:
- topic entry points
- map of related ideas
- active research questions
- writing/project outlines
- grouped trails through multiple permanent notes

### Step 8: Output package

Always output in this order:

## Conversion summary
- source mode
- number of clusters
- number of permanent notes created
- whether a structure note update is recommended

## Note inventory
- one-line list of all generated notes

## Permanent notes
- full Markdown for each note

## Link plan
- source note -> target note
- relation type
- rationale

## Structure note action
- update existing / create new / none
- draft Markdown if update or creation is recommended

## Open ambiguities
- assumptions made
- weakly supported claims
- places where source context may be insufficient

## Permanent note format

Use this exact format:

```md
---
id: <YYYYMMDD-title>
title: <clear declarative title>
type: permanent-note
source_type: <article|book|paper|meeting|thought-dump|mixed>
created: <YYYY-MM-DD>
tags:
  - <optional-tag>
---

# <title>

## Summary
<1-2 sentence summary of the note>

## Note
<self-contained body written in clear paragraphs>

## Links
- <relation-type> [[<target-id>|<target-title>]] — <why this link exists>

## References
- <author / title / year / locator / url if available>
````

Additional note constraints:
- The note filename must be exactly `<id>.md`.
- By default, `<title>` should be written in Chinese for this repository.
- By default, `<id>` must use the repository's canonical `timestamp-title` format, where `timestamp` is `YYYYMMDD` derived from `created` and `title` matches the Chinese note title.
- Do not generate English slug IDs unless the user explicitly requests another ID scheme.

## Structure note format

Use this exact format when needed:

```md
---
id: <YYYYMMDD-title>
title: <topic entry point title>
type: structure-note
created: <YYYY-MM-DD>
tags:
  - structure-note
---

# <title>

## Purpose
<what area this structure note helps navigate>

## Entry points
- [[<note-id>|<note-title>]] — <why start here>

## Subtopics
### <subtopic-name>
- [[<note-id>|<note-title>]] — <relationship or role>

## Open questions
- <question 1>
- <question 2>
```

## Quality bar

A good output:

* rewrites instead of copying
* preserves source traceability
* creates notes that are reusable without reopening the source
* links notes with explicit meaning
* avoids fake precision and weak links
* proposes structure notes only when they add navigational value

A bad output:

* large quoted passages
* vague titles like "AI", "thoughts", "reading notes"
* links based only on shared words
* one huge note containing many claims
* rigid category trees
* missing references

## If existing notes are missing

If the user did not provide existing notes:

* still create permanent notes
* add a "Potential links to look for later" subsection inside each note
* suggest what kinds of old notes should be searched next

## If source evidence is weak

If the source is fragmentary or ambiguous:

* keep the note tentative
* mark uncertainty in the summary or body
* avoid overstating claims
* include an ambiguity note in the output package

## Style

Use the user's language if specified.
Be concise, but do not compress away meaning.
Prefer clarity over elegance.
Explain the why of links and splits.
