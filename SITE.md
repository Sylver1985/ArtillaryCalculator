# Site settings: pages, donations and ad spaces

These work the same wherever the site is hosted. For putting it online see
[HOSTINGER.md](HOSTINGER.md) or [DEPLOY.md](DEPLOY.md) (Fly.io).

## Pages

| Address | Page |
|---|---|
| `/` | Tool chooser: the two calculators, an ad space and the support banner |
| `/l81` | L81 mortar calculator (two ad spaces, as the mortar has no tilt panel) |
| `/sph2` | SPH-2 calculator with the low/high arc choice (one ad space) |

All three are the same file, `index.html` on the server. The server sends
`/l81` and `/sph2` to it (`.htaccess` on Hostinger, `nginx.conf` on Fly.io)
and the script shows the right page. The links between pages are relative, so
the site also works in a folder, e.g. `lobbyforge.net/artillery/l81`. Opened
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
  utmSource:     "wardogs-artillery"
};
```

Edit, commit, and put the new version online: upload the new `index.html`
([HOSTINGER.md, "Updating the site"](HOSTINGER.md#updating-the-site)), or let
a merge to `main` do it if you've turned on automatic updates.

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
2. Sign up at <https://adsense.google.com> and add the **main domain** as the
   site, e.g. `lobbyforge.net` even if the calculator is at
   `artillery.lobbyforge.net`: AdSense takes main domains only, and an
   approved domain covers its subdomains and folders. Put your publisher ID
   (`ca-pub-…`) in `adsenseClient` and update the site. On its own this only
   loads the AdSense script so Google can verify the site; the spaces don't
   change yet.
3. **ads.txt** goes at the root of the **main domain**:
   `https://lobbyforge.net/ads.txt`. Google doesn't look for it on a
   subdomain. Copy the line from `deploy/ads.txt.example` with your publisher
   number (the `pub-…` part) in place of the zeros, and:
   - if the calculator *is* the main domain's site, save it as
     `site/ads.txt` in the repo and update the site;
   - otherwise add it to the `ads.txt` of whatever serves the main domain
     (on Hostinger: File Manager → that website's `public_html`).

   Check that `https://<main-domain>/ads.txt` shows it.
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

## LobbyForge

- The ad and strip link to `lobbyforge.net` with tracking tags,
  `?utm_source=wardogs-artillery&utm_medium=calculator&utm_campaign=house_ad`
  (or `strip`). Visits from the calculator show up under that source in
  LobbyForge's analytics.
- The ad's wording is in the page's `tplLobbyForge` template. It uses
  lobbyforge.net's own lines and its name-banner logo; if the logo can't load,
  the name shows as text.
