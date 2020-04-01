import datetime
import json
import os
from github import Github

g = Github(os.environ['GITHUB_TOKEN'])

class Repo:
  def __init__(self, repo, release, last_release_timestamp):
    self.repo = repo
    self.release = release
    self.last_release_timestamp = last_release_timestamp

org = g.get_organization('elementary')

repos = []
for repo in org.get_repos():
  release = None
  try:
    release = repo.get_latest_release()
  except:
    pass
    
  repos.append(Repo(repo, release, release.created_at.timestamp() if release else 0))

repos = filter(lambda repo: repo.last_release_timestamp != 0, repos)  
repos = sorted(repos, key=lambda repo: repo.last_release_timestamp, reverse=True)

json_out = []
for repo in repos:
  release_date = datetime.datetime.fromtimestamp(repo.last_release_timestamp).strftime("%Y-%m-%d")
  json_out.append ({
    "repo": repo.repo.name,
    "version": repo.release.tag_name,
    "release_date": release_date
  })

  print('{} ({}) released {}'.format (repo.repo.name, repo.release.tag_name, release_date))
  
with open('_data/releases.json', 'w') as outfile:
    json.dump(json_out, outfile)
