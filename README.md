# One More Take Films — promo website

A single-page animated site for **One More Take Films** (wedding films, song shoots
& music videos, Punjab) and the painting work of **@daat_e_dio**.

Plain HTML, CSS and JavaScript. No build step, no framework, no dependencies.

```
demo/
├─ index.html              ← all the page content / text lives here
├─ assets/
│  ├─ css/style.css        ← all styling & animation
│  ├─ js/main.js           ← preloader, scroll reveal, filters, cursor
│  └─ img/                 ← drop photos here (see img/README.txt)
└─ README.md
```

## Run it

Double-click `index.html`. That's it — it opens in the browser and works offline
(except the Google Fonts, which need internet the first time).

## Photos

**Currently populated** with 9 stills pulled from the `manavgeet_gill` song shoot post
(`instagram.com/p/DbiNEzOoDmy/`). These are saved as real files in `assets/img/` —
**not** hotlinked to Instagram, because Instagram's CDN URLs are signed and expire
after a few weeks, which would silently break every image on the site.

**Source resolution was 640px** — Instagram's public ceiling. The 1080px URLs are
present in the page but unsigned (`urlgen_bucketless`), and re-signing them or
rewriting the size parameter both return 403.

They've been run through `scratchpad/enhance.py` (Pillow): JPEG-artifact cleanup,
Lanczos upscale capped at 2x, two-stage unsharp mask, and a gentle contrast/colour
lift. That measurably improves how they read on screen, but **it cannot restore
detail Instagram discarded**. Replacing `hero.jpg` with an original camera file is
still the single biggest visual upgrade available.

**The art section is still empty** — it needs a post URL from `@daat_e_dio`.

### Adding or replacing photos

Every image is a labelled slot. Save a file into `assets/img/` using the filename
listed in [`assets/img/README.txt`](assets/img/README.txt) and it shows up on the
next refresh. Missing files show a dashed placeholder rather than a broken image.

`setup-photos.html` (open it in a browser) takes a drag-and-dropped photo, crops it
to the right shape, compresses it, and hands it back already named correctly.

## Before it goes live — edit these

Open `index.html` and search for these. They're the only placeholder values:

| Find | Replace with |
|---|---|
| `+91XXXXXXXXXX` (in `wa.me/91XXXXXXXXXX`) | real WhatsApp number, digits only, with country code |
| `+91 XXXXX XXXXX` | the number as you want it displayed |
| `hello@onemoretakefilms.com` | a real email address (or delete that card) |

Both `<a>` tags are marked `data-edit` so they're easy to find.

Also worth a look:
- **Prices / packages** — there's no pricing section. If you want one, the
  `.svc` list in the Services section is the easiest block to copy.
- **Section copy** — the About and Process text is written to sound like a
  small two-person crew. Change the wording to whatever's actually true.

## Publish it

It's static files, so anything works and the free tiers are enough:

- **Netlify Drop** — drag the whole `demo` folder onto <https://app.netlify.com/drop>. Live in ~10 seconds, free URL.
- **GitHub Pages** — push the folder to a repo, Settings → Pages → deploy from branch.
- **Any hosting / cPanel** — upload the folder contents to `public_html`.

Then put the link in both Instagram bios.

## What's animated

- 3 · 2 · 1 · **ACTION** clapperboard preloader
- Letterbox bars opening on the hero, title lines rising line-by-line
- Film grain + vignette over the whole page
- Scrolling marquee of services
- Parallax on the hero background and the About photo frames
- Scroll-triggered fade-ups (staggered per group)
- Filterable work grid (All / Weddings / Song shoots / Portraits)
- Hover: image zoom & desaturate-to-colour, service rows fill in, art captions slide up
- Custom circle cursor on desktop

All of it respects `prefers-reduced-motion` — motion-sensitive visitors get the
static version automatically.

## Browser support

Any current Chrome, Edge, Firefox or Safari, desktop and mobile. Layout collapses
to a single column under 760px and the nav becomes a full-screen menu.
