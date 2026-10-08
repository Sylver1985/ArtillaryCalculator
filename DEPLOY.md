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
| `fly.toml` | App settings: name, region (`iad`), machine size, auto-stop, health check. |
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

### 3. Create the app

Fly bills per **organisation**, and your account's existing one already has your
payment card, so create the app there. It's still its own app with its own
machines; only the bill is shared.

```
fly orgs list
fly apps create wardogs-firegrid --org personal
```

`personal` is your account's own organisation; if `fly orgs list` shows the
one you want under another name, use that. If the name is taken, see
[Troubleshooting](#troubleshooting).

**Want a separate bill?** Run `fly orgs create wardogs-firegrid`, add a payment
card at <https://fly.io/dashboard/wardogs-firegrid/billing> (Fly refuses to
create apps in a new organisation until it has one: "We need your payment
information to continue"), then use `--org wardogs-firegrid` above.

Run the commands in this guide one at a time and check each succeeds before
the next: a failed step makes the rest fail too.

### 4. Deploy

```
fly deploy -a wardogs-firegrid
```

This uploads the folder, builds the image on Fly's builders and starts it in
Ashburn, Virginia (`iad`), beside LobbyForge; the first time takes a minute or
two. Fly makes **two machines**, on different physical servers: one serves
the site, and the other is a stopped spare that only starts if the first goes
down or more than 200 requests arrive at once. A stopped machine costs only its
storage, under a cent a month, so the backup is nearly free. To run just one:
`fly scale count 1 -a wardogs-firegrid`.

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

### 7. Get it on Google and Bing

As soon as `https://wardogsfiregrid.com` loads, work through
[SITE.md, "Getting found on Google and Bing"](SITE.md#getting-found-on-google-and-bing):
Search Console, the sitemap, **Request indexing** for each page, and Bing.

## Day to day

```
fly status -a wardogs-firegrid     # machines and health check
fly logs -a wardogs-firegrid       # live nginx log
```

To deploy by hand (no GitHub token, or a change you haven't pushed): pull or
download the latest repo, then `fly deploy -a wardogs-firegrid` from its
folder.

## Cost

Roughly **US$3–5 a month at 50,000 visits a week**: about $2.20 for the
machine and $1–3 for bandwidth. Traffic mostly affects the bandwidth part. Current
prices: <https://fly.io/docs/about/pricing/>.

- **One machine always runs** (`min_machines_running = 1` in `fly.toml`), so
  nobody waits for a boot. Asleep, the site took about 4.5 s to answer the
  first visitor, slow enough to trouble search engine crawlers. To save the
  machine's running cost, set it to `0` and deploy: it then sleeps when idle
  and the first visit after a quiet spell waits for it to start.
- **Region:** `iad` (Ashburn, Virginia) is Fly's cheapest region and close to
  most US and European players. The page is one small download, so players
  further away barely notice. To move it, see "Moving to another region"
  below.

## Moving to another region

`primary_region` in `fly.toml` decides where new machines start, but
existing machines stay where they are. To move them, e.g. from Sydney to
Ashburn: set `primary_region`, then

```
fly deploy -a wardogs-firegrid
fly scale count 2 --region iad -a wardogs-firegrid
fly scale count 0 --region syd -a wardogs-firegrid
fly status -a wardogs-firegrid
```

The first `scale` starts the new machines (2: the running one and its spare;
use 1 if you've scaled down to one), the second removes the old ones, and
`fly status` should list only the new region. The site stays up
throughout, and its addresses and certificates don't change.

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
