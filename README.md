# Wardogs Artillery & Mortar Calculator

Range, bearing and mils for the Wardogs **L81 mortar** and **SPH-2** (low and
high arc), from map coordinates.

- **Simple** mode: flat-ground solution straight from the firing tables.
- **Advanced** mode adds:
  - target height (ASL) correction for the SPH-2
  - gun-platform tilt, set from a gauge that matches the in-game one
  - **adjust from impact**: log where a round landed and the next round is
    corrected from it
- Fits on one screen from a 1366×768 laptop to 4K, and works on phones.
- A page for each gun, `/l81` and `/sph2`, with a tool chooser at `/`.
- Free to use: ad spaces for sponsors or AdSense, and a **Support** tab for
  PayPal donations towards hosting.

## Use

Open `Artillery & Mortar Calculator.html` in a browser. It's one
self-contained file with nothing to install; the L81 and SPH-2 tabs switch
pages (`#l81`, `#sph2` when opened from disk).

## Host it

- **Hostinger** or similar web hosting: [HOSTINGER.md](HOSTINGER.md). Upload
  four files; optional automatic updates from GitHub.
- **Fly.io**: [DEPLOY.md](DEPLOY.md). A small nginx container.
- Donate link, ad spaces, sponsors and AdSense, on either host:
  [SITE.md](SITE.md).

| File | Purpose |
|---|---|
| `Artillery & Mortar Calculator.html` | The whole site in one file: tool chooser, L81 page and SPH-2 page. Served as `index.html`. |
| `privacy.html` | Privacy page, linked from the calculator. |
| `site/` | Extra files served next to the page: `robots.txt`, and later `ads.txt` and sponsor images. |
| `deploy/htaccess` | Server settings for Hostinger (Apache/LiteSpeed), installed as `.htaccess`. |
| `deploy/build-site.sh` | Builds the files for upload: `dist/site/` and `dist/wardogs-site.zip`. |
| `.github/workflows/build-site.yml` | On each change to `main`: builds that zip as a download, and optionally publishes it to a branch for Hostinger to deploy. |
| `deploy/nginx.conf`, `Dockerfile`, `fly.toml`, `.github/workflows/fly-deploy.yml` | Fly.io hosting. |
| `deploy/ads.txt.example` | Template for AdSense's `ads.txt`. |

## Credits

Firing tables are community measurements from
[apollyon-sys/wardogs-calculator](https://github.com/apollyon-sys/wardogs-calculator)
(MIT). BULKHEAD publishes no official ballistics.
