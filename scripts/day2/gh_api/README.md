export GITHUB*TOKEN=ghp*... # con permessi admin:org, repo
export GITHUB_ORG=nome-organizzazione

`python github_setup.py`

## github action setup

Settings > Secrets and variables > Actions > New repository secret e aggiungi:

- GH_ADMIN_TOKEN: un GitHub personal access token (PAT) con i permessi:
  - admin:org
  - repo
  - read:user e write:org se vuoi gestire team/utenti
- GH_ORG: nome dell’organizzazione su GitHub (es. lab-corsi)
