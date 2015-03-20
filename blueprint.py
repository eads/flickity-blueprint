# -*- coding: utf-8 -*-
import getpass
import json
import requests

from clint.textui import colored, puts
from flask import Blueprint
from tarbell.hooks import register_hook

NAME = "Basic Bootstrap 3 template"

blueprint = Blueprint('base', __name__)

@register_hook('newproject')
def create_repo(site, git):
    create = raw_input("Want to create a Github repo for this project [Y/n]? ")
    if create and not create.lower() == "y":
        return puts("Not creating Github repo...")

    name = site.path.split('/')[-1]
    user = raw_input("What is your Github username? ")
    password = getpass.getpass("What is your Github password? ")
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    data = {'name': name, 'has_issues': True, 'has_wiki': True}
    resp = requests.post('https://api.github.com/user/repos', auth=(user, password), headers=headers, data=json.dumps(data))
    puts("Created {0}".format(colored.green("https://github.com/{0}/{1}".format(user, name))))
    clone_url = resp.json().get("clone_url")
    puts(git.remote.add("origin", "git@github.com:{0}/{1}.git".format(user,name)))
    puts(git.push("origin", "master"))
