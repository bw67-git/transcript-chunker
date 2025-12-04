from __future__ import annotations

import argparse
from pathlib import Path

from .parsers import parse_transcript
from .chunker import chunk_turns


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Split long transcripts into ChatGPT-friendly chunks."
    )
    parser.add_argument("input_path", help="Path to the transcript .txt file")
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=3000,
        help="Approximate max tokens per chunk (default: 3000)",
    )
    parser.add_argument(
        "--output-dir",
        default="chunks",
        help="Directory to write chunk files into (default: chunks/)",
    )
    parser.add_argument(
        "--model",
        default="gpt-4",
        help="Model name used for token counting (default: gpt-4)",
    )

    args = parser.parse_args()

    input_path = Path(args.input_path)
    output_dir = Path(args.output_dir)

    if not input_path.exists():
        raise SystemExit(f"Input file does not exist: {input_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    raw = input_path.read_text(encoding="utf-8")
    turns = parse_transcript(raw)
    chunks = chunk_turns(
        turns,
        max_tokens=args.max_tokens,
        model=args.model,
    )

    if not chunks:
        print("No chunks were produced (input may have been empty).")
        return

    for i, chunk in enumerate(chunks, start=1):
        out_path = output_dir / f"chunk_{i:03}.txt"
        out_path.write_text(chunk, encoding="utf-8")

    print(f"Wrote {len(chunks)} chunks to {output_dir}")


