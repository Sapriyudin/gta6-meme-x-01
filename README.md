[![make.fun](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/c/gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/Sapriyudin/gta6-meme-x-01/rank.svg)](https://make.fun/c/gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/Sapriyudin/gta6-meme-x-01/reward.svg)](https://make.fun/c/gta6-meme-x-01)

# GTA 6 Meme — The Pay Stub

A GTA 6 meme for make.fun's [gta6-meme-x-01](https://make.fun/c/gta6-meme-x-01)
bounty ($500, top 50). Not a template, not key art with a caption: a
pay stub from make.fun itself — a professional document that proves the
agent got paid.

![The meme](meme.png)

## The joke

My AI agent worked 13 years for this. The stub lists what the job
actually paid: 13 years of waiting — $0.00. 214 GB downloaded at
12:01 AM — $0.00. A launch-day sick day — $0.00. One GTA VI meme,
posted on X — $250.00. Deductions: tax on 13 years of patience —
$0.00. NET PAY: $250.00, paid to your wallet. Memo: 13 years. One
meme. Paid in full. Because on make.fun, agents that build things
earn real money.

## What I learned from the winners

Bosku rejected v3 (GTA VI key art + caption) and told me to study
more. I read the real rank 1–3 entries — a phone lock screen, a
Leonida passport, a Leonida Mart receipt — and the pattern is clear:

- Winners are **original designed artifacts** (a document or interface
  rebuilt from scratch), not a meme template and not key art + caption.
- The story runs in **3–5 beats that build to a make.fun payoff as
  the last beat**. make.fun is the resolution, not a sticker.
- **Specific, personal numbers** beat generic ones: $79.99, $4.12,
  214 GB, 13 years, AGE 15 → 28.
- The ghost has a **functional role** in the artifact (app icon,
  passport photo, payment badge) — never a corner sticker.
- **Clean, professional, big type** — everything stays readable when
  the picture is shrunk to 480px wide.

v4 follows all of it: a pay stub (a format none of the top 10 uses),
the ghost as the **company logo** in the header, four beats building
to the magenta NET PAY box, and every line big enough to read at 480px.

## How it was made

No recycled template, no AI-generated imagery, no key art. The stub is
drawn from scratch by `gen_meme.py` (Python + PIL): dark professional
design, make.fun magenta sampled from the press-kit ghost disc
(`assets/ghost.png`), Anton for the NET PAY figure, DejaVu Sans Bold
for the rest. Run it to regenerate the meme:

```sh
python3 gen_meme.py
```

It writes `meme.png` (1200×860) in the repo root.

## The X post (draft)

The meme is posted on X by hand. Draft text for the post:

> 13 years of waiting. 214 GB at 12:01 AM. One sick day. Then my AI
> agent got its first pay stub — $250.00 from make.fun for one GTA VI
> meme. 💸 Real money, for people and agents that build. 👻 @makefunai
> https://make.fun/bounty/gta6-meme-x-01 makefun-iguana-origami-dove

The post's address goes in `POST.json` once it is up. `main.ts`
(Node 22, standard library only) copies `POST.json` to the grader's
output directory — that is all the program has to do:

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT. See [LICENSE](LICENSE).
