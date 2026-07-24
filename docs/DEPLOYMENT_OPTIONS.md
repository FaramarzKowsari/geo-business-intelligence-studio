# Deployment and distribution options

GeoBusiness Intelligence Studio supports three distinct audiences.

## Public browser users

Deploy the FastAPI service through `render.yaml`. Users receive a normal HTTPS URL and need no Python, terminal, or local installation.

## Windows desktop users

Run the **Build Windows Edition** GitHub Actions workflow or publish a GitHub Release. The workflow builds, smoke-tests, hashes, and uploads a self-contained EXE.

## Developers and private operators

Run the project with Python, Docker Compose, or the included Dockerfile. This mode is appropriate for customization, private data policies, dedicated geocoding endpoints, and production infrastructure.

## Static project website

GitHub Pages hosts the repository index, author biography, visual guidebook, DOI metadata, sitemap, and Search Console assets. GitHub Pages does not execute FastAPI; the public application URL should point to Render or another Python host.
