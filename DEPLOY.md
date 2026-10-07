# Launching Wardogs FireGrid on Fly.io

**Wardogs FireGrid** runs as its own Fly app, **`wardogs-firegrid`**, on its own
machines and its own domain, **`wardogsfiregrid.com`**. It shares nothing with
LobbyForge's servers. The
server is nginx in a small Docker image; Fly builds it for you, so you don't
need Docker on your computer.

Every command names the app with
`-a wardogs-firegrid`, so none of them can act on another app in your Fly
account. The donate link, ad spaces and AdSense are in [SITE.md](SITE.md).

## The Fly.io files

| File | Purpose |
|---|---|
| `fly.toml` | App settings: name, region (`syd`), machine size, auto-stop, health check. |
| `Dockerfile` | Builds the nginx image from the page, `privacy.html`, `img/` and `site/`. |
| `deploy/nginx.conf` | Web server config: the `/l81` and `/sph2` addresses, `www.` to bare domain redirect, gzip, security headers, `/healthz`. |
| `.github/workflows/fly-deploy.yml` | Redeploys automatically when `main` changes, once it has a token (step 6). |

## Launch

Run these in **PowerShell** on Windows (a macOS or Linux terminal takes the same
commands).

### 1. Get the repo

```
git clone https://github.com/Sylver1985/ArtillaryCalculator.git
cd ArtillaryCalculator
```

No Git? On GitHub: **Code → Download ZIP**, extract it, open the folder, and
right-click in it → **Open in Terminal**.

### 2. Check flyctl and your login

```
fly version
fly auth whoami
```

- `fly` not found: install it with `iwr https://fly.io/install.ps1 -useb | iex`,
  then open a new PowerShell window.
- Not logged in: `fly auth login`.

### 3. Create the app in its own organisation

A Fly organisation has its own bill and members. Giving the calculator one
keeps its costs and access separate from anything else on your Fly account:

```
fly orgs create wardogs-firegrid
fly orgs list
fly apps create wardogs-firegrid --org wardogs-firegrid
```

`fly orgs list` shows the new organisation's slug; if it isn't exactly
`wardogs-firegrid` (say the name was taken), use the slug it shows after
`--org`. The new organisation is billed on its own; if Fly asks for a payment
card for it, add one on the Fly dashboard under the organisation's **Billing**. (To use
an organisation you already have instead, skip `orgs create` and give
`--org` that one's name; `fly orgs list` shows them. It's still its own app
and machines either way.)

If the app name is taken, see [Troubleshooting](#troubleshooting).

### 4. Deploy

```
fly deploy -a wardogs-firegrid
```

This uploads the folder, builds the image on Fly's builders and starts it in
Sydney; the first time takes a minute or two. Fly makes **two machines**: one
serves the site and the other is a stopped spare that only starts in a real
rush (it costs cents a month while stopped).

Check `https://wardogs-firegrid.fly.dev` opens, then the L81 and SPH-2 tabs.

### 5. Put it on your domain

Ask Fly for certificates for the domain and its `www.`, then list the app's
addresses:

```
fly certs add wardogsfiregrid.com -a wardogs-firegrid
fly certs add www.wardogsfiregrid.com -a wardogs-firegrid
fly ips list -a wardogs-firegrid
```

`fly ips list` shows a `v4` address (shared) and a `v6` address.

The domain's DNS is at Hostinger. In hPanel: **Domains** → `wardogsfiregrid.com`
→ **DNS / Nameservers** → DNS records. Right now it holds Hostinger's parking
records, which point the domain at a Hostinger holding page:

- **Delete** the `A` record for `@` (it points at `2.57.91.91`).
- **Edit** the `CNAME` record for `www` (it points at `wardogsfiregrid.com`) to
  point at `wardogs-firegrid.fly.dev` instead.
- Leave any `MX`, `TXT` or other records alone; they're for email and
  verification.

Then add the two records for the bare domain, so the full set is:

| Type | Name | Target (Points to) | TTL |
|---|---|---|---|
| `A` | `@` | the `v4` address from `fly ips list` | leave the default |
| `AAAA` | `@` | the `v6` address from `fly ips list` | leave the default |
| `CNAME` | `www` | `wardogs-firegrid.fly.dev` | leave the default |

(`fly certs setup wardogsfiregrid.com -a wardogs-firegrid` prints the same
records if you want to double-check. An `_acme-challenge` record it may
mention is optional.)

Then check both, and repeat every few minutes until each certificate shows as
issued:

```
fly certs check wardogsfiregrid.com -a wardogs-firegrid
fly certs check www.wardogsfiregrid.com -a wardogs-firegrid
```

Usually that's within minutes of the DNS records going live (DNS can take up
to a few hours). Then open `https://wardogsfiregrid.com`, `/l81` and `/sph2`.
`www.wardogsfiregrid.com` redirects to the bare domain, so search engines see
one site.

### 6. Turn on automatic deploys

After this, merging into `main` puts the change live; no more `fly deploy`.

```
fly tokens create deploy -a wardogs-firegrid
```

Copy the whole token it prints, including the `FlyV1 ` at the start. On
GitHub: the repo → **Settings → Secrets and variables → Actions → New
repository secret**. Name `FLY_API_TOKEN`, paste the token, **Add secret**.

To test it: **Actions → Deploy to Fly.io → Run workflow**. It should finish
green within a couple of minutes.

## Day to day

```
fly status -a wardogs-firegrid     # machines and health check
fly logs -a wardogs-firegrid       # live nginx log
```

To deploy by hand (no GitHub token, or a change you haven't pushed): pull or
download the latest repo, then `fly deploy -a wardogs-firegrid` from its
folder.

## Cost

Roughly **US$4–7 a month at 50,000 visits a week**: about $3 for the machine
and $1–4 for bandwidth. Traffic mostly affects the bandwidth part. A new
organisation has no free allowance. Current prices:
<https://fly.io/docs/about/pricing/>.

- The machine **stops when nobody is using it** and starts on the next visit,
  so that first visitor waits about a second. To keep it always on, set
  `min_machines_running = 1` in `fly.toml` and deploy.
- **Region:** `syd` costs about a quarter more than Fly's cheapest regions. If
  most players turn out to be in the US or Europe, a region there (e.g. `iad`
  or `lhr`) is cheaper and faster for them: change `primary_region` in
  `fly.toml` and deploy (`fly platform regions` lists them).

## AdSense: ads.txt

With the site on its own domain, `ads.txt` lives in this repo: copy
`deploy/ads.txt.example` to `site/ads.txt`, put your publisher number in place
of the zeros, and deploy. It's then at `https://wardogsfiregrid.com/ads.txt`.
The rest of the AdSense setup: [SITE.md, "Setting up AdSense"](SITE.md#setting-up-adsense).

## Trying the server locally (optional)

With Docker installed:
```
docker build -t wardogs-firegrid .
docker run --rm -p 8080:8080 wardogs-firegrid
```
Then open <http://localhost:8080>. You can also just open the HTML file
directly; the calculator itself needs no server.

## Troubleshooting

- **"Name has already been taken"** at step 3: pick another app name (e.g.
  `wardogsfiregrid`), put it in `fly.toml` (`app = "…"`), and use it in
  place of `wardogs-firegrid` in every command, including the `www` CNAME
  target.
- **`certs check` says the DNS isn't set up**: compare the records with
  `fly ips list -a wardogs-firegrid`, and make sure the parking `A` record
  (`2.57.91.91`) is gone from Hostinger's DNS.
- **Deploy hangs on health checks**: `fly logs -a wardogs-firegrid` shows
  nginx's error. The check is `GET /healthz` on port 8080.
- **Changes not showing**: the page is served with `Cache-Control: no-cache`,
  so a normal reload picks up a new deploy. `fly status -a wardogs-firegrid`
  shows which version is running.
- **The GitHub deploy fails with an auth error**: the `FLY_API_TOKEN` secret
  is missing part of the token. Create a new one (step 6) and paste all of it.
