# Launching the calculator on Fly.io

The calculator is a single self-contained page, so the server is tiny: nginx in
a Docker image, serving it on Fly.io. Fly builds the image for you, so you don't
need Docker on your own computer.

## What's in the repo

| File | Purpose |
|---|---|
| `Artillery & Mortar Calculator.html` | The calculator. Served as the site's home page (`/`). |
| `privacy.html` | Privacy page, linked from the calculator. AdSense requires one. |
| `site/robots.txt` | Lets search engines index the site. |
| `deploy/nginx.conf` | Web server config: port 8080, gzip, security headers, `/healthz`. |
| `deploy/ads.txt.example` | Template for AdSense's `ads.txt` (see [Ads](#ads)). |
| `Dockerfile` | Builds the nginx image. |
| `fly.toml` | Fly.io app settings: name, region, health check, machine size. |
| `.github/workflows/fly-deploy.yml` | Redeploys automatically when `main` changes. |

## First launch

You'll need a Fly.io account; signing up asks for a payment card.

1. **Install `flyctl`**, Fly's command-line tool:
   - Windows (PowerShell): `iwr https://fly.io/install.ps1 -useb | iex`
   - macOS: `brew install flyctl`
   - Linux: `curl -L https://fly.io/install.sh | sh`

2. **Sign in** (or `fly auth signup` for a new account):
   ```
   fly auth login
   ```

3. **Pick the app's name.** Open `fly.toml` and change `app = "wardogs-artillery"`
   to a name of your own. It must be unique across Fly.io and becomes the
   address: `https://<name>.fly.dev`. Change `primary_region` too if you like;
   `syd` (Sydney) is set. `fly platform regions` lists the others.

4. **Create the app and deploy.** From the repo folder:
   ```
   fly apps create <name>
   fly deploy
   ```
   `fly deploy` uploads the folder, builds the image on Fly's builders and starts
   it. The first deploy takes a minute or two.

5. **Open it:**
   ```
   fly open
   ```

### Check it's healthy
```
fly status        # machines and health check
fly logs          # nginx access/error log, live
```

## Your own domain

The site works at `<name>.fly.dev` straight away. To use your own domain, for
example `artillery.lobbyforge.net`:

1. Request a certificate:
   ```
   fly certs add artillery.lobbyforge.net
   ```
2. Add the DNS record it asks for at your DNS provider. For a subdomain that is
   usually a `CNAME` pointing at `<name>.fly.dev`; for a bare domain, the `A`
   and `AAAA` records from `fly ips list`.
3. Check progress with `fly certs show artillery.lobbyforge.net`. HTTPS is
   live once it says the certificate is issued, usually within minutes.

**AdSense needs a domain you own**: it won't approve a `*.fly.dev` address.

## Updating the site

Manually: edit, commit, then `fly deploy` again.

### Automatic deploys

`.github/workflows/fly-deploy.yml` redeploys every time `main` changes, so merging
a pull request puts it live. It stays idle until GitHub has a Fly token:

1. Create a deploy token for the app:
   ```
   fly tokens create deploy -x 999999h
   ```
2. On GitHub: the repo → **Settings → Secrets and variables → Actions → New
   repository secret**. Name it `FLY_API_TOKEN` and paste the whole token,
   including the `FlyV1 ` at the start.

The next push to `main` deploys. You can also run it by hand from the
**Actions** tab ("Deploy to Fly.io" → **Run workflow**).

## Cost

`fly.toml` asks for the smallest machine (shared CPU, 256 MB), and it **stops
when nobody is using it** and starts on the next visit. That first visitor waits
about a second. A static site this size costs very little; current prices are
at <https://fly.io/docs/about/pricing/>. To keep it always warm, set
`min_machines_running = 1` in `fly.toml` and redeploy.

## Ads

The calculator has one 300×250 ad space: the right-hand column on desktop, and
after the results on phones. Its behaviour is set by `AD_CONFIG`, near the end
of the script in `Artillery & Mortar Calculator.html`:

```js
var AD_CONFIG = {
  adsenseClient: "",                       // publisher ID, "ca-pub-0000000000000000"
  adsenseSlot:   "",                       // the ad unit's data-ad-slot number
  lobbyforgeUrl: "https://lobbyforge.net/",
  utmSource:     "wardogs-artillery"
};
```

- **Both empty** (as shipped): the space shows the LobbyForge ad.
- **Publisher ID only:** loads the AdSense script so Google can verify the
  site. The space still shows LobbyForge.
- **Both filled:** the space shows AdSense, and LobbyForge moves to a one-line
  strip in the left column. It's always on the page exactly once.

### Setting up AdSense

1. Deploy on **your own domain** first (above).
2. Sign up at <https://adsense.google.com>, add the site, and put your
   publisher ID (`ca-pub-…`) in `adsenseClient`. Deploy.
3. **ads.txt:** copy `deploy/ads.txt.example` to `site/ads.txt`, replace the
   zeros with your publisher number (the `pub-…` part), and deploy. Check that
   `https://<your-domain>/ads.txt` shows it.
4. Ask AdSense to review the site. Approval can take days to a few weeks.
5. Once approved, create an ad unit: **Ads → By ad unit → Display ads**, size
   **Fixed, 300 × 250**. Copy its `data-ad-slot` number into `adsenseSlot` and
   deploy.
6. **Leave Auto ads off** for this site. Google would insert extra ads wherever
   it likes, pushing the one-screen layout off the screen.
7. **Consent for European visitors:** in AdSense, **Privacy & messaging →
   European regulations**, create and publish a consent message. Google shows
   it for you; nothing to change in the page.
8. Review `privacy.html` and adjust the wording or contact address if needed.
   It's linked from the calculator's footer and from AdSense's checks.

The ad is shown at its real 300×250 size regardless of the page's
fit-to-screen scaling. Scaling ads would break ad-network rules.

## LobbyForge

- The ad links to `lobbyforge.net` with tracking tags,
  `?utm_source=wardogs-artillery&utm_medium=calculator&utm_campaign=house_ad`
  (or `strip`). Visits from the calculator show up under that source in
  LobbyForge's analytics. Change `lobbyforgeUrl` or `utmSource` in `AD_CONFIG`
  if needed.
- The ad's text is in the page, in the `lf-card` link. It uses LobbyForge's own
  lines ("The Discord LFG bot you design yourself.", "Buttons, not
  commands.", "Free to start") and the logo from
  `https://lobbyforge.net/lf_name_banner.png`. If the logo can't load, the name
  shows as text.

## Trying the server locally (optional)

With Docker installed:
```
docker build -t wardogs-artillery .
docker run --rm -p 8080:8080 wardogs-artillery
```
Then open <http://localhost:8080>. You can also just open the HTML file
directly; the calculator itself needs no server.

## Troubleshooting

- **"Name has already been taken"**: pick another `app` name in `fly.toml`
  and rerun `fly apps create`.
- **Deploy hangs on health checks**: `fly logs` shows nginx's error. The
  check is `GET /healthz` on port 8080.
- **Changes not showing**: the page is served with `Cache-Control: no-cache`,
  so a normal reload picks up a new deploy. Check `fly status` shows the new
  version.
