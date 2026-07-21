# Cloud Agent Contract

- One virtual machine, one assigned book, one `translate/<slug>` branch.
- Never run `init` or `lock-titles`; all six books are already initialized.
- Do not modify `main`, shared scripts, styles, glossaries, or another book directory.
- Commit only completed blocks plus their checkpoint changes. Do not commit temporary files or assembled `.zh.md` output.
- Use repository-relative paths: `sources/<book>.md` and `pipeline/translate/<book>/`.
- Before a PR, require `done == total`, verification with zero ERROR, a small source/translation sample review, and a `DONE_<book>.flag` that records remaining WARN items.
- Information theory is a repair-first branch: fix existing formula/heading corruption before translating further.
