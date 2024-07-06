# SPDX-FileCopyrightText: 2024-present underfirst <underfirst@gmail.com>
#
# SPDX-License-Identifier: MIT
from pathlib import Path

import click

from alfred_snippet_manager.__about__ import __version__
from alfred_snippet_manager.controllers.main import AlfredSnippetManager

mgr = AlfredSnippetManager()


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="alfred_snippet_manager")
def alfred_snippet_manager():
    click.echo("Alfred snippet manager...")


@alfred_snippet_manager.command()
def sync():
    click.echo("Sync repo and update...")
    mgr.sync_repos()
    mgr.update()


@alfred_snippet_manager.command()
def check_repos():
    click.echo("Check git repositories...")
    mgr.sync_repos()


@alfred_snippet_manager.command()
@click.option("--repo", help="Add git repository.")
@click.option("--local", help="Add local directory.")
def configure(repo: str | None = None, local: str | None = None):
    if repo is None and local is None:
        msg = "Both repo and preference are None. Set at least each of them."
        raise ValueError(msg)
    if repo is not None:
        click.echo(f"Add git repository: {repo}")
        mgr.add_repo(repo)
    if local is not None:
        click.echo(f"Add local directory: {local}")
        mgr.add_local(Path(local))
