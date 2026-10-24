#!/usr/bin/env python3
"""Check a draft post for the things that usually make it flop.

What it does:
    Reads one draft file and checks the character limit, hook length,
    sentence length, filler words, cliches, paragraph size, hashtags,
    and whether there is a call to action. Prints FIX, WARN, and OK lines.

Run it from the repo root:
    python scripts/check_draft.py draft.md --platform linkedin
    python scripts/check_draft.py draft.md --platform x

The platform defaults to linkedin. Exit code 0 means nothing is blocking.
Exit code 1 means at least one FIX line still needs work.
"""

import argparse
import re
import sys

PLATFORMS = {
    "linkedin": {"limit": 3000, "min_tags": 3, "max_tags": 5},
    "x": {"limit": 280, "min_tags": 0, "max_tags": 2},
    "instagram": {"limit": 2200, "min_tags": 3, "max_tags": 8},
    "threads": {"limit": 500, "min_tags": 0, "max_tags": 3},
    "newsletter": {"limit": 5000, "min_tags": 0, "max_tags": 3},
}

# Words that usually add nothing. Cut unless removing them changes the meaning.
FILLER = [
    "very", "really", "just", "actually", "basically", "literally", "simply",
    "quite", "in order to", "at the end of the day", "it is important to note",
    "needless to say", "a lot of", "kind of", "sort of",
]

# Phrases that make a post sound like every other post.
CLICHES = [
    "in today's fast-paced world", "game-changer", "game changer", "dive into",
    "unlock", "leverage", "delve", "tapestry", "testament to", "elevate",
    "synergy", "revolutionize", "transformative", "in today's world",
]

THROAT_CLEARING = [
    "in this post", "let me tell you", "i want to talk about",
    "today i want to", "here is a quick thought", "i am going to share",
]

CTA_WORDS = [
    "comment", "reply", "tell me", "share", "send this", "save", "follow",
    "dm me", "try it", "what do you think", "which one", "your turn",
    "let me know", "link in",
]

BAIT = [
    "comment yes", "comment \"yes\"", "tag a friend", "agree?", "who else?",
    "like if you agree", "share if you agree",
]


def word_count(text):
    return len(re.findall(r"[A-Za-z0-9']+", text))


def find_phrases(text, phrases):
    """Return {phrase: count} for matches, case-insensitive."""
    found = {}
    lowered = text.lower()
    for phrase in phrases:
        pattern = r"(?<!\w)" + re.escape(phrase) + r"(?!\w)"
        count = len(re.findall(pattern, lowered))
        if count:
            found[phrase] = count
    return found


def main():
    parser = argparse.ArgumentParser(
        description="Check a draft post before the user publishes it."
    )
    parser.add_argument("file", help="path to the draft file (.md or .txt)")
    parser.add_argument(
        "--platform",
        default="linkedin",
        choices=sorted(PLATFORMS),
        help="where the post will be published (default: linkedin)",
    )
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    try:
        with open(args.file, "r", encoding="utf-8-sig") as handle:
            raw = handle.read()
    except OSError as error:
        print(f"FIX   Could not open {args.file}: {error}")
        return 1

    text = raw.replace("\r\n", "\n").replace("\r", "\n").strip()
    info = PLATFORMS[args.platform]
    limit = info["limit"]

    fixes = []
    warnings = []
    passes = []

    if not text:
        print("FIX   The draft is empty.")
        return 1

    # Remove a leading Markdown heading marker so the hook is measured cleanly.
    hook = ""
    for line in text.split("\n"):
        line = line.strip()
        if line:
            hook = re.sub(r"^#{1,6}\s*", "", line)
            break

    chars = len(text)
    words = word_count(text)

    if chars > limit:
        fixes.append(
            f"Too long: {chars} characters. Cut {chars - limit} to fit {args.platform} ({limit} max)."
        )
    elif chars > int(limit * 0.9):
        warnings.append(
            f"Close to the limit: {chars} of {limit} characters. Cut anything that is not pulling weight."
        )
    else:
        passes.append(f"{chars} of {limit} characters.")

    # Hook
    hook_words = word_count(hook)
    if len(hook) > 120:
        warnings.append(
            f"Hook is {len(hook)} characters. Aim for under 120 so the first line reads as one thought."
        )
    elif hook_words > 25:
        warnings.append(
            f"Hook is {hook_words} words. Shorten it so the reader gets the point at a glance."
        )
    else:
        passes.append(f"Hook is {len(hook)} characters and {hook_words} words.")

    throat = find_phrases(hook, THROAT_CLEARING)
    if throat:
        warnings.append(
            f"Hook starts with a wind-up ({', '.join(throat)}). Cut it and start with the point."
        )

    # Sentences
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    sentence_word_counts = [word_count(s) for s in sentences]
    long_ones = [(s, n) for s, n in zip(sentences, sentence_word_counts) if n > 45]
    if long_ones:
        sample = long_ones[0][0]
        if len(sample) > 60:
            sample = sample[:57].rstrip() + "..."
        warnings.append(
            f"{len(long_ones)} sentence(s) over 45 words. First one: \"{sample}\" Split it."
        )
    if sentence_word_counts:
        average = sum(sentence_word_counts) / len(sentence_word_counts)
        if average > 22:
            warnings.append(f"Average sentence is {average:.0f} words. Aim for 15 or fewer.")
        else:
            passes.append(f"Average sentence is {average:.0f} words.")

    # Paragraphs
    paragraphs = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    heavy = [p for p in paragraphs if word_count(p) > 70]
    if heavy:
        warnings.append(
            f"{len(heavy)} paragraph(s) over 70 words. Break them up; white space helps people read."
        )
    else:
        passes.append(f"{len(paragraphs)} paragraphs, none too heavy.")

    # Filler and cliches
    filler = find_phrases(text, FILLER)
    if filler:
        listed = ", ".join(f'"{k}" x{v}' if v > 1 else f'"{k}"' for k, v in filler.items())
        warnings.append(f"Filler words: {listed}. Cut unless they change the meaning.")

    cliches = find_phrases(text, CLICHES)
    if cliches:
        listed = ", ".join(f'"{k}"' for k in cliches)
        warnings.append(f"Cliches: {listed}. Say the thing in your own words.")
    if not filler and not cliches:
        passes.append("No filler words or cliches found.")

    # Hashtags
    tags = re.findall(r"(?<!\w)#([A-Za-z0-9_]+)", text)
    if len(tags) > info["max_tags"]:
        warnings.append(
            f"{len(tags)} hashtags. {args.platform} works best with {info['max_tags']} or fewer."
        )
    elif len(tags) < info["min_tags"]:
        warnings.append(
            f"{len(tags)} hashtags. Add specific ones; {args.platform} usually wants {info['min_tags']} or more."
        )
    else:
        passes.append(f"{len(tags)} hashtags, in range for {args.platform}.")

    # Call to action
    lowered = text.lower().replace("’", "'")
    has_cta = "?" in text or any(word in lowered for word in CTA_WORDS)
    if has_cta:
        passes.append("Has a call to action.")
    else:
        warnings.append("No clear call to action. Add one question or one small action.")

    bait = find_phrases(lowered, BAIT)
    if bait:
        warnings.append(
            "Possible engagement bait (" + ", ".join(f'"{k}"' for k in bait) + "). Ask a real question instead."
        )

    # Report
    print(f"Platform: {args.platform} (limit {limit} characters)")
    print(f"Characters: {chars}")
    print(f"Words: {words}")
    print(f"Paragraphs: {len(paragraphs)}")
    print()

    for message in fixes:
        print(f"FIX   {message}")
    for message in warnings:
        print(f"WARN  {message}")
    for message in passes:
        print(f"OK    {message}")

    print()
    if fixes:
        print(f"Result: {len(fixes)} fix(es), {len(warnings)} warning(s). Fix the FIX lines first.")
        return 1
    print(f"Result: ready to review. {len(warnings)} warning(s), no blockers.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
