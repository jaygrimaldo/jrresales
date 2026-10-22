# jrresales.com

J.R. Grimaldo's Real Estate website. Built as plain pages, hosted on GitHub Pages from the `docs` folder.

## How it works

- `build.py` holds everything that changes: brokerage name, contact info, page text (English and Spanish), listings, sold homes, reviews.
- `src/assets/` holds the headshot and any listing photos.
- `docs/` is the finished site. Do not edit it by hand; run `python3 build.py` and it is rebuilt.

## Common changes

- New listing: add it to `LISTINGS` in `build.py`, drop the photo in `src/assets/`, rebuild, commit, push.
- Listing sold: move it from `LISTINGS` to `SOLD`.
- Switch to HomeSmart branding: edit the `BRAND` block at the top of `build.py`, rebuild.
- Turn on a form service: set `formspree_id` in `SITE`.
