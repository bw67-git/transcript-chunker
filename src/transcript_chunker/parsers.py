from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional
import re

# Basic pattern for lines like:
# [Speaker Name] 13:31:37 Some text here...
SPEAKER_LINE_RE = re.compile(
    r"^\[(?P<speaker>.+?)\]\s+(?P<time>\d{2}:\d{2}:\d{2})\s*(?P<text>.*)$"
)


@dataclass
class SpeakerTurn:
    """A single speaker turn in the transcript."""

    speaker: Optional[str]
    timestamp: Optional[str]
    text: str  # raw text for this turn (possibly multi-line)


def parse_transcript(raw: str) -> List[SpeakerTurn]:
    """
    Parse a raw transcript into a list of SpeakerTurn objects.

    Heuristics:
    - If a line matches `[Speaker] HH:MM:SS text`, start a new turn.
    - Otherwise, treat the line as a continuation of the current turn.
    - Blank lines are preserved as line breaks inside the current turn.
    """
    turns: List[SpeakerTurn] = []
    current: Optional[SpeakerTurn] = None

    for line in raw.splitlines():
        stripped = line.strip()

        # Blank line: keep as a blank line in the current turn, if any.
        if stripped == "":
            if current is not None:
                current.text += "\n"
            continue

        match = SPEAKER_LINE_RE.match(line)
        if match:
            # Close out the previous turn
            if current is not None:
                turns.append(current)

            current = SpeakerTurn(
                speaker=match.group("speaker").strip(),
                timestamp=match.group("time"),
                text=match.group("text").strip(),
            )
        else:
            # Continuation of current turn, or free-floating text if no current
            if current is None:
                current = SpeakerTurn(
                    speaker=None,
                    timestamp=None,
                    text=line.rstrip("\n"),
                )
            else:
                current.text += "\n" + line.rstrip("\n")

    if current is not None:
        turns.append(current)

    return turns
