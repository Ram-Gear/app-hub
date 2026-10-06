# Ram-Gear Shop Apps (launcher)

One landing page that links to every Ram-Gear Manufacturing Incorporated shop web app.

- `index.html` is the page: inline CSS and JS, no build step, no server, no CDNs or other external resources.
- `icons/` holds the app icons. The page loads them by relative path (`icons/<slug>.svg`, plus `icons/app-hub-64.png` / `app-hub-192.png` for the favicon and apple-touch-icon).
- `screenshot-desktop.png` (1280x800) and `screenshot-mobile.png` (390 wide, full page) are previews only.

## Opening it locally

1. Copy `index.html` and the `icons` folder together, keeping the folder structure, e.g. to
   `Z:\pricebook\PROGRAMS\Ram-Aps\`.
2. Double-click `index.html`. It opens in the default browser from disk (`file:///...`); no server is needed.
3. The page and icons work offline. The live app tiles link to the apps on GitHub Pages (https), so
   opening an app needs an internet connection.

`manifest.webmanifest` and `sw.js` are harmless on disk: the service worker is only registered when the
page is served over http(s), so a double-clicked `file://` copy behaves exactly as before.

Everything is relative-path only: no `fetch()` of local files, no ES modules, no external fonts or scripts.
The same folder also works unchanged on GitHub Pages.

## Installing on an Android phone (once published)

The hub is an installable Progressive Web App (`manifest.webmanifest` + `sw.js`). After it is on GitHub Pages
(planned URL: https://ram-gear.github.io/app-hub/):

1. Open the URL in **Chrome** on the phone.
2. Tap the **⋮** menu, then **Install app** (older Chrome: **Add to Home screen**). Chrome may also show an
   install banner on its own.
3. Confirm. "RG Shop Apps" appears on the home screen with the App Hub icon and opens full-screen
   (standalone, no address bar).

The launcher opens offline (the service worker caches the page, manifest and icons). Tapping a live app opens it
from GitHub Pages, which needs a connection; those apps are never cached or intercepted by the hub.

To uninstall: long-press the icon and choose Uninstall / Remove.

### PWA notes for maintainers

- `start_url` and `scope` are `./`, so the hub works under any project subpath. The manifest `id` is fixed at
  `/app-hub/` so it never collides with other Ram-Gear PWAs on the same `ram-gear.github.io` origin.
- `sw.js`: page loads are network-first (updates show up the next time it is opened online; cached copy when offline).
  Icons and the manifest use stale-while-revalidate. Requests outside the hub folder pass straight through.
- When you **add a new icon file** to the page, also add it to the `SHELL` list in `sw.js` and bump `VERSION`
  (e.g. `rg-hub-v2`) so phones pick it up offline. Editing only the `APPS` array in `index.html` needs no `sw.js` change.
- Icons are `purpose: "any"` only. Art's PNGs have transparent rounded corners, so they are not true full-bleed
  maskable icons; Android shows them inside a launcher-shaped plate. A full-bleed `app-hub-maskable-512.png` from Art
  could be added later.

## Adding or changing an app

Open `index.html` and find the `APPS` array near the top of the `<script>` block (marked `APP LIST`). Each app is one line:

```js
{ name: "My App", status: "live", icon: "icons/my-app.svg", url: "https://ram-gear.github.io/my-app/", desc: "One-line description." },
```

- `status: "live"`: clickable card that opens `url` in a new tab, with a green **Live** badge.
- `status: "soon"`: muted, non-clickable card with a yellow **Coming soon** badge (no `url` needed).
- `icon`: relative path to the tile icon (shown at 56 px; muted on Coming soon tiles). Leave it out for no icon.
- Optional `note` / `noteUrl`: small muted text (or link) under the description.

## Current apps

| App | Status | Icon | Link |
|---|---|---|---|
| QC Form | Live | `icons/qc-form.svg` | https://ram-gear.github.io/ramgear-app/ |
| Web Gear Calc | Live | `icons/web-gear-calc.svg` | https://ram-gear.github.io/wgc/ |
| RG Worm MOW | Live | `icons/rg-worm-mow.svg` | https://ram-gear.github.io/rg-worm-mow/ |
| Card File | Coming soon | `icons/cardfile.svg` | private repo, not published |
| Change Gear | Coming soon | `icons/change-gear.svg` | in progress |

## Icons

App icons were designed by Art and live in `icons/` (see `icons/README.md` for the full set, colors and
naming). The header logo and favicon use `app-hub`. Don't hand-edit them here; Art regenerates them with
`icons/build_icons.py`. The page palette (slate header, teal accents) follows the icons' teal
(`#2E7386` / `#245E6E` / `#9FD3E1`).

Files needed on the shop PC: `index.html`, `icons/app-hub.svg`, `icons/app-hub-64.png`,
`icons/app-hub-192.png`, `icons/qc-form.svg`, `icons/web-gear-calc.svg`, `icons/rg-worm-mow.svg`,
`icons/cardfile.svg`, `icons/change-gear.svg` (copying the whole `icons/` folder is fine too).
Optional there, harmless from disk (used only when served over https): `manifest.webmanifest`, `sw.js`,
`icons/app-hub-512.png`.
Dev-only: `README.md`, `screenshot-*.png`, `icons/build_icons.py`, `icons/preview-sheet.png`,
`icons/README.md`, `icons/__pycache__/`, and every icon PNG not listed above (the `-512` PNGs other than app-hub, and the `-192`/`-64` PNGs other than app-hub).

## Publishing

Not published yet. Hosting on GitHub Pages (for example, a new `Ram-Gear/app-hub` repo) waits for Gary's approval. For GitHub Pages, publish the whole folder (including `manifest.webmanifest`, `sw.js` and all of `icons/`).
