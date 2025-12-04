transcript-chunker

Transcript-aware, token-safe chunking for LLMs.

This tool takes long transcript files (e.g., meeting captions) and splits them into smaller, ChatGPT-friendly chunks while trying to respect:

Speaker turns

Timestamps

Model token limits

It’s designed so you can copy the resulting chunk files directly into an LLM without hitting context limits or slicing in the middle of a speaker’s turn when avoidable.

Status

Early prototype / WIP.

✅ Project scaffolded as a Python package with CLI

✅ Virtual environment + editable install

✅ Basic transcript parsing and token-aware chunking

🚧 More robust parsing for different transcript formats

🚧 Tests and CI

🚧 Optional integration with additional text chunking libraries

Installation (local development)

From the project root:

# Clone this repo (example)
git clone https://github.com/bw67-git/transcript-chunker.git
cd transcript-chunker

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip and install this package in editable mode
python -m pip install --upgrade pip
python -m pip install -e .


After this, the transcript-chunker command should be available inside the virtual environment.

Usage

Basic usage:

transcript-chunker path/to/transcript.txt --max-tokens 3000 --output-dir chunks

Arguments

input_path (positional, required)
Path to a plain-text transcript file.

--max-tokens (optional, default: 3000)
Approximate maximum tokens per chunk. This uses tiktoken with the specified model to estimate tokens and will avoid exceeding this limit when possible.

--output-dir (optional, default: chunks)
Directory where the chunk files will be written. The directory will be created if it doesn’t exist.

--model (optional, default: gpt-4)
Model name used for token counting via tiktoken. If the model is not recognized, a fallback encoding (cl100k_base) is used.

Output

The tool writes a series of files into the chosen output directory, for example:

chunks/
  chunk_001.txt
  chunk_002.txt
  chunk_003.txt
  ...


Each file contains a subset of the original transcript text. Speaker labels and timestamps are preserved; chunk boundaries are chosen to:

Accumulate complete speaker turns into each chunk

Stay under the token limit (--max-tokens) when possible

Fall back to line-based splitting if a single speaker turn is larger than the token budget

How it works (high level)
1. Parsing (parsers.py)

The transcript is parsed into a list of SpeakerTurn objects. The parser:

Detects lines of the form:

[Speaker Name] HH:MM:SS Some text...


Starts a new speaker turn when such a line is seen

Treats subsequent lines as a continuation of the current turn until the next speaker/timestamp line

Preserves blank lines inside the current turn

2. Chunking (chunker.py)

Chunking operates on these SpeakerTurn objects:

Each speaker turn is rendered back into text with its label and timestamp

tiktoken is used to estimate the token count for each turn

Turns are accumulated into a chunk until adding another would exceed max_tokens

A single oversized turn (larger than max_tokens on its own) is split by lines as a fallback

3. CLI (cli.py)

The command-line interface wires everything together:

Reads the input file

Parses it into turns

Chunks the turns according to the settings

Writes chunk files such as chunk_001.txt, chunk_002.txt, etc.

Example

From the project root, with .venv activated:

transcript-chunker examples/sample_transcript.txt --max-tokens 3000 --output-dir chunks

ls chunks
head -n 20 chunks/chunk_001.txt


You should see speaker-tagged transcript content in chunk_001.txt.

Acknowledgements

This project is inspired by and conceptually informed by:

tiktoken

– tokenization utilities for OpenAI models

semchunk

– semantic / token-aware text chunking

The idea behind LangChain’s text splitters, especially RecursiveCharacterTextSplitter

We are not copying large blocks of code from these projects; instead, we use them as references for design and, where appropriate, as dependencies for tokenization.
