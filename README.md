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

See [DEPLOY.md](DEPLOY.md) for launching it on Fly.io, adding your own domain,
automatic deploys from `main`, the donate link, and selling or filling the ad
spaces.

## Credits

Firing tables are community measurements from
[apollyon-sys/wardogs-calculator](https://github.com/apollyon-sys/wardogs-calculator)
(MIT). BULKHEAD publishes no official ballistics.
