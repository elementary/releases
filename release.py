import datetime
import timeago
import json
import os
import sys
from github import Github
from github.GithubException import UnknownObjectException as GithubUnknownObjectException

g = Github(os.environ['GITHUB_TOKEN'], per_page=100)

class NoReleasesFound(Exception):
  pass

class Repo:
  def __init__(self, repo):
    self.repo = repo

    self.releases = self.repo.get_releases()
    if self.releases.totalCount == 0:
      raise NoReleasesFound

    self.last_release_timestamp = self.releases[0].created_at.timestamp()
    self.commits = self.repo.get_commits(since=self.releases[0].created_at,sha='master')

org = g.get_organization('elementary')

repos = []
for repo in org.get_repos():
  if repo.archived is False:
    print ('Processing {}...'.format(repo.name))
    try:
      repos.append(Repo(repo))
    # This catches repos that don't have releases and ignores them
    except NoReleasesFound:
      pass

repos = sorted(repos, key=lambda repo: repo.last_release_timestamp, reverse=True)

json_out = []
for repo in repos:
  new_commits = 0
  try:
    # Remove 1 commit, since the release commit itself seems to get included
    new_commits = repo.commits.totalCount - 1
    if new_commits < 0:
      new_commits = 0
  except GithubUnknownObjectException:
    pass

  releases = []
  for release in repo.releases:
    release_date = datetime.datetime.fromtimestamp(repo.last_release_timestamp).strftime("%Y-%m-%d")
    releases.append ({
      "version": release.tag_name,
      "release_date": release.created_at.isoformat(),
      "timeago": timeago.format(release.created_at, now),
      "title": release.title,
      "body": release.body,
      "href": release.html_url
    })

  json_out.append ({
    "name": repo.repo.name,
    "releases": releases,
    "new_commits": new_commits
  })
  
with open('_data/repos.json', 'w') as outfile:
    json.dump(json_out, outfile, indent=2)
