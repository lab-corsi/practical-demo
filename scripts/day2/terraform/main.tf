terraform {
  required_providers {
    github = {
      source  = "integrations/github"
      version = "6.6.0"
    }
  }
}

provider "github" {
  token = var.github_token
  owner = var.github_org
}

variable "github_token" {
  type      = string
  sensitive = true
}

variable "github_org" {
  type = string
}

locals {
  # Repos CSV: name,private,team,permission
  repos_csv = file("${path.module}/repos.csv")
  repos     = csvdecode(local.repos_csv)

  # Teams CSV: team,users...
  teams_csv  = file("${path.module}/teams.csv")
  team_lines = csvdecode(local.teams_csv)

  # Crea una mappa che associa ogni team agli utenti separati in un array
  team_user_map = {
    for team in local.team_lines :
    team.team => [for user in split("|", team.users) : user]
  }
}

# Create all teams
resource "github_team" "teams" {
  for_each = local.team_user_map
  name     = each.key
  privacy  = "closed"
}

# Create all repos
resource "github_repository" "repos" {
  for_each = {
    for repo in local.repos :
    repo.name => {
      name       = repo.name
      private    = repo.private == "true"
      team_name  = repo.team
      permission = repo.permission
    }
  }

  name      = each.value.name
  private   = each.value.private
  auto_init = true
}

# Give teams access to repos
resource "github_team_repository" "access" {
  for_each = {
    for repo in local.repos :
    "${repo.team}-${repo.name}" => {
      repo       = repo.name
      team       = repo.team
      permission = repo.permission
    }
  }

  team_id    = github_team.teams[each.value.team].id
  repository = each.value.repo
  permission = each.value.permission
}

# Add users to teams
locals {
  # Appiattisco la mappa team → [users...] in una singola mappa flat_members:
  flat_team_members = merge([
    for team, users in local.team_user_map : {
      for user in users : "${team}-${user}" => {
        team = team
        user = user
      }
    }
  ]...)
}

resource "github_team_membership" "memberships" {
  for_each = local.flat_team_members

  team_id  = github_team.teams[each.value.team].id
  username = each.value.user
  role     = "member"
}
