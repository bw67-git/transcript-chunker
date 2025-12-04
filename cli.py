# src/transcript_chunker/cli.py

import argparse

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

    args = parser.parse_args()

    # We'll implement this shortly
    print(
        f"[stub] Would chunk '{args.input_path}' into '{args.output_dir}' "
        f"with max_tokens={args.max_tokens}"
    )

