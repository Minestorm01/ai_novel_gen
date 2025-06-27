"""writer_bot CLI entry-point – generate chapters from an overview."""
from __future__ import annotations

import json
import textwrap
from pathlib import Path
from typing import List

import click
import openai
from rich import print as rprint

from .prompt import build_messages, parse_footer
from .memory import MemoryStore
from .logger import log


@click.command()
@click.option(
    "--out-md",
    type=click.Path(path_type=Path, writable=True),
    required=True,
    help="Markdown file to write / append the generated prose to.",
)
@click.option(
    "--words",
    default=5_000,
    show_default=True,
    help="Target total word-count for the chapter.",
)
@click.argument(
    "overview",
    type=click.Path(path_type=Path, exists=True),
)
@click.argument(
    "memory",
    # ⬇⬇⬇ allow a *new* memory file, so exists=False
    type=click.Path(path_type=Path, exists=False),
    required=False,
    default="project_memory.json",
)
def app(out_md: Path, words: int, overview: Path, memory: Path) -> None:
    """Generate a chapter from OVERVIEW, using MEMORY to track progress."""
    log.info("Starting writer-bot ")

    store = MemoryStore(memory)

    while store.data.get("words_written", 0) < words:
        remaining = words - store.data["words_written"]
        chunk_target = min(1_200, remaining)

        # ── build prompt
        messages: List[dict[str, str]] = build_messages(
            overview.read_text(encoding="utf-8"),
            store.last_paragraphs(),
            chunk_target,
        )

        # ── call OpenAI
        completion = (
            openai.chat.completions.create(
                model="gpt-4o-mini",
                max_tokens=int(chunk_target * 1.4),
                messages=messages,
            )
            .choices[0]
            .message.content
        )

        # ── split prose / footer
        footer_meta = parse_footer(completion)
        done_flag = footer_meta.get("done", False)
        prose = completion.split("```json")[0].rstrip()

        # ── write / append to markdown
        out_md.parent.mkdir(parents=True, exist_ok=True)
        mode = "a" if out_md.exists() else "w"
        out_md.write_text(prose + "\n\n", encoding="utf-8") if mode == "w" else out_md.open("a", encoding="utf-8").write(prose + "\n\n")

        # ── update memory
        words_in_chunk = len(prose.split())
        store.append_chunk(prose, words_in_chunk)
        log.info("Chunk saved – total words: %d", store.data["words_written"])

        # ── finish?
        if done_flag or store.data["words_written"] >= words:
            store.mark_complete()
            rprint("[bold green]### CHAPTER COMPLETE[/bold green]")
            break


if __name__ == "__main__":
    # Invoke click CLI
    app()  # type: ignore[misc]
