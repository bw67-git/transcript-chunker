from __future__ import annotations

from typing import Iterable, List

import tiktoken
import semchunk

from .parsers import SpeakerTurn


def _get_encoding(model: str = "gpt-4") -> tiktoken.Encoding:
    """
    Get a tiktoken encoding for the given model, with a safe fallback.
    """
    try:
        return tiktoken.encoding_for_model(model)
    except KeyError:
        # Fallback used by many chat models
        return tiktoken.get_encoding("cl100k_base")


def _count_tokens(text: str, encoding: tiktoken.Encoding) -> int:
    return len(encoding.encode(text))


def render_turn(turn: SpeakerTurn) -> str:
    """
    Render a SpeakerTurn back into text, preserving speaker/timestamp if present.
    """
    prefix = ""
    if turn.speaker and turn.timestamp:
        prefix = f"[{turn.speaker}] {turn.timestamp} "
    elif turn.speaker:
        prefix = f"[{turn.speaker}] "

    return prefix + turn.text


def chunk_turns(
    turns: Iterable[SpeakerTurn],
    max_tokens: int = 3000,
    model: str = "gpt-4",
) -> List[str]:
    """
    Chunk a sequence of SpeakerTurn objects into text chunks that stay under
    max_tokens when encoded for the given model.

    Heuristics:
    - Never split inside a SpeakerTurn unless a single turn exceeds max_tokens.
    - If a single turn exceeds max_tokens, fall back to splitting that turn by lines.
    """
    encoding = _get_encoding(model)

    # First render all turns to text and count tokens per turn
    turn_texts = [render_turn(t) for t in turns]
    token_counts = [_count_tokens(txt, encoding) for txt in turn_texts]

    chunks: List[str] = []
    current_lines: List[str] = []
    current_tokens = 0

    def flush_current() -> None:
        nonlocal current_lines, current_tokens
        if current_lines:
            chunks.append("\n".join(current_lines))
            current_lines = []
            current_tokens = 0

    i = 0
    while i < len(turn_texts):
        text = turn_texts[i]
        n_tokens = token_counts[i]

        # If a single turn is larger than max_tokens, flush current and split this turn.
        if n_tokens > max_tokens:
            flush_current()

            # Use semchunk to split this single turn into semantically meaningful
            # sub-chunks, using the same token counter we already use.
            # semchunk.chunk() expects:
            #   - text
            #   - chunk_size (in tokens)
            #   - token_counter: callable(text) -> int
            subchunks = semchunk.chunk(
                text=text,
                chunk_size=max_tokens,
                token_counter=lambda s: _count_tokens(s, encoding),
            )

            # Append each semchunk-produced subchunk as its own chunk
            for sub in subchunks:
                if sub.strip():
                    chunks.append(sub)

            i += 1
            continue

        # If adding this turn would exceed max_tokens, flush current chunk first.
        if current_tokens + n_tokens > max_tokens and current_lines:
            flush_current()

        current_lines.append(text)
        current_tokens += n_tokens
        i += 1

    flush_current()
    return chunks

