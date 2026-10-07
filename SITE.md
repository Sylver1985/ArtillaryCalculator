# Wardogs FireGrid site settings: pages, donations and ad spaces

These work the same wherever the site is hosted. It runs on Fly.io at
`wardogsfiregrid.com`: [DEPLOY.md](DEPLOY.md).

## Pages

| Address | Page |
|---|---|
| `/` | Tool chooser: the two calculators, an ad space and the support banner |
| `/l81` | L81 mortar calculator (two ad spaces, as the mortar has no tilt panel) |
| `/sph2` | SPH-2 calculator with the low/high arc choice (one ad space) |

All three are the same file, `index.html` on the server. The server sends
`/l81` and `/sph2` to it (`.htaccess` on Hostinger, `nginx.conf` on Fly.io)
and the script shows the right page. The links between pages are relative, so
the site also works in a folder, e.g. `example.com/firegrid/l81`. Opened
straight from disk, the tabs use `#l81` and `#sph2` instead. Each page
remembers its own gun position, weapon and mode.

## Changing the settings

Everything you'd change is in `SITE_CONFIG`, near the end of the script in
`Artillery & Mortar Calculator.html`:

```js
var SITE_CONFIG = {
  donateUrl: "",                 // your PayPal link for the Support button
  adsenseClient: "",             // AdSense publisher ID, "ca-pub-…"
  slots: {
    "side-1": { adsenseSlot: "", sponsor: null },   // right column, both tool pages
    "side-2": { adsenseSlot: "", sponsor: null },   // right column, L81 page only
    "home-1": { adsenseSlot: "", sponsor: null }    // the tool chooser
  },
  advertiseUrl:  "mailto:support@lobbyforge.net?subject=…",
  lobbyforgeUrl: "https://lobbyforge.net/",
  utmSource:     "wardogs-firegrid"
};
```

Edit, commit, and put the new version online. On Fly.io a merge to `main`
deploys it once automatic deploys are on ([DEPLOY.md](DEPLOY.md), step 6),
or run `fly deploy -a wardogs-firegrid`. On Hostinger, upload the new
`index.html` ([HOSTINGER.md](HOSTINGER.md#updating-the-site)).

## Donations

The **Support ♥** tab, on every page, opens a short note saying the tools are
free but hosting isn't, with a **Donate with PayPal** button. Until `donateUrl`
is set it shows "Donations open here soon".

To set it up, use either:
- a **PayPal.Me** link, from <https://www.paypal.com/paypalme/>, such as
  `https://paypal.me/YourName`; or
- a **PayPal Donate button**: on PayPal, **Pay & get paid → Accept donations**
  (or <https://www.paypal.com/donate/buttons>), create a button, and copy its
  link, `https://www.paypal.com/donate/?hosted_button_id=…`.

Put the link in `donateUrl`.

## Ad spaces

Every space is a standard 300×250. Each fills in this order:

1. **A paid sponsor** booked for that space (see below).
2. **AdSense**, if `adsenseClient` and that space's `adsenseSlot` are both set.
3. **LobbyForge**, for the first unfilled space on the page. After that:
   **"Advertise here"**, linking to `advertiseUrl`.

LobbyForge always appears exactly once per page: when paid ads fill every space,
it moves to a one-line strip.

### Selling a space to a sponsor

Ask for a **300×250 image** (PNG, JPG or GIF) and the link it should open. Host
the image with the site: put it in the repo's `site/sponsors/` folder, and it
is published next to the page as `sponsors/acme.png` (on Hostinger you can
also upload it to a `sponsors` folder with the File Manager). Then book the
space:

```js
"side-1": { adsenseSlot: "", sponsor: { image: "sponsors/acme.png", url: "https://acme.example/", alt: "Acme" } },
```

An image on the sponsor's own site works too: give its full `https://`
address. Sponsor links are marked `rel="sponsored"`, which Google requires for
paid links. "Advertise here" sends people to `advertiseUrl`, which is your
support email by default. Point it at a page or form if you have one.

### Setting up AdSense

1. Put the site on **a domain you own** (AdSense won't take `*.fly.dev` or
   a host's temporary address).
2. Sign up at <https://adsense.google.com> and add `wardogsfiregrid.com` as
   the site (AdSense takes main domains only; an approved domain covers its
   subdomains and folders). Put your publisher ID
   (`ca-pub-…`) in `adsenseClient` and update the site. On its own this only
   loads the AdSense script so Google can verify the site; the spaces don't
   change yet.
3. **ads.txt**: copy `deploy/ads.txt.example` to `site/ads.txt`, put your
   publisher number (the `pub-…` part) in place of the zeros, and deploy.
   Check that `https://wardogsfiregrid.com/ads.txt` shows it. (Google reads
   ads.txt only from a main domain, never a subdomain, so if the site ever
   moves to a subdomain, the file has to go on the main domain instead.)
4. Ask AdSense to review the site. Approval can take days to a few weeks.
5. Once approved, create a **Display ad** unit, size **Fixed, 300 × 250**, for
   each space you want AdSense in, and put each unit's `data-ad-slot` number in
   that space's `adsenseSlot`. One unit per space gives you per-space reports;
   reusing one number everywhere also works. A booked sponsor still takes
   priority over AdSense in its space.
6. **Leave Auto ads off** for this site. Google would insert extra ads wherever
   it likes, pushing the one-screen layout off the screen.
7. **Consent for European visitors:** in AdSense, **Privacy & messaging →
   European regulations**, create and publish a consent message. Google shows
   it for you; nothing to change in the page.
8. Review `privacy.html` and adjust the wording or contact address if needed.

AdSense ads are shown at their real 300×250 size regardless of the page's
fit-to-screen scaling, as ad-network rules require. A space a page doesn't show
(the second one on the SPH-2 page) never requests an ad.

## Logo and icons

The master logo is `design/firegrid-logo.webp`. `deploy/make-icons.py` turns it
into everything in `img/`: the home-page badge, the top-bar mark, the tab
icons (`favicon.ico`, plus PNGs for Android and iPhone home screens) and
`og-image.jpg`, the picture Discord, Reddit and Steam show when someone
shares a link. To change the logo, replace the master and run:

```
python3 deploy/make-icons.py
```

(It needs Pillow: `pip install pillow`.) Then commit `img/` and deploy.

## Getting found on Google

`site/sitemap.xml` lists the three pages and `site/robots.txt` points search
engines at it. To get indexed sooner and see what people search for:

1. Go to <https://search.google.com/search-console>, **Add property →
   Domain**, and enter `wardogsfiregrid.com`.
2. It gives you a `TXT` record. Add it in Hostinger's DNS (**Domains →
   wardogsfiregrid.com → DNS / Nameservers**), then click **Verify**. It can
   take a few minutes for the record to be seen.
3. **Sitemaps** → submit `https://wardogsfiregrid.com/sitemap.xml`.

Links from where players are (Discord servers, Reddit, Steam guides) do more
for ranking than anything on the page itself.

## LobbyForge

- The ad and strip link to `lobbyforge.net` with tracking tags,
  `?utm_source=wardogs-firegrid&utm_medium=calculator&utm_campaign=house_ad`
  (or `strip`). Visits from FireGrid show up under that source in
  LobbyForge's analytics.
- The ad's wording is in the page's `tplLobbyForge` template. It uses
  lobbyforge.net's own lines and its name-banner logo; if the logo can't load,
  the name shows as text.
