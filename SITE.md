# Wardogs FireGrid site settings: pages, donations and ad spaces

These work the same wherever the site is hosted. It runs on Fly.io at
`wardogsfiregrid.com`: [DEPLOY.md](DEPLOY.md).

## Pages

| Address | Page |
|---|---|
| `/` | Tool chooser: the two calculators, an ad space and the support banner |
| `/l81` | L81 mortar calculator |
| `/sph2` | SPH-2 calculator with the low/high arc choice |
| `/guide` | How to use FireGrid (`guide.html`) |

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
    "side-1":    { adsenseSlot: "", sponsor: null },   // 300x250, right column, both tool pages
    "side-2":    { adsenseSlot: "", sponsor: null },   // 300x250, right column, L81 page
    "left-l81":  { adsenseSlot: "", sponsor: null },   // 320x100, left column, L81 page
    "left-sph2": { adsenseSlot: "", sponsor: null },   // 320x50,  left column, SPH-2 page
    "home-1":    { adsenseSlot: "", sponsor: null }    // 300x250, the tool chooser
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

| Space | Size | Where |
|---|---|---|
| `side-1` | 300×250 | Right column, L81 **and** SPH-2 pages (the most seen) |
| `side-2` | 300×250 | Right column, L81 page |
| `left-l81` | 320×100 | Left column under the buttons, L81 page |
| `left-sph2` | 320×50 | Left column under the buttons, SPH-2 page |
| `home-1` | 300×250 | Tool chooser (home page) |

All are standard ad sizes, so both sponsors and AdSense can fill them. Each
space fills in this order:

1. **A paid sponsor** booked for that space (see below).
2. **AdSense**, if `adsenseClient` and that space's `adsenseSlot` are both set.
3. **LobbyForge**, once per page, in the first unsold 300×250 space, or a
   banner space if those are all sold. Every other unsold space shows
   **"Advertise here"**, linking to `advertiseUrl`.

When every space on a page is sold, LobbyForge steps aside on the tool pages
(there's no room left) and becomes a one-line strip on the home page.

The banners were sized to the room the left column has on every desktop screen,
so the pages still fit without scrolling. With AdSense switched on, a window
smaller than 1280×720 can scroll slightly: Google's ads must stay full size
while the page shrinks to fit.

### Selling a space to a sponsor

Ask for an image **exactly the space's size** (300×250, 320×100 or 320×50; PNG,
JPG or GIF, ideally under 150 KB) and the link it should open. Host
the image with the site: put it in the repo's `site/sponsors/` folder, and it
is published next to the page as `sponsors/acme.png` (on Hostinger you can
also upload it to a `sponsors` folder with the File Manager). Then book the
space:

```js
"side-1": { adsenseSlot: "", sponsor: { image: "sponsors/acme.png", url: "https://acme.example/", alt: "Acme" } },
```

Set `sponsor` back to `null` when the booking ends.

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
5. Once approved, create a **Display ad** unit with a **Fixed size** matching
   each space you want AdSense in (300 × 250, 320 × 100 or 320 × 50), and put
   each unit's `data-ad-slot` number in that space's `adsenseSlot`. One unit
   per space gives you per-space reports; spaces of the same size can share
   one. A booked sponsor still takes priority over AdSense in its space.
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

## Getting found on Google and Bing

### Already in place

- **Titles and descriptions** on every page built around what players search
  for: *Wardogs artillery calculator*, *Wardogs mortar calculator*, *L81 mortar*,
  *SPH-2 artillery*, *mils*, *bearing*. (The old `<meta name="keywords">` tag is
  ignored by Google and Bing, so the words go in titles, headings and text
  instead.)
- **The guide**, `/guide` (`guide.html`): about 1,500 words on using
  FireGrid, which gives search engines (and AdSense's reviewers) real
  content to rank and approve.
- **`site/sitemap.xml`** listing all five pages, and **`site/robots.txt`**
  allowing everything and pointing at the sitemap.
- **Structured data**: the calculator is described as a free web app for
  WARDOGS, the guide as an article with an FAQ.
- **Canonical addresses**, so only `wardogsfiregrid.com/…` is indexed, never
  `www.` or the `fly.dev` address.
- **IndexNow**: every deploy from GitHub tells Bing (and through it DuckDuckGo
  and Yahoo, plus Yandex and others) that the pages changed. The key file is
  `site/92178755fb1399f77e4b3d27edccee6c.txt`.

### Do these as soon as https://wardogsfiregrid.com loads

1. **Google Search Console**, <https://search.google.com/search-console>:
   **Add property → Domain**, enter `wardogsfiregrid.com`, and copy the `TXT`
   record it gives you. In hPanel, **Domains → wardogsfiregrid.com → DNS /
   Nameservers**, add it (Type `TXT`, Name `@`, the value it gave you), then
   click **Verify**. The record can take a few minutes to be seen.
2. **Sitemaps** (left menu): submit `https://wardogsfiregrid.com/sitemap.xml`.
3. **URL inspection** (search bar at the top): enter each of these and click
   **Request indexing**:
   - `https://wardogsfiregrid.com/`
   - `https://wardogsfiregrid.com/l81`
   - `https://wardogsfiregrid.com/sph2`
   - `https://wardogsfiregrid.com/guide`

   This is the quickest way into Google; new pages usually show up within a
   few days.
4. **Bing Webmaster Tools**, <https://www.bing.com/webmasters>: sign in and
   choose **Import from Google Search Console**. It copies the site and
   sitemap across in one step.
5. **Links from players** do more for ranking than anything on the page:
   post FireGrid where Wardogs players are (Discord servers, Reddit, Steam
   community guides), ideally with words like "Wardogs artillery calculator"
   in or near the link.

When you change a page substantially, update its `<lastmod>` date in
`site/sitemap.xml`.

## LobbyForge

- The ad and strip link to `lobbyforge.net` with tracking tags,
  `?utm_source=wardogs-firegrid&utm_medium=calculator&utm_campaign=house_ad`
  (or `strip`). Visits from FireGrid show up under that source in
  LobbyForge's analytics.
- The ad's wording is in the page's `tplLobbyForge` template. It uses
  lobbyforge.net's own lines and its name-banner logo; if the logo can't load,
  the name shows as text.
