# transcript-chunker

**Transcript-aware, token-safe chunking for LLMs.**

Split long transcripts (e.g. meeting captions) into ChatGPT-friendly chunks without slicing through speaker turns or breaking token limits.

---

## ✨ Features

- ✅ Preserves **speaker turns** and **timestamps**
- ✅ Token-aware using `tiktoken`
- ✅ Output is ready for direct use in LLM chats
- ✅ Simple CLI and modular Python codebase
- 🚧 WIP: Better parsing for various formats, optional semantic chunking (`semchunk`), and CI/tests

---

## 📁 Example Output

Running the chunker generates files like:

```
runs/meeting_saved_closed_caption/
├── chunk_001.txt
├── chunk_002.txt
├── ...
```

Each file:
- Preserves speaker labels and timestamps
- Ends on complete turns when possible
- Stays under the token limit (`--max-tokens`), using fallbacks when needed

---

## ⚙️ Installation (Local Development)

```bash
git clone https://github.com/bw67-git/transcript-chunker.git
cd transcript-chunker

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -e .
```

---

## 🚀 Usage

```bash
transcript-chunker path/to/transcript.txt \
  --max-tokens 3000 \
  --output-dir runs/transcript_name
```

### Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `input_path` | Path to transcript `.txt` file | _required_ |
| `--max-tokens` | Max tokens per chunk (approximate) | `3000` |
| `--output-dir` | Directory for output chunks | `chunks/` |
| `--model` | Model name for token counting | `gpt-4` |

---

## 🧠 How It Works

### 1. Parsing (`parsers.py`)

- Detects lines like `[Speaker Name] HH:MM:SS`
- Groups subsequent lines into a `SpeakerTurn`
- Creates a list of speaker turn objects

### 2. Chunking (`chunker.py`)

- Uses `tiktoken` to count tokens per turn
- Accumulates turns under the `--max-tokens` limit
- If a turn is too large, splits it by line (fallback)

### 3. CLI (`cli.py`)

- Reads input file
- Parses turns
- Chunks turns
- Writes chunk files to output directory

---

## 🧪 Example

```bash
transcript-chunker examples/sample_transcript.txt \
  --max-tokens 3000 \
  --output-dir chunks

ls chunks
head chunks/chunk_001.txt
```

---

## 🙏 Acknowledgements

This tool is inspired by:

- [tiktoken](https://github.com/openai/tiktoken) – Tokenization utilities for OpenAI models
- [semchunk](https://github.com/normal-computing/semchunk) – Semantic + token-aware chunking
- LangChain's recursive text splitters

We don’t copy code from these libraries — we reference their ideas, use their APIs when helpful, and credit them accordingly.

---
