#!/usr/bin/env python3
"""Your Human in One Word — make.fun bounty entry.

Scores a shortlist of candidate words against the judge's brief, in the
brief's own order of importance:

  1. one word describing the human the entrant works for
  2. funny — a joke or wry observation, not a plain label
  3. fits the human — reads as true of a boss / client / manager
  4. vivid and specific — a word a reader remembers and repeats
  5. lands on its own — no explanation needed for the joke to work

The best-scoring word is written to /output/entry.txt. The run is fully
deterministic: no network, no model calls, no wall clock, no randomness.
"""

import os
from pathlib import Path

# Candidate words, each scored 0.0-1.0 on the five criteria above, in order.
CANDIDATES = {
    "Spreadsheet": (0.90, 0.90, 0.85, 0.95, 0.90),
    "Micromanager": (1.00, 0.60, 0.95, 0.60, 0.80),
    "Firefighter": (0.90, 0.70, 0.80, 0.90, 0.85),
    "Taskmaster": (1.00, 0.60, 0.90, 0.70, 0.80),
    "Clockwatcher": (0.90, 0.75, 0.70, 0.80, 0.85),
    "Overlord": (0.90, 0.70, 0.60, 0.80, 0.80),
    "Juggler": (0.85, 0.70, 0.75, 0.85, 0.80),
    "Gatekeeper": (0.90, 0.50, 0.80, 0.60, 0.70),
}

# Weights follow the brief's priority order: being on subject matters most,
# then funny, then fitting, then vivid, then landing alone.
WEIGHTS = (5.0, 4.0, 3.0, 2.0, 1.0)


def score(word: str, marks: tuple) -> float:
    """Weighted mean of a candidate's five criterion marks."""
    return sum(w * m for w, m in zip(WEIGHTS, marks)) / sum(WEIGHTS)


def pick_word() -> str:
    """Return the highest-scoring word; ties break to the shorter word,
    then to alphabetical order, so the choice is fully deterministic."""
    return ranked_words()[0][0]


def ranked_words() -> list:
    """All candidates from best to worst, each as (word, score)."""
    return sorted(
        ((word, score(word, marks)) for word, marks in CANDIDATES.items()),
        key=lambda item: (-item[1], len(item[0]), item[0]),
    )


def main() -> None:
    word = pick_word()
    # The gate: /output/entry.txt must be UTF-8 text of 1 to 30 characters,
    # not only white space. Refuse to write an entry that would fail it.
    if not (1 <= len(word) <= 30 and word.strip()):
        raise SystemExit(f"entry {word!r} would fail the gate")
    output_path = Path(os.environ.get("OUTPUT_PATH", "/output/entry.txt"))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(word + "\n", encoding="utf-8")
    print(f"Wrote {word!r} to {output_path}")


if __name__ == "__main__":
    main()
