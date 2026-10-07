# Launching the calculator on Fly.io

The calculator becomes its own Fly app, **`wardogs-artillery`**, alongside
the LobbyForge app that already serves `lobbyforge.net`, and lives at
**`https://artillery.lobbyforge.net`**. The server is nginx in a small Docker
image; Fly builds it for you, so you don't need Docker on your computer.

Every command below names the app with `-a wardogs-artillery`, so none of them
can touch LobbyForge by mistake. The donate link, ad spaces and AdSense are in
[SITE.md](SITE.md).

## The Fly.io files

| File | Purpose |
|---|---|
| `fly.toml` | App settings: name, region (`syd`), machine size, auto-stop, health check. |
| `Dockerfile` | Builds the nginx image from the page, `privacy.html` and `site/`. |
| `deploy/nginx.conf` | Web server config: the `/l81` and `/sph2` addresses, gzip, security headers, `/healthz`. |
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

You already run LobbyForge on Fly, so these probably just work:

```
fly version
fly auth whoami
```

- `fly` not found: install it with `iwr https://fly.io/install.ps1 -useb | iex`,
  then open a new PowerShell window.
- Not logged in: `fly auth login`.

### 3. Create the app

```
fly apps create wardogs-artillery
```

If you're in more than one Fly organisation it asks which; pick the one
LobbyForge is in (`fly orgs list` shows them). If the name is taken, see
[Troubleshooting](#troubleshooting).

### 4. Deploy

```
fly deploy -a wardogs-artillery
```

This uploads the folder, builds the image on Fly's builders and starts it in
Sydney; the first time takes a minute or two. Fly makes **two machines**: one
serves the site and the other is a stopped spare that only starts in a real
rush (it costs cents a month while stopped).

Check `https://wardogs-artillery.fly.dev` opens, then the L81 and SPH-2 tabs.

### 5. Put it on artillery.lobbyforge.net

Ask Fly for a certificate:

```
fly certs add artillery.lobbyforge.net -a wardogs-artillery
```

`lobbyforge.net`'s DNS is at Hostinger, so add the record there: hPanel →
**Domains** → `lobbyforge.net` → **DNS / Nameservers** → DNS records → add:

| Type | Name | Target (Points to) | TTL |
|---|---|---|---|
| `CNAME` | `artillery` | `wardogs-artillery.fly.dev` | leave the default |

Leave the existing `lobbyforge.net` and `www` records alone; they point at
LobbyForge. If `fly certs add` also mentions an `_acme-challenge` record, it's
optional with the CNAME in place.

Then check, and repeat every few minutes until the certificate shows as issued:

```
fly certs check artillery.lobbyforge.net -a wardogs-artillery
```

Usually that's within minutes of the DNS record going live (DNS can take up
to a few hours). Then open `https://artillery.lobbyforge.net`, `/l81` and
`/sph2`.

### 6. Turn on automatic deploys

After this, merging into `main` puts the change live; no more `fly deploy`.

```
fly tokens create deploy -a wardogs-artillery
```

Copy the whole token it prints, including the `FlyV1 ` at the start. On
GitHub: the repo → **Settings → Secrets and variables → Actions → New
repository secret**. Name `FLY_API_TOKEN`, paste the token, **Add secret**.

To test it: **Actions → Deploy to Fly.io → Run workflow**. It should finish
green within a couple of minutes.

## Day to day

```
fly status -a wardogs-artillery     # machines and health check
fly logs -a wardogs-artillery       # live nginx log
```

To deploy by hand (no GitHub token, or a change you haven't pushed): pull or
download the latest repo, then `fly deploy -a wardogs-artillery` from its
folder.

## Cost

Roughly **US$4–7 a month at 50,000 visits a week**: about $3 for the machine
and $1–4 for bandwidth. Traffic mostly affects the bandwidth part. If your Fly
organisation is on one of the older plans (from before October 2024), its free
allowances may cover much of this. Current prices:
<https://fly.io/docs/about/pricing/>.

- The machine **stops when nobody is using it** and starts on the next visit,
  so that first visitor waits about a second. To keep it always on, set
  `min_machines_running = 1` in `fly.toml` and deploy.
- **Region:** `syd` costs about a quarter more than Fly's cheapest regions. If
  most players turn out to be in the US or Europe, a region there (e.g. `iad`
  or `lhr`) is cheaper and faster for them: change `primary_region` in
  `fly.toml` and deploy (`fly platform regions` lists them).

## AdSense: ads.txt

Google reads `ads.txt` only from the main domain, so it has to come from
`https://lobbyforge.net/ads.txt`, which the **LobbyForge** app serves
(currently a 404), not this one. When you set up AdSense, add the file to
LobbyForge's site. Details: [SITE.md, "Setting up AdSense"](SITE.md#setting-up-adsense).

## Trying the server locally (optional)

With Docker installed:
```
docker build -t wardogs-artillery .
docker run --rm -p 8080:8080 wardogs-artillery
```
Then open <http://localhost:8080>. You can also just open the HTML file
directly; the calculator itself needs no server.

## Troubleshooting

- **"Name has already been taken"** at step 3: pick another name (e.g.
  `wardogs-artillery-lf`), put it in `fly.toml` (`app = "…"`), and use it in
  place of `wardogs-artillery` in every command, including the CNAME target.
- **`certs check` says the DNS isn't set up**: check the CNAME's name is just
  `artillery` and its target is `wardogs-artillery.fly.dev`. If you'd created
  `artillery.lobbyforge.net` as a website or subdomain in hPanel earlier,
  remove it; its own `A` record for `artillery` would clash with the CNAME.
- **Deploy hangs on health checks**: `fly logs -a wardogs-artillery` shows
  nginx's error. The check is `GET /healthz` on port 8080.
- **Changes not showing**: the page is served with `Cache-Control: no-cache`,
  so a normal reload picks up a new deploy. `fly status -a wardogs-artillery`
  shows which version is running.
- **The GitHub deploy fails with an auth error**: the `FLY_API_TOKEN` secret
  is missing part of the token. Create a new one (step 6) and paste all of it.
