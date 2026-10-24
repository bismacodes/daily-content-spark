#!/usr/bin/env python3
"""Build a fill-in content brief from one everyday thought.

What it does:
    Turns a single thought into a ready-to-fill outline for one platform:
    angle options, hook seeds, structure, CTA options, and hashtag ideas.
    It never writes the final post and never invents facts.

Run it from the repo root:
    python scripts/make_brief.py "I deleted 4 apps and got 2 hours back"
    python scripts/make_brief.py "my best ideas come on walks" --platform x --audience "busy parents"

Options:
    --platform   linkedin (default), x, instagram, threads, or newsletter
    --audience   who the post is for (default: "people like you")

Output goes to the screen as Markdown. Nothing is saved or sent.
"""

import argparse
import re
import sys

PLATFORMS = {
    "linkedin": {
        "limit": 3000,
        "words": "120-220",
        "hashtags": "3-5",
        "note": "One lesson, short lines, white space between paragraphs.",
    },
    "x": {
        "limit": 280,
        "words": "40-60",
        "hashtags": "0-2",
        "note": "One sharp thought. No wind-up, no thread unless asked.",
    },
    "instagram": {
        "limit": 2200,
        "words": "80-150",
        "hashtags": "3-8",
        "note": "First line stops the scroll. The caption tells the story.",
    },
    "threads": {
        "limit": 500,
        "words": "60-100",
        "hashtags": "0-3",
        "note": "Casual, like talking to a friend. One idea only.",
    },
    "newsletter": {
        "limit": 5000,
        "words": "300-600",
        "hashtags": "0-3",
        "note": "One story, one takeaway, one next step.",
    },
}

STOPWORDS = {
    "about", "after", "again", "also", "and", "another", "any", "are", "because",
    "been", "before", "being", "but", "can", "could", "did", "does", "doing",
    "down", "each", "even", "every", "for", "from", "get", "got", "had", "has",
    "have", "here", "how", "into", "its", "just", "like", "made", "make", "many",
    "more", "most", "much", "must", "my", "never", "not", "now", "of", "off",
    "on", "once", "only", "or", "other", "our", "out", "over", "own", "really",
    "same", "she", "should", "since", "some", "still", "such", "than", "that",
    "the", "their", "them", "then", "there", "these", "they", "thing", "things",
    "this", "those", "through", "time", "too", "under", "until", "very", "was",
    "way", "were", "what", "when", "where", "which", "while", "who", "why",
    "will", "with", "would", "you", "your",
}

def keywords(text, limit=5):
    """Pick up to `limit` useful words, in the order they appear."""
    words = re.findall(r"[a-z][a-z'-]{3,}", text.lower())
    picked = []
    for word in words:
        word = word.strip("'-")
        if len(word) < 4 or word in STOPWORDS or word in picked:
            continue
        picked.append(word)
        if len(picked) == limit:
            break
    return picked


def shorten(text, limit=90):
    """Trim a thought on a word boundary so it fits in a template."""
    text = " ".join(text.split()).strip().rstrip(".!?")
    if len(text) <= limit:
        return text
    cut = text[:limit]
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    return cut + "..."


def hashtags(words):
    tags = []
    for word in words:
        tag = re.sub(r"[^a-z0-9]", "", word.lower())
        if tag and tag not in tags:
            tags.append(tag)
    return ["#" + tag for tag in tags]


def main():
    parser = argparse.ArgumentParser(
        description="Turn one everyday thought into a fill-in content brief."
    )
    parser.add_argument("thought", help="the raw thought or moment, in the user's words")
    parser.add_argument(
        "--platform",
        default="linkedin",
        choices=sorted(PLATFORMS),
        help="where the post will be published (default: linkedin)",
    )
    parser.add_argument(
        "--audience",
        default="people like you",
        help='who the post is for, e.g. "busy parents"',
    )
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    thought = " ".join(args.thought.split())
    if not thought:
        print("Nothing to work with. Pass the thought in quotes.")
        return 1

    info = PLATFORMS[args.platform]
    short = shorten(thought)
    short_lower = short[0].lower() + short[1:] if short else short
    words = keywords(thought)
    first = words[0] if words else "this"
    second = words[1] if len(words) > 1 else "the boring part"

    print("# Content brief")
    print()
    print(f"**Thought:** {thought}")
    print(f"**Platform:** {args.platform} (limit {info['limit']} characters, aim for {info['words']} words)")
    print(f"**Audience:** {args.audience}")
    print(f"**Platform feel:** {info['note']}")
    print()
    print("## The one point")
    print()
    print(f"Finish this sentence before you draft: \"The one thing I want {args.audience} to remember is ______.\"")
    print("If you cannot finish it in one line, the post is not ready.")
    print()
    print("## Pick one angle")
    print()
    print(f"1. **Lesson** - The lesson hiding in \"{short}\".")
    print(f"2. **Story** - What actually happened when {short_lower}.")
    print(f"3. **Practical** - One change worth copying: {short_lower}.")
    print()
    print("Choose one. Do not blend all three.")
    print()
    print("## Hook seeds (pick one, rewrite in your voice)")
    print()
    print(f'1. "{short}." Then a line break. Then the turn.')
    print(f"2. I almost did not talk about {first}.")
    print(f"3. Everyone talks about {first}. Nobody mentions {second}.")
    print(f"4. {short} - and here is the part I did not expect.")
    print(f"5. For {args.audience}: {short_lower}.")
    print()
    print("## Outline")
    print()
    print("1. **Hook** - 1-2 short lines. It must make sense on its own.")
    print("2. **Scene** - the real detail: where you were, what you did, who was there.")
    print("3. **Turn** - what changed, what you noticed, or what you got wrong.")
    print("4. **Takeaway** - one sentence the reader can use today.")
    print("5. **CTA** - one question or one small action. Not both.")
    print()
    print("## CTA options")
    print()
    print("- What is one small thing you would change this week? Tell me below.")
    print("- If this helped, save it and send it to one person who needs it.")
    print("- I am testing this for 7 days. Want the follow-up? Comment \"day 1\".")
    print("- Disagree? Reply with the strongest counter-argument.")
    print()
    print(f"## Hashtag ideas ({info['hashtags']})")
    print()
    tags = hashtags(words)
    if tags:
        print(" ".join(tags))
        print()
        print("Keep only the tags a reader would actually search for. Skip generic ones.")
    else:
        print("Not enough specific words in the thought. Add 3-5 tags a reader would search for.")
    print()
    print("## Fact check before drafting")
    print()
    print("- What exactly happened? Keep only details you can stand behind.")
    print("- Which number, name, or date can you confirm?")
    print("- Would the person involved be okay with this being public?")
    print()
    print("## Before posting")
    print()
    print("- Replace every `[square bracket]` with a real detail.")
    print("- Read it out loud. Cut the first line if it is only a wind-up.")
    print("- Remove any line that sounds like a slogan instead of a person.")
    print("- Check the character limit with `python scripts/check_draft.py draft.md --platform " + args.platform + "`.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
