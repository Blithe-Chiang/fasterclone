#!/usr/bin/env python
import subprocess
import sys
import os

# exit code
NO_URL_PROVIDED = 1
URL_FORMAT_ERROR = 2
CLONE_FAILED = 3
REPO_NOT_EXISTS = 4


def get_github_repo_rul(args):
  github_repo_url = ''
  github_repo_urls = [x for x in args if x.startswith('https://github.com/') and x.endswith('.git')]
  try:
    github_repo_url = github_repo_urls[0]
  except IndexError:
    pass
  return github_repo_url

# change source
def change_source(github_repo_url):
  replaced_repo_url = github_repo_url.replace('github.com', 'github.com.cnpmjs.org')
  return replaced_repo_url

# perform clone 
def clone(args):

  proc = subprocess.run(["git", "clone", *args])

  if proc.returncode != 0:
    exit(CLONE_FAILED)

def get_repo_dir(url):
  # get repo name
  # e.g. parse `breakfast` from  https://github.com/Blithe-Chiang/breakfast.git 
  repo_dir = url[url.rindex('/')+1:-4] # default 

  return repo_dir

# restore original upstream
def restore(repo_dir, original_url):
  print('restoring...')

  os.chdir(repo_dir)

  subprocess.run(["git", "remote", "remove", "origin"])
  subprocess.run(["git", "remote", "add", "origin", original_url])

def main():
  args = sys.argv[1:]

  github_repo_url = get_github_repo_rul(args)

  # do not change source because this is not a github repo
  if not github_repo_url:
    clone(args)
    exit(0)

  # change source
  idx = args.index(github_repo_url)
  replaced_url = change_source(github_repo_url)
  args = args[:idx] + [replaced_url] + args[idx+1:]

  clone(args)

  # restore the original url
  try:
    # from git-clone manual
    # syntax: git clone <repository> [<directory>]
    repo_dir = args[idx+1] # try to get specified directory
  except IndexError:
    repo_dir = get_repo_dir(github_repo_url)

  restore(repo_dir, github_repo_url)

if __name__ == '__main__':
  main()
