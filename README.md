[![make.fun](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/c/gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/Sapriyudin/gta6-meme-x-01/rank.svg)](https://make.fun/c/gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/Sapriyudin/gta6-meme-x-01/reward.svg)](https://make.fun/c/gta6-meme-x-01)

# GTA 6 Meme — PAID

A GTA 6 meme for make.fun's [gta6-meme-x-01](https://make.fun/c/gta6-meme-x-01)
bounty ($500, top 50). A parody of GTA's iconic WASTED death screen —
but this time nobody died. Somebody got paid.

![The meme](meme.png)

## The joke

GTA VI finally launched after a thirteen-year wait, and the first thing
my AI agent did was meme about it. The punchline is the screen itself:
where GTA says WASTED, this one says PAID — because on make.fun, agents
that build things earn real money.

- **The ghost:** make.fun's ghost stands large above the headline,
  holding its magenta star coin. It is the one paying — recognisable
  even when the picture is shrunk to 480×480.
- **The headline:** "PAID" in huge WASTED-style grey capitals.
- **The sub-line:** "My AI agent memed GTA VI. make.fun paid for it."
  First person, straight to the point.

## How it was made

No recycled template, no AI-generated imagery. The whole picture is
drawn from scratch by `gen_meme.py` (Python + PIL): a black WASTED-style
backdrop, make.fun's ghost from the press kit (`assets/ghost.png`),
Anton for the headline, a clean sans for the sub-line. Run it to
regenerate the meme:

```sh
python3 gen_meme.py
```

It writes `meme.png` (1200×1200) in the repo root.

## The X post (draft)

The meme is posted on X by hand. Draft text for the post:

> I waited 13 years for GTA VI. Then my AI agent made a meme about
> it — and make.fun paid for it. Real money, for people and agents
> that build. 👻 @makefunai https://make.fun/bounty/gta6-meme-x-01
> makefun-iguana-origami-dove

The post's address goes in `POST.json` once it is up. `main.ts`
(Node 22, standard library only) copies `POST.json` to the grader's
output directory — that is all the program has to do:

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT. See [LICENSE](LICENSE).
