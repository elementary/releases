import datetime
import json
import os
import sys
from github import Github
from github.GithubException import UnknownObjectException as GithubUnknownObjectException

g = Github(os.environ['GITHUB_TOKEN'])

class NoReleasesFound(Exception):
  pass

class Repo:
  def __init__(self, repo):
    self.repo = repo

    try:
      self.release = self.repo.get_latest_release()
    except GithubUnknownObjectException:
      raise NoReleasesFound

    self.last_release_timestamp = self.release.created_at.timestamp()
    self.commits = self.repo.get_commits(since=self.release.created_at,sha='master')

org = g.get_organization('elementary')

repos = []
for repo in org.get_repos():
  print ('Processing {}...'.format(repo.name))
  try:
    repos.append(Repo(repo))
  # This catches repos that don't have releases and ignores them
  except NoReleasesFound:
    pass

repos = sorted(repos, key=lambda repo: repo.last_release_timestamp, reverse=True)

json_out = []
for repo in repos:
  release_date = datetime.datetime.fromtimestamp(repo.last_release_timestamp).strftime("%Y-%m-%d")
  commits_since = 0
  try:
    # Remove 1 commit, since the release commit itself seems to get included
    commits_since = repo.commits.totalCount - 1
    if commits_since < 0:
      commits_since = 0
  except GithubUnknownObjectException:
    pass

  json_out.append ({
    "repo": repo.repo.name,
    "version": repo.release.tag_name,
    "release_date": release_date,
    "commits_since": commits_since
  })
  
with open('_data/releases.json', 'w') as outfile:
    json.dump(json_out, outfile, indent=2)
