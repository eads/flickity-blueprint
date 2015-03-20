# -*- coding: utf-8 -*-
import getpass
import json
import os
import requests
import shutil

from clint.textui import colored, puts
from flask import Blueprint
from tarbell.hooks import register_hook

NAME = "Flickity gallery"

blueprint = Blueprint('base', __name__)


@register_hook('newproject')
def copy_files(site, git):
    """
    Copy css and js
    """
    blueprint_root = os.path.join(site.path, '_blueprint')

    puts("Copying css and javascript")

    os.mkdir(os.path.join(site.path, 'css'))
    src_css = os.path.join(blueprint_root, 'css/style.css')
    dst_css = os.path.join(site.path, 'css/style.css')
    shutil.copy2(src_css, dst_css)

    os.mkdir(os.path.join(site.path, 'js'))
    src_js = os.path.join(blueprint_root, 'js/app.js')
    dst_js = os.path.join(site.path, 'js/app.js')
    shutil.copy2(src_js, dst_js)

    puts(git.add('.'))
    puts(git.commit(m='Add css and js files'))


@register_hook('newproject')
def create_repo(site, git):
    """
    Ask to create a repository
    """
    create = raw_input("Want to create a Github repo for this project [Y/n]? ")
    if create and not create.lower() == "y":
        return puts("Not creating Github repo...")

    name = site.path.split('/')[-1]
    user = raw_input("What is your Github username? ")
    password = getpass.getpass("What is your Github password? ")
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    data = {'name': name, 'has_issues': True, 'has_wiki': True}
    requests.post('https://api.github.com/user/repos', auth=(user, password), headers=headers, data=json.dumps(data))
    puts("Created {0}".format(colored.green("https://github.com/{0}/{1}".format(user, name))))
    puts(git.remote.add("origin", "git@github.com:{0}/{1}.git".format(user, name)))
    puts(git.push("origin", "master"))
