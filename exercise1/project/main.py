from functools import lru_cache

import requests
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/members_only")
@login_required
def post_select():
    posts_by_id = _get_posts_by_id()
    return render_template("posts.html", posts_by_id=posts_by_id, post=None)


@main.route("/members_only/<post_id>")
@login_required
def post_detail(post_id):
    posts_by_id = _get_posts_by_id()
    try:
        post = posts_by_id[int(post_id)]
    except ValueError:
        post = None
    return render_template("posts.html", posts_by_id=posts_by_id, post=post)


@lru_cache
def _get_posts_by_id():
    posts = requests.get("https://jsonplaceholder.typicode.com/posts")
    posts.raise_for_status()
    posts_by_id = {post["id"]: post for post in posts.json()}
    return posts_by_id
