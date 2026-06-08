# Blog figure generators

Source scripts for the diagrams in the post
[The Forgetting Wall in Video and World Models](../../content/posts/forgetting-wall/index.html).

These are **build-time tools** — Hugo does not publish the `tools/` directory.

## `gen_embed.py` (the one that matters)

Generates the three section-4 SVGs and writes them **directly** into the post's
published media folder, `static/posts/forgetting-wall/media/`:

- `fig41.svg` — 4.1 Look at less of the past (sliding window / attention sink / KV eviction)
- `fig42.svg` — 4.2 Summarize the past into a fixed state (linear attention)
- `fig43.svg` — 4.3 Keep everything, store it for less (block-wise KV quantization)

```sh
python3 tools/blog-figures/gen_embed.py
```

Each diagram carries a color legend; `fig43.svg` additionally labels the bottom
strip as the **KV cache**. Edit the palette/legend text at the top of the script
and re-run; the SVGs are overwritten in place — no manual copy step.

## `gen_fig41.py` / `gen_fig42.py` / `gen_fig43.py`

Older palette-exploration scripts that emit standalone `figNN_preview.html` files
(to the current working directory) for comparing color schemes. Not used by the
site; kept for reference. `gen_embed.py` supersedes them with the chosen "8a" palette.
