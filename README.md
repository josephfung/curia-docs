# Curia Documentation

Source for the [Curia docs](https://docs.meetcuria.com) — built with [Mintlify](https://mintlify.com).

Curia is a self-hosted, governance-first AI executive assistant. If you're here to read the docs rather than edit them, head to [docs.meetcuria.com](https://docs.meetcuria.com).

## Local preview

Install the Mintlify CLI if you haven't already:

```bash
npm i -g mintlify
```

Start the dev server from the repo root (where `docs.json` lives):

```bash
mintlify dev
```

Preview at `http://localhost:3000`. Hot-reload is on by default — changes to `.mdx` files and `docs.json` update immediately.

## Repository structure

```
curia-docs/
├── docs.json               # Site config: theme, nav, colors, fonts
├── style.css               # Custom CSS overrides
├── index.mdx               # Landing page
│
├── core-concepts/          # What Curia is and how it works
├── get-started/            # Installation, configuration, deployment, playbooks
├── agents/                 # How agents work, built-in agents, building custom ones
├── skills/                 # How skills work, built-in skills, building custom ones
├── channels/               # Email, Signal, CLI, HTTP — setup and custom channels
├── security/               # Autonomy engine, approval workflow, audit log, redaction
├── references/             # Configuration schema, API reference, memory schemas
│
└── assets/                 # Logo files and images
```

Content is written in [MDX](https://mdxjs.com/) with Mintlify components (`<Card>`, `<Note>`, `<Steps>`, etc.). The navigation structure is declared in `docs.json` — adding a new page requires both a file and an entry there.

## Making changes

All changes go through pull requests — pushes directly to `main` are not allowed.

**For small edits** (typos, wording, factual corrections): edit the file directly on GitHub and open a PR from the editor.

**For larger changes** (new pages, restructured sections):

1. Clone the repo and create a branch
2. Run `mintlify dev` to preview locally
3. Make your changes
4. Open a PR — Mintlify will generate a deploy preview automatically

See [CONTRIBUTING.md](CONTRIBUTING.md) for writing guidelines.

## Deployment

The Mintlify GitHub app handles deployment. Every merge to `main` triggers an automatic deploy to [docs.meetcuria.com](https://docs.meetcuria.com). No manual steps required.

If the deploy preview on a PR doesn't appear, check that the Mintlify GitHub app is installed under [Settings → Integrations](https://dashboard.mintlify.com/settings/organization/github-app).

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `mintlify dev` fails to start | Run `mintlify update` to get the latest CLI version |
| Page loads as 404 locally | Make sure the page is listed under `navigation` in `docs.json` |
| Changes not appearing after merge | Check the Mintlify dashboard for deploy status and error logs |
