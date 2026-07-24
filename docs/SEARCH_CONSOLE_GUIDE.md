# Google Search Console and Discoverability Guide

## Canonical GitHub Pages property

Use this exact URL-prefix, including the final slash:

`https://faramarzkowsari.github.io/geo-business-intelligence-studio/`

If the broader property `https://faramarzkowsari.github.io/` is already verified in your Search Console account, it includes this repository subpath. You may still add a separate URL-prefix property when you want project-specific reports.

## Publish GitHub Pages

1. Open the repository on GitHub.
2. Go to **Settings → Pages**.
3. Under **Build and deployment**, choose **GitHub Actions** as the source.
4. Push the Pages workflow and site files.
5. Wait for the `Deploy GitHub Pages` workflow to finish successfully.
6. Open the project URL and confirm that the landing page and guidebook load.

## Search Console submission

1. Add or select the correct URL-prefix property.
2. Verify ownership if Google asks for it.
3. Open **Sitemaps**.
4. Submit `https://faramarzkowsari.github.io/geo-business-intelligence-studio/sitemap.xml`.
5. Use **URL Inspection** for the project homepage and guidebook.
6. Run the live test and request indexing.

## Files already prepared

- `docs/index.html` — canonical landing page with structured data
- `docs/guidebook/index.html` — crawlable guidebook
- `docs/sitemap.xml` — important public URLs
- `docs/robots.txt` — crawl permission and sitemap location
- `docs/llms.txt` — concise machine-readable project description
- `docs/site.webmanifest` — application metadata
- Open Graph, Twitter Card, canonical, citation, and Schema.org metadata

## Backlinks and internal links

Link to the canonical project page from your GitHub profile README, personal GitHub Pages site, ORCID, LinkedIn, relevant Zenodo records, book pages, and technical articles. Use descriptive anchor text rather than generic text such as “click here.”
