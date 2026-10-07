#!/bin/sh
# Builds the site as plain files for ordinary web hosting (Hostinger and the
# like): dist/site/ and the same files zipped as dist/wardogs-site.zip.
# See HOSTINGER.md. Run from anywhere: sh deploy/build-site.sh
set -eu

cd "$(dirname "$0")/.."
out=dist/site

rm -rf "$out" dist/wardogs-site.zip
mkdir -p "$out"

# the page keeps its readable name in the repo; on the web it is the index
cp "Artillery & Mortar Calculator.html" "$out/index.html"
cp privacy.html "$out/privacy.html"
cp deploy/htaccess "$out/.htaccess"
cp -R img "$out/img"
# robots.txt, and ads.txt and sponsor images once you add them
cp -R site/. "$out/"

if command -v zip >/dev/null 2>&1; then
    (cd "$out" && zip -qrX ../wardogs-site.zip .)
else
    python3 -c 'import shutil, sys; shutil.make_archive("dist/wardogs-site", "zip", sys.argv[1])' "$out"
fi

echo "Built $out/ and dist/wardogs-site.zip:"
(cd "$out" && find . -type f | sed 's|^\./|  |' | sort)
