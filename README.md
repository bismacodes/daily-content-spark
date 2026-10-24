# Daily Content Spark

Daily Content Spark is an Agent Skill that helps an AI agent turn one small, real thought from your day into a post you can publish. It writes a strong first line, keeps one clear point, and ends with a call to action, while using only the details you actually give it.

## What it does

Give the agent a rough thought ("I deleted four apps and got two hours back") and it builds a short brief, drafts a post for LinkedIn, X, Instagram, Threads, or a newsletter, and checks the draft for length, filler words, clichés, and missing calls to action. It never invents facts or personal stories; it leaves clear markers where you need to add a real detail.

## Example prompts

- "Generate content for today: I deleted four apps and got two hours back."
- "Turn this thought into a LinkedIn post: my best ideas come on walks without headphones."
- "Write a tweet about the one meeting rule I changed."
- "Make this draft better: [paste your draft]."
- "I want to post about [thought], but make it sound like me."

## What is in this repo

- `SKILL.md` — the instruction card the agent always reads. It explains the steps, the rules, and two short examples.
- `scripts/make_brief.py` — a small program that turns one thought into a fill-in brief: angles, hook ideas, an outline, calls to action, and hashtag ideas.
- `scripts/check_draft.py` — a small program that checks a draft before you post: character limit, first line, long sentences, filler words, clichés, hashtags, and whether there is a call to action.
- `references/content-playbook.md` — extra reading the agent opens only when it needs it: platform rules, hook formulas, post shapes, voice rules, a cut list, a CTA bank, and bad-to-good rewrites.
- `README.md` — this page.
- `LICENSE` — the MIT license.
- `.gitignore` — tells git which local files to skip.

The scripts use only the Python standard library. They need Python 3.8 or newer. Nothing is installed and nothing is sent anywhere.

## Install with one command

```bash
npx skills add YOUR_GITHUB_USERNAME/daily-content-spark
```

Replace `YOUR_GITHUB_USERNAME` with your real GitHub username. The repo name is `daily-content-spark`.

## Check it before installing

This lists the files the installer will use, without installing anything:

```bash
npx skills add YOUR_GITHUB_USERNAME/daily-content-spark --list
```

You should see `SKILL.md`, `scripts/make_brief.py`, `scripts/check_draft.py`, and `references/content-playbook.md`.

## Manual install for Claude Code

Clone the repo, then copy the whole folder (the repo root is the skill) into either place below.

Per project:

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/daily-content-spark.git
mkdir -p .claude/skills
cp -r daily-content-spark .claude/skills/daily-content-spark
```

Personal (available in every project):

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/daily-content-spark.git
mkdir -p ~/.claude/skills
cp -r daily-content-spark ~/.claude/skills/daily-content-spark
```

On Windows PowerShell, the copy step is:

```powershell
Copy-Item -Recurse -Force daily-content-spark "$HOME\.claude\skills\daily-content-spark"
```

Check that the file `.claude/skills/daily-content-spark/SKILL.md` exists. If it is nested one level deeper, the agent will not find it.

## Other agents

Cursor, OpenCode, Codex, and other Agent Skills compatible tools are supported through the same `npx skills add` command. The installer puts the skill where that agent looks for it. If your agent is not supported, use the manual install and copy the folder to the folder that agent documents.

## How to test that it works

1. Install the skill with the `npx` command above.
2. Open a new agent session in an empty folder.
3. Ask: "Generate content for today: I deleted four apps and got two hours back."
4. You should get a post with a short first line, one clear point, and a call to action.
5. Ask: "Check this draft" and paste it. The agent should run `scripts/check_draft.py` and report `FIX` or `WARN` lines.

If the agent does not react to the prompt, check that `SKILL.md` is directly inside the installed skill folder.

## Hacktoberfest

Built for the Hacktoberfest hackathon. Contributions are welcome: new platform rules, better examples, clearer wording, or fixes to the checker. Keep pull requests small and explain what you changed and why. Please do not add fake statistics or invented stories to the examples.

## License

MIT. See `LICENSE`.
