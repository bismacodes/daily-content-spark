---
name: daily-content-spark
description: Turns a rough everyday thought, note, or observation into a ready-to-post piece of content for LinkedIn, X, Instagram, Threads, or a newsletter, with a strong hook, one clear point, and a call to action. Use when the user says things like "turn this thought into a post", "generate content for today", "write a LinkedIn post about my morning", "help me post this idea", or "make this draft better".
---

# Daily Content Spark

Turn one small, real moment into a post that sounds like the user, not like a brand robot.

## Rules

- One post = one idea. If the thought has two ideas, pick the sharper one and mention the other as a follow-up.
- Never invent facts, numbers, quotes, names, or personal stories. Use only what the user gave you. Where a real detail is missing, leave a marker like `[add what you did with the time]`.
- Keep the user's own words for the most human line. Polish around it; do not replace it.
- No engagement bait ("Comment YES if..."), no fake vulnerability, no "In today's fast-paced world".
- Produce text only. Do not post, schedule, or send anything.

## Steps

1. **Collect the thought.** You need the raw thought and the platform. If the platform is missing, default to LinkedIn and say so. Ask at most one short question, and only if the thought itself is missing.
2. **Open the playbook** at `references/content-playbook.md` when the platform is X, Instagram, Threads, or a newsletter, when the user asks for a different tone, when you need a hook formula or CTA, or when the first draft feels flat. Skip it for a simple LinkedIn rewrite.
3. **Build a brief (optional, useful for a new post).** Run:

   ```bash
   python scripts/make_brief.py "their thought here" --platform linkedin --audience "busy parents"
   ```

   Use its angles, hook seeds, outline, and CTA options. Replace every placeholder with the user's real material.
4. **Draft the post.** Include: a first line that works alone (under 12 words if possible), one concrete detail from the user, the turn (what changed or what you noticed), one takeaway, and one call to action. Keep paragraphs to 1–3 short sentences. Follow the platform limit in the playbook.
5. **Check the draft.** Save it as `draft.md` in a scratch folder, then run:

   ```bash
   python scripts/check_draft.py draft.md --platform linkedin
   ```

   Fix every line starting with `FIX`. Read each `WARN` and fix the ones that make the post weaker, then run again. Exit code `1` means at least one `FIX` remains.
6. **Deliver:**
   - the final post in a code block
   - the character count
   - two alternative first lines
   - one short version (under 280 characters) for replies or X
   - one line naming the detail only the user can add

## Platform defaults

| Platform | Limit | Hashtags | Feel |
|---|---|---|---|
| LinkedIn | 3000 chars | 3–5 | one lesson, short lines, white space |
| X | 280 chars | 0–2 | one sharp thought, no wind-up |
| Instagram | 2200 chars | 3–8 | first line stops the scroll, caption tells the story |
| Threads | 500 chars | 0–3 | casual, like talking to a friend |
| Newsletter | 5000 chars | 0–3 | one story, one takeaway, one next step |

## Examples

**Example 1 — LinkedIn**

User: "generate content for today: I deleted 4 apps and got 2 hours back"

Agent action: run `make_brief.py`, draft, then `check_draft.py`. Final:

```text
I deleted four apps last week.

Not because they are bad. Because I opened them before I decided to.

The quiet part: I did not miss any of them. [add what you did with the two hours]

If one app opens before you decide, delete it for 7 days. Then tell me what you noticed.
```

**Example 2 — X**

User: "turn this into a tweet: my best ideas come when I am walking without headphones"

Agent action: skip the brief, write tight, run `check_draft.py --platform x`. Final:

```text
My best ideas do not arrive at a desk.

They arrive 20 minutes into a walk with no headphones.

Boredom is not wasted time. It is where the next idea finds you.
```

## Troubleshooting

- Script fails with "can't open file": run it from the repo root, or use the full path to the script.
- Script fails with "No module named": the scripts use only the Python standard library. Check `python --version`; Python 3.8+ is enough.
- User wants a platform not listed: use the closest row, keep it under 2000 characters, and skip hashtags.
