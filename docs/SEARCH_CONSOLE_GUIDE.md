# Google Search Console and Discoverability Guide

## Canonical property

Use this exact URL-prefix, including the final slash:

`https://faramarzkowsari.github.io/geo-business-intelligence-studio/`

A verified broader property for `https://faramarzkowsari.github.io/` also covers this subpath, but a separate URL-prefix property provides project-specific reporting.

## Sitemap

Submit:

`https://faramarzkowsari.github.io/geo-business-intelligence-studio/sitemap.xml`

## Request indexing

Use **URL Inspection -> Test live URL -> Request indexing** for:

- `https://faramarzkowsari.github.io/geo-business-intelligence-studio/`
- `https://faramarzkowsari.github.io/geo-business-intelligence-studio/guidebook/`
- `https://faramarzkowsari.github.io/geo-business-intelligence-studio/guidebook/inside-geobusiness-intelligence-studio.pdf`

The Render application is operational infrastructure, while GitHub Pages is the canonical crawlable project site. The landing page links to the live application, Windows release, guidebook, source repository, and Zenodo DOI.

## Files prepared for discovery

- `docs/index.html` - canonical landing page with SoftwareApplication structured data
- `docs/guidebook/index.html` - crawlable guidebook with Book structured data
- `docs/sitemap.xml` - public project URLs
- `docs/robots.txt` - crawl permission and sitemap location
- `docs/llms.txt` - machine-readable project description
- `docs/site.webmanifest` - application metadata
- Open Graph, Twitter Card, citation, canonical, DOI, and Schema.org metadata

## Backlinks

Link to the canonical project page from the GitHub profile README, personal website, ORCID, LinkedIn, Zenodo record, Google Scholar profile where appropriate, book pages, and technical articles. Use descriptive anchor text.

## Status checklist

- [ ] GitHub Pages workflow is green
- [ ] Project homepage opens publicly
- [ ] Guidebook HTML and PDF open publicly
- [ ] Sitemap is accepted by Search Console
- [ ] Homepage indexing is requested
- [ ] Guidebook indexing is requested
- [ ] Zenodo record links back to the repository
