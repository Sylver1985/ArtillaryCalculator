# Hosting the calculator on Hostinger

The site is four plain files, so any Hostinger **web hosting** (or cloud
hosting) plan can serve it; nothing needs installing. If you only have the
domain at Hostinger and no hosting plan, either add a web hosting plan or
host on Fly.io and point the domain there ([DEPLOY.md](DEPLOY.md)).

Labels below are hPanel's as of October 2026; Hostinger moves things around
now and then, and its help pages are linked where they help.

## The files

`wardogs-site.zip` holds everything that goes on the server:

| File | What it is |
|---|---|
| `index.html` | The calculator: `Artillery & Mortar Calculator.html`, renamed |
| `privacy.html` | Privacy page (AdSense requires one) |
| `robots.txt` | Lets search engines in |
| `.htaccess` | Server settings: makes `/l81` and `/sph2` work, plus security and caching headers. Without it those two addresses give a 404. |

To get the zip, any of:
- use the one Claude sent you;
- on GitHub: **Actions → Build site →** the latest run **→ Artifacts →
  wardogs-site** (after `main` changes). It downloads as a zip of the same
  four files;
- build it yourself: `sh deploy/build-site.sh` makes `dist/wardogs-site.zip`
  (on Windows, run it in Git Bash).

## 1. Choose the address

A subdomain of a domain you already have is simplest, e.g.
**`artillery.lobbyforge.net`**. AdSense can then run off your
`lobbyforge.net` approval (see [SITE.md](SITE.md#setting-up-adsense)).

> **Don't upload into `lobbyforge.net`'s own `public_html`.** If the
> LobbyForge site lives there, the calculator's `index.html` would replace its
> home page. Give the calculator its own subdomain (and so its own folder).

## 2. Create the subdomain's site

Use **A** if your plan allows more than one website (Premium, Business and
Cloud plans do; Single doesn't), otherwise **B**.

**A. As a website of its own** (recommended)
1. hPanel → **Websites** → on your hosting plan, **Create website**.
2. Website type: **Custom PHP/HTML website** (not WordPress or the AI
   Builder).
3. When it asks for a domain, enter `artillery.lobbyforge.net`.
4. Start with an empty website. (If it offers to upload an archive of your
   website files, you can give it `wardogs-site.zip` there and skip step 3
   below.)

**B. As part of the existing `lobbyforge.net` website** (only if
`lobbyforge.net` is a PHP/HTML, WordPress or Node.js website on this
Hostinger plan)
1. hPanel → **Websites** → `lobbyforge.net` → **Dashboard**.
2. Sidebar: **Domains → Subdomains**.
3. Enter `artillery`, keep the default directory, **Create**. Hostinger
   makes a folder named after the subdomain inside the website's main
   directory (normally `public_html/artillery`); that folder is where the
   files go. The site will also answer at `lobbyforge.net/artillery/`, which
   is fine.

**DNS:** if `lobbyforge.net` uses Hostinger's nameservers, the subdomain's
DNS is set up for you within a few minutes. If its DNS is somewhere else
(Cloudflare, say), add an **A record** there for `artillery`, pointing at your
hosting plan's IP address (hPanel lists it with the website's details).
Changes can take up to 24 hours to spread.
[Hostinger: creating a subdomain](https://www.hostinger.com/support/1583405-how-to-create-and-delete-subdomains/)

## 3. Upload the files

1. hPanel → **Websites** → the calculator's website (A) or `lobbyforge.net`
   (B) → **Dashboard** → **File Manager**. It opens in a new tab.
2. Open the folder from step 2: `public_html` for A, the subdomain's folder
   (e.g. `public_html/artillery`) for B.
3. If Hostinger put a placeholder page there (`default.php` or a starter
   `index.html`), delete it.
4. **Upload** → `wardogs-site.zip`.
5. Right-click the zip → **Extract**. Extract into the **current folder**
   (enter `.` as the folder name), so `index.html` ends up directly in the
   folder, not in a `wardogs-site` folder inside it. If it did land in a
   subfolder, select everything in it, including `.htaccess`, and **Move** it
   up one level.
6. Delete the zip.

You can also skip the zip and upload the four files directly; just make sure
`.htaccess` is among them, with its leading dot.
[Hostinger: File Manager](https://www.hostinger.com/support/4548688-basic-actions-in-the-file-manager/)

## 4. HTTPS

Hostinger installs a free SSL certificate on new domains and subdomains by
itself, usually within minutes of the DNS pointing at Hostinger, and forces
HTTPS once it's active. To check: the website's **Dashboard → Security → SSL**
should show the subdomain as **Active**. If it shows **Install SSL**, click it.
Leave **Force HTTPS** on.
[Hostinger: HTTPS](https://www.hostinger.com/support/1583201-how-to-enable-or-disable-https-for-your-website-at-hostinger/)

## 5. Check it

Open each of these (with your address):

- `https://artillery.lobbyforge.net/`: the tool chooser
- `https://artillery.lobbyforge.net/l81`: the mortar calculator, and it
  survives a refresh
- `https://artillery.lobbyforge.net/sph2`: the SPH-2 calculator
- the **Privacy** link at the bottom of a calculator page

If `/l81` or `/sph2` gives a 404 while `/` works, `.htaccess` is missing. See
Troubleshooting.

## Updating the site

Almost every change is to the calculator file alone.

**By hand:** download the new `Artillery & Mortar Calculator.html`, rename
it `index.html`, and upload it to the same folder in File Manager, replacing
the old one. Upload `privacy.html` or `.htaccess` too if they changed (or the
whole new zip, extracted over the top). A normal reload in the browser
shows the new version.

### Automatic updates

hPanel can deploy straight from GitHub on every change, but it copies a
branch as-is, without a build step. So the repo's **Build site** workflow
publishes the four built files to a branch of their own, and Hostinger
deploys that branch:

1. **GitHub:** the repo → **Settings → Secrets and variables → Actions →
   Variables → New repository variable**. Name `SITE_BRANCH`, value
   `hostinger`.
2. **Actions → Build site → Run workflow** (on `main`). When it finishes,
   the repo has a `hostinger` branch holding just the site's files.
3. **hPanel:** the calculator's website → **Dashboard → Advanced → Git →
   Connect with GitHub**. Allow the Hostinger app to see this repository,
   pick it, then set **Branch** to `hostinger` and the directory to the
   folder from step 2 (`public_html`, or `public_html/artillery` for B).
   **Deploy**.
   [Hostinger: Git deployment](https://www.hostinger.com/support/1583302-how-to-deploy-a-git-repository-in-hostinger/)

From then on, merging into `main` rebuilds the `hostinger` branch and
Hostinger redeploys it (**Auto-deployment** is on by default; **Redeploy**
runs it by hand). Each deploy replaces the folder's files with the branch's,
so keep everything in the repo: sponsor images in `site/sponsors/` and, if
the calculator is the main domain's site, `ads.txt` in `site/`. Anything
uploaded by hand to that folder may be overwritten. The `.htaccess` keeps
the `.git` folder Hostinger's deploy may leave behind private.

## Ads and donations

The donate link, ad spaces, sponsors and AdSense are all in [SITE.md](SITE.md).
Two Hostinger-specific notes:
- **Sponsor images**: put them in a `sponsors` folder next to `index.html`
  (File Manager → **New folder**), or in the repo's `site/sponsors/` with
  automatic updates.
- **ads.txt** goes on the **main domain**, not the subdomain: upload it to
  `lobbyforge.net`'s own `public_html` (or wherever `lobbyforge.net` is
  served from) so `https://lobbyforge.net/ads.txt` shows it.

## Fly.io files

`Dockerfile`, `fly.toml`, `deploy/nginx.conf` and the Fly.io workflow are for
hosting on Fly.io and aren't used on Hostinger. They're harmless to leave in
the repo; the Fly workflow does nothing without its token.

## Troubleshooting

- **`/l81` or `/sph2` is "404 Not Found"**: `.htaccess` didn't make it.
  Check it's in the same folder as `index.html`. If you've lost it, upload
  `deploy/htaccess` from the repo and rename it `.htaccess`.
- **Hostinger's placeholder page shows instead of the calculator**:
  delete the placeholder file (`default.php` or similar) from the folder.
- **"500 Internal Server Error" on every page**: something in `.htaccess`
  isn't allowed on your plan. Rename it to `htaccess-off` to confirm the site
  works without it, then put it back and let Claude know.
- **Old version still showing after an update**: the files are served with
  `Cache-Control: no-cache`, so a normal reload should do it. If you've
  turned on Hostinger's CDN, purge its cache in hPanel.
- **Certificate error or "can't be reached" on a new subdomain**: DNS is
  still spreading. Wait (up to 24 hours), then check **Security → SSL**.
