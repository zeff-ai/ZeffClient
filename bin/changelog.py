#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""Create change discription files from git history."""
__author__ = """Lance Finn Helsten <lanhel@zeff.ai>"""
__copyright__ = """Copyright © 2019, Ziff, Inc. — All Rights Reserved"""
__license__ = """
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import sys
import getpass
from configparser import ConfigParser
import re
from pathlib import Path
from git import Repo
import requests


class GitHubAuth:
    def __init__(self):
        try:
            path = Path.home() / ".config" / "zeff" / "changelog.conf"
            with open(path, "rt") as fp:
                config = ConfigParser()
                config.read_file(fp)
            self.user = config["Server"]["username"]
            self.passwd = config["Server"]["token"]
        except FileNotFoundError:
            self.user = input("GitHub Username: ")
            self.passwd = getpass.getpass(prompt="GitHub Password: ")
            self.refresh()

    def refresh(self):
        self.otp = input("GitHub OTP:      ")

    @property
    def authn(self):
        return (self.user, self.passwd)

    @property
    def headers(self):
        try:
            return {"x-github-otp": self.otp}
        except AttributeError:
            return {}


def git_commits():
    """Generate a commit and github issue number."""
    path = Path.cwd()
    repo = Repo(path)
    assert not repo.bare
    lasttag = repo.tags[-1]
    for commit in repo.iter_commits(rev=f"{lasttag}..."):
        mo = re.match(r".+?\(#(?P<issue>\d+)\).*", commit.summary)
        if not mo:
            continue
        yield (commit, int(mo.groupdict()["issue"]))


def github_issue_labels(issue, githubauth):
    """Get the labels attached to a GitHub ``issue``."""
    url = f"https://api.github.com/repos/zeff.ai/ZeffClient/issues/{issue}/labels"
    authn = githubauth.authn
    headers = githubauth.headers
    resp = requests.get(url, auth=authn, headers=headers)
    if resp.status_code == 401:
        githubauth.refresh()
        authn = githubauth.authn
        headers = githubauth.headers
        resp = requests.get(url, auth=authn, headers=headers)
    json = resp.json()
    ret = [label["name"] for label in json]
    return ret


def news_type(commit, labels):
    """Return the news type of the commit (e.g. feature, bugfix, etc.)"""
    if "documentation" in labels:
        return "doc"
    elif "enhancement" in labels:
        return "feature"
    elif "bug" in labels:
        return "bugfix"
    else:
        return "misc"


def create_news_item(commit, issue, ntype):
    name = f"{issue}.{ntype}"
    try:
        path = Path.cwd() / "changelog" / name
        with open(path, "xt") as fp:
            print(commit.message, file=fp)
    except FileExistsError:
        print(f"Skipping news item {name}: it already exists.", file=sys.stderr)


def main():
    githubauth = GitHubAuth()
    for commit, issue in git_commits():
        labels = github_issue_labels(issue, githubauth)
        ntype = news_type(commit, labels)
        create_news_item(commit, issue, ntype)


if __name__ == "__main__":
    main()
