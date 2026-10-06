# Ram-Gear App Hub icons

A matching set of six launcher icons for the Ram-Gear App Hub. All of them share the same rounded-square
tile: a 512×512 viewBox, corner radius 112, and the same teal vertical gradient. Each has a flat white glyph
with a single light-teal accent.

## Files

| App | SVG (source) | PNGs (rendered from the SVG) |
|---|---|---|
| QC Form | `qc-form.svg` | `qc-form-512.png`, `qc-form-192.png`, `qc-form-64.png` |
| Web Gear Calc | `web-gear-calc.svg` | `web-gear-calc-512.png`, `web-gear-calc-192.png`, `web-gear-calc-64.png` |
| RG Worm MOW | `rg-worm-mow.svg` | `rg-worm-mow-512.png`, `rg-worm-mow-192.png`, `rg-worm-mow-64.png` |
| Cardfile | `cardfile.svg` | `cardfile-512.png`, `cardfile-192.png`, `cardfile-64.png` |
| Change Gear | `change-gear.svg` | `change-gear-512.png`, `change-gear-192.png`, `change-gear-64.png` |
| App Hub | `app-hub.svg` | `app-hub-512.png`, `app-hub-192.png`, `app-hub-64.png` |

Other files:

- `preview-sheet.png`: all six icons at 192 px with names, plus a 64 px row at actual size.
- `build_icons.py`: the generator. It writes every SVG, renders the PNGs with CairoSVG, and builds the
  preview sheet. Run `pip install cairosvg pillow`, then `python3 build_icons.py`. Gear outlines are
  computed (module-based stub teeth, evenly spaced). The Change Gear train is phased so its teeth
  actually mesh.

## Naming convention

`<slug>.svg` and `<slug>-<size>.png`. The size is the exact square pixel size (512, 192 or 64).
PNGs are RGBA, and the area outside the rounded tile is transparent. The slugs are `qc-form`,
`web-gear-calc`, `rg-worm-mow`, `cardfile`, `change-gear` and `app-hub`.

## Colors

These come from the Ram-Gear web app (`app.css` custom properties and the existing `icons/icon-*.png`).

| Use | Hex | Source |
|---|---|---|
| Tile gradient, top | `#2E7386` | `--navy`: primary button teal and the existing app icon background |
| Tile gradient, bottom | `#245E6E` | the same teal, about 20% darker (subtle depth only) |
| Glyph | `#FFFFFF` | white |
| Accent | `#9FD3E1` | `--link-on-dark`: also the underline in the app's "RG" icon |
| Preview sheet background | `#F3F5F6` | `--light` |
| Preview sheet text | `#2C2C2E` | `--header` charcoal |

Cut-outs (check marks, card lines, gear bores, separation outlines) are painted with the tile gradient
itself (`userSpaceOnUse`), so they match the background exactly.
