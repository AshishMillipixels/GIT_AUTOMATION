import click
import os
import git
from git import Repo
import subprocess
from git_operations import (
    init_local_repo, add_and_commit, push_changes, create_branch,
    ensure_main_branch, auto_add_commit, merge_branch, generate_gitignore_function,
)
from github_api import create_github_repo, create_github_repo
from git_operations import generate_gitignore

@click.group()
def cli():
    """GitHub Automation CLI."""
    pass

#Create Repository (Locally & on GitHub)
@click.command()
@click.argument("repo_name")
@click.option("--private", is_flag=True, help="Create a private repository")
def create_repo(repo_name, private):
    """Create a new GitHub repository."""
    repo_path = f"./{repo_name}"
    create_github_repo(repo_name, private)

    if not os.path.exists(repo_path):
        os.makedirs(repo_path)

    repo = init_local_repo(repo_path)
                   
    origin_url = f"https://github.com/ashishkr010/{repo_name}.git"

    # Check if 'origin' already exists
    if "origin" not in [remote.name for remote in repo.remotes]:
        repo.create_remote("origin", url=origin_url)
        print(f" Remote 'origin' added with URL: {origin_url}")
    else:
        print(f"Remote 'origin' already exists. Updating URL to {origin_url}")
        repo.delete_remote("origin")  
        repo.create_remote("origin", url=origin_url) 

    # Add README and push initial commit
    with open(os.path.join(repo_path, "README.md"), "w") as f:
        f.write("this is our final script!")

    add_and_commit(repo_path, "Initial commit with README")
    push_changes(repo_path, "origin", "main")

    print(f"Repository '{repo_name}' created & pushed successfully!")


cli.add_command(create_repo)

# Initialize Local Git Repository
@click.command()
@click.argument("repo_path")
def init(repo_path):
    """Initialize a local Git repository."""
    init_local_repo(repo_path)
    print(f"Git initialized at {repo_path}")

cli.add_command(init)

# Create Branch
@click.command()
@click.argument("repo_path")
@click.argument("branch_name")
def branch(repo_path, branch_name):
    """Create a new branch."""
    create_branch(repo_path, branch_name)
    print(f"Branch '{branch_name}' created in {repo_path}")

cli.add_command(branch)

# Commit Changes
@click.command()
@click.argument("repo_path")
@click.argument("message")
def commit(repo_path, message):
    """Add and commit changes."""
    add_and_commit(repo_path, message)
    print(f"Changes committed with message: '{message}'")

cli.add_command(commit)

@cli.command()
@click.argument("repo_path")
@click.argument("remote", default="origin")
@click.argument("branch", default="main")
def push(repo_path, remote, branch):
    """Push commits to a remote repository."""
    push_changes(repo_path, remote, branch)


cli.add_command(push)


# Merge Branches
@click.command()
@click.argument("repo_path")
@click.argument("source_branch")
@click.argument("target_branch", default="main")
def merge(repo_path, source_branch, target_branch):
   
    merge_branch(repo_path, source_branch, target_branch)
    print(f"Merged '{source_branch}' into '{target_branch}'")

cli.add_command(merge)

#to be reviewed later(working...)
"""@click.command()
@click.argument("repo_name")
@click.argument("branch_name")
@click.option("--title", default="Auto PR", help="Title of the Pull Request")
def pr(repo_name, branch_name, title):
    Create a GitHub Pull Request.
    pr_number = create_github_pr(branch_name, title)
    if pr_number:
        print(f"PR #{pr_number} created successfully!")
    else:
        print(f"Failed to create PR.")

"""
#cli.add_command(pr)



@click.command(name="generate-gitignore")
@click.argument("repo_path", type=click.Path(exists=True))
def generate_gitignore(repo_path):
    """Automatically detect project type and generate a .gitignore file."""
    generate_gitignore_function(repo_path)


cli.add_command(generate_gitignore)




if __name__ == "__main__":
    cli()
