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

## Use

Open `Artillery & Mortar Calculator.html` in a browser. It's one
self-contained file with nothing to install.

## Host it

See [DEPLOY.md](DEPLOY.md) for launching it on Fly.io, adding your own domain,
automatic deploys from `main`, and setting up the ad space.

## Credits

Firing tables are community measurements from
[apollyon-sys/wardogs-calculator](https://github.com/apollyon-sys/wardogs-calculator)
(MIT). BULKHEAD publishes no official ballistics.
