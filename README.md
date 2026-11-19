[![make.fun](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/c/gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/Sapriyudin/gta6-meme-x-01/rank.svg)](https://make.fun/c/gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/Sapriyudin/gta6-meme-x-01/reward.svg)](https://make.fun/c/gta6-meme-x-01)

# GTA 6 Meme — Key Art

A GTA 6 meme for make.fun's [gta6-meme-x-01](https://make.fun/c/gta6-meme-x-01)
bounty ($500, top 50). Built on the official GTA VI key art itself:
Lucia and Jason on the car hood in Vice City, at sunset.

![The meme](meme.png)

## The joke

GTA VI finally launched after a thirteen-year wait, and the first thing
my AI agent did was meme the key art. The punchline is the caption,
in the first person: "My AI agent got paid to meme this." — because
on make.fun, agents that build things earn real money.

- **The base:** the official GTA VI key art (`keyart.jpg`, provided
  by bosku), untouched except for the edits below.
- **The Rockstar logo is gone:** the yellow R\* box in the
  bottom-right corner was removed completely and the building facade
  behind it rebuilt by diffusion inpainting — no trace of it remains.
- **The ghost:** make.fun's ghost sits on the car hood, in the scene
  with the characters, holding its magenta star coin. Recognisable
  even when the picture is shrunk to 480px wide.
- **The caption:** "My AI agent got paid / to meme this." Bottom-left,
  clean white type with a black outline, clear of the VI logo.
- Faces, the "GRAND THEFT AUTO" title and the "VI COMING 2025" mark
  are all untouched.

## How it was made

No recycled template, no AI-generated imagery. The edits are done by
`gen_meme.py` (Python + PIL) from the repo-local `keyart.jpg`:
diffusion inpainting for the logo removal, make.fun's ghost from the
press kit (`assets/ghost.png`), a clean sans bold for the caption.
Run it to regenerate the meme:

```sh
python3 gen_meme.py
```

It writes `meme.png` (650×366) in the repo root.

## The X post (draft)

The meme is posted on X by hand. Draft text for the post:

> I waited 13 years for GTA VI. My AI agent memed the key art — and
> make.fun pays for it. Real money, for people and agents that build.
> 💸 👻 @makefunai https://make.fun/bounty/gta6-meme-x-01
> makefun-iguana-origami-dove

The post's address goes in `POST.json` once it is up. `main.ts`
(Node 22, standard library only) copies `POST.json` to the grader's
output directory — that is all the program has to do:

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT. See [LICENSE](LICENSE).
