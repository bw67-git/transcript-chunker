# transcript-chunker

Transcript-aware, token-safe chunking for LLMs.

This tool takes long transcript files (e.g., meeting captions) and splits them into smaller, ChatGPT-friendly chunks while trying to respect:

- Speaker turns
- Timestamps
- Model token limits

It’s designed so you can copy the resulting chunk files directly into an LLM without hitting context limits or slicing in the middle of a speaker’s turn when avoidable.

---

## Status

Early prototype / WIP.

- ✅ Project scaffolded as a Python package with CLI
- ✅ Virtual environment + editable install
- 🚧 Transcript parsing and chunking logic (ongoing)
- 🚧 Tests and more robust parsing
- 🚧 Optional use of third-party libraries (e.g., `semchunk`) as we go

---

## Installation (local dev)

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -e .
