"""github-blog generator:

`python main.py <github_token> <github_repo>`

Read issues from GitHub and generate HTML articles.

Powered by Jinja2 and PyGithub
"""
import argparse
import os
import shutil

import requests
from feedgen.feed import FeedGenerator
from github import Github
from github.Issue import Issue
from github.PaginatedList import PaginatedList
from jinja2 import Environment, FileSystemLoader


def dir_init(content_dir: str, backup_dir: str):
    """
    A function to initialize directories by removing existing ones and creating new ones.
    """
    if os.path.exists(content_dir):
        shutil.rmtree(content_dir)
    if os.path.exists(backup_dir):
        shutil.rmtree(backup_dir)

    os.mkdir(content_dir)
    os.mkdir(content_dir + "blog/")
    os.mkdir(backup_dir)

    static_dir = content_dir + "static/"
    if not os.path.exists(static_dir):
        shutil.copytree("templates/static", static_dir)


def get_all_issues(
    github_token: str,
    github_repo: str,
) -> PaginatedList[Issue]:
    """Get all issues for a given GitHub repository.

    Args:
        github_token: GitHub personal access token.
        github_repo: GitHub repository name in the format "owner/name".

    Returns:
        List of GitHub issue objects.
    """
    user = Github(github_token)
    repo = user.get_repo(github_repo)
    issues = repo.get_issues()
    return issues


def render_article_list(issues: PaginatedList[Issue]):
    """
    A function that renders an article list using a provided list of issues.

    Parameters:
    - issues: PaginatedList, a paginated list of issues to render in the article list.

    Returns:
    - str, the rendered article list HTML content.
    """
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("index.html")
    return template.render(issues=issues)


def save_index_as_html(content: str):
    """
    Save the provided content as an HTML file at the specified path.

    Parameters:
    content (str): The content to be written to the HTML file.
    """
    path = content_dir + "index.html"
    f = open(path, "w", encoding="utf-8")
    f.write(content)
    f.close


def markdown2html(mdstr: str):
    """
    Convert markdown text to HTML using the GitHub API.

    Args:
        mdstr (str): The markdown text to be converted to HTML.

    Returns:
        str: The HTML representation of the input markdown text.
    """
    payload = {"text": mdstr, "mode": "gfm"}
    headers = {"Authorization": "token {}".format(options.github_token)}
    try:
        response = requests.post(
            "https://api.github.com/markdown", json=payload, headers=headers
        )
        response.raise_for_status()  # Raises an exception if status code is not 200
        return response.text
    except requests.RequestException as e:
        raise Exception("markdown2html error: {}".format(e))


def render_issue_body(issue: Issue):
    """
    Render the body of an issue by converting markdown to HTML and injecting it into a template.

    Parameters:
    issue (Issue): The issue object containing the body to render.

    Returns:
    str: The rendered HTML body of the issue.
    """
    html_body = markdown2html(issue.body)
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("post.html")
    return template.render(issue=issue, html_body=html_body)


def save_articles_to_content_dir(issue: Issue, content: str):
    path = content_dir + f"blog/{issue.number}.html"
    f = open(path, "w", encoding="utf-8")
    f.write(content)
    f.close


def gen_rss_feed(issues: PaginatedList[Issue]):
    fg = FeedGenerator()
    fg.id("https://geoqiao.github.io/contents")
    fg.title("GeoQiao's Blog")
    fg.author({"name": "GeoQiao", "email": "geoqiao@example.com"})
    fg.link(href="https://geoqiao.github.io/contents", rel="alternate")
    fg.description("This is GeoQiao's Blog")

    for issue in issues:
        fe = fg.add_entry()
        fe.id(f"https://geoqiao.github.io/contents/blog/{issue.number}.html")
        fe.title(issue.title)
        fe.link(href=f"https://geoqiao.github.io/contents/blog/{issue.number}.html")
        fe.description(issue.body[:100])
        fe.published(issue.created_at)
        fe.content(markdown2html(issue.body), type="html")

    fg.atom_file("./contents/atom.xml")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("github_token", help="<github_token>")
    parser.add_argument("github_repo", help="<github_repo>")
    options = parser.parse_args()

    content_dir: str = "./contents/"
    backup_dir: str = "./backup/"

    dir_init(content_dir, backup_dir)
    issues = get_all_issues(options.github_token, options.github_repo)
    article_list = render_article_list(issues)
    save_index_as_html(content=article_list)

    for issue in issues:
        content = render_issue_body(issue)
        save_articles_to_content_dir(issue, content=content)

    gen_rss_feed(issues)
