# Books Translate review rules

For pull requests that change `pipeline/translate/<book>/blocks/`:

1. Treat `sources/<book>.md` and the block `src` fields in
   `pipeline/translate/<book>/checkpoint.json` as the English source of truth.
2. Do not accept `verify ERROR=0` as proof of translation quality. It only
   proves mechanical structure.
3. Compare changed translations with their complete source blocks. Flag:
   - omitted or duplicated paragraphs;
   - truncated block beginnings or endings;
   - missing Q numbers, question stems, hints, answers, list items, tables,
     formulas, footnotes, numbers, units, and chapter references;
   - reversed meaning, unjustified strengthening/weakening, or literal Chinese
     that changes the claim;
   - ordinary untranslated English outside code, formulas, abbreviations,
     proper names, and intentional first-use terminology;
   - glossary violations, especially statistical and scientific terms.
4. Inspect adjacent blocks whenever content was realigned or moved.
5. For technical books, check every formula and exact number in changed blocks.
6. A completed book must have `done == total`, zero verification errors,
   explained warnings, an independent chapter sample, and
   `pipeline/translate/<book>/DONE_<book>.flag`.
7. Never recommend `init`, `lock-titles`, direct edits to generated `.zh.md`
   files, or changes to another book's directory.

Report concrete block IDs and quote both source and translation for every
blocking semantic finding.
