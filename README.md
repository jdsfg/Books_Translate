# Books Translate

Private cloud-translation workspace. Canonical translation state is stored in `pipeline/translate/<book>/checkpoint.json` and `blocks/<id>.md`; assembled `sources/<book>.zh.md` files are derived and ignored.

## Cloud workflow

1. Create or switch to one `translate/<slug>` branch per book.
2. Use `python pipeline/translate_book.py status sources/<book>.md`.
3. Translate only the next block, then commit through `python pipeline/translate_book.py commit <source> <block-id> --file <temporary-file>`.
4. Push small batches to the assigned branch. Never push directly to `main`.
5. Run the book-specific verification command before opening a pull request.

See `CLOUD_AGENT.md` and `STATUS.md` before translating.
