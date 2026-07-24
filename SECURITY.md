# Security Policy

## Supported versions

Security fixes target the latest release on the default branch.

## Reporting a vulnerability

Please do not open a public issue containing secrets, exploit details, or personal data. Contact the repository owner privately through the verified contact channels on the GitHub profile.

## Secret handling

- Never commit `.env` files or API keys.
- Restrict Google Cloud keys by API, application, and environment.
- Use GitHub Actions secrets for CI/CD.
- Rotate a secret immediately if it appears in Git history.
- Treat downloaded business contact data according to applicable privacy and marketing law.

## Deployment

The development server is not hardened for direct public exposure. Production deployments should add TLS, authentication, request quotas, audit logs, secure headers, and a reverse proxy.
