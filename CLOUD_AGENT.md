# Cloud Agent Contract

- One virtual machine, one assigned book, one `translate/<slug>` branch.
- Never run `init` or `lock-titles`; every book already promoted into `sources/` has been initialized and title-locked by the control model.
- Do not modify `main`, shared scripts, styles, glossaries, or another book directory.
- Commit only completed blocks plus their checkpoint changes. Do not commit temporary files or assembled `.zh.md` output.
- Use repository-relative paths: `sources/<book>.md` and `pipeline/translate/<book>/`.
- `sources/pending/` contains uninitialized future books. Do not translate, initialize, lock titles for, or move one until the control model has completed its `SOURCE_INTAKE.md` preflight.
- Before a PR, require `done == total`, verification with zero ERROR, a small source/translation sample review, and a `DONE_<book>.flag` that records remaining WARN items.
- Information theory is a repair-first branch: fix existing formula/heading corruption before translating further.
