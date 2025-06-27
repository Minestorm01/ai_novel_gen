# Writer-Bot ✍️  ![CI](https://github.com/your-user/writer-bot/actions/workflows/ci.yml/badge.svg)

Turnkey CLI that chunk-writes chapters with OpenAI, following the **Universal AI Book-Writing Protocol**.

## Quick-start

```bash
git clone https://github.com/your-user/writer-bot.git
cd writer-bot
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="sk-..."   # or create .env
writer-bot write examples/chapter_overview.md
```

The bot appends prose to `chapter.md` until it hits 5 000 words, tagging the end with `### CHAPTER COMPLETE`.

## CI/CD

* **CI** – lint, type-check, tests on every push.  
* **Release** – tag `vX.Y.Z` → build & upload artefact.

MIT licensed.


# write Chapter 3
writer-bot write chapter03_overview.md --goal 6000

# once happy, move the resultant prose into book/chapters/
mv chapter.md book/chapters/chapter03.md

# regenerate its summary for future continuity
python -m writer_bot.summarise book/chapters/chapter03.md
