#1. if in linux use 'ctrl+f' and replace YOUR_USERNAME with github_username
"""2. Also, using terminal setup GITHUB API TOKEN, 
    command:  export GITHUB_TOKEN=" replace with your github token"
        also, check if it has been successfully setup or not
    command:  echo $GITHUB_TOKEN
    must print the token that you have put.
"""

import git
import os
from git import Repo
import requests


def init_local_repo(repo_path):
    """Ensure a Git repository is initialized with a remote and a main branch."""

    # Check if directory exists, create if not
    if not os.path.exists(repo_path):
        os.makedirs(repo_path)

    # Initialize repo if not already
    if not os.path.exists(os.path.join(repo_path, ".git")):
        repo = git.Repo.init(repo_path)
        print("Git repository initialized.")
    else:
        repo = git.Repo(repo_path)

    # Ensure 'main' branch exists
    if "main" not in repo.heads:
        repo.git.checkout("-b", "main")
        print("Created 'main' branch.")

    # Ensure remote 'origin' exists
    remote_url = f"https://github.com/YOUR_USERNAME/{os.path.basename(repo_path)}.git"
    if "origin" not in [remote.name for remote in repo.remotes]:
        repo.create_remote("origin", remote_url)
        print(f" Remote 'origin' added with URL: {remote_url}")

    # Ensure upstream is set for main
    try:
        repo.git.push("--set-upstream", "origin", "main")
        print("Pushed 'main' branch and set upstream.")
    except git.exc.GitCommandError:
        print("Warning: 'main' branch might already be pushed.")

    return repo




def create_branch(repo_path, branch_name):
    """Create a new branch if it doesn't already exist."""
    repo = Repo(repo_path)

    # Check if the branch already exists
    if branch_name in repo.heads:
        print(f"Branch '{branch_name}' already exists!")
        return

    # Create the branch and check it out
    new_branch = repo.create_head(branch_name)
    repo.head.reference = new_branch
    repo.head.reset(index=True, working_tree=True)

    print(f"Branch '{branch_name}' created successfully!")

def add_and_commit(repo_path, commit_message):
    #Stage all changes and commit them.
    repo = git.Repo(repo_path)
    repo.git.add(A=True)
    repo.index.commit(commit_message)
    print(f" Changes committed: {commit_message}")



def push_changes(repo_path, remote_name="origin", branch="main"):
    #Push commits to a remote repository.
    repo = git.Repo(repo_path)

    # Check if the remote exists, otherwise add it
    if remote_name not in [remote.name for remote in repo.remotes]:
        remote_url = f"https://github.com/YOUR_USERNAME/{repo_path.split('/')[-1]}.git"
        repo.create_remote(remote_name, remote_url)
        print(f" Remote '{remote_name}' added with URL {remote_url}")

    # Ensure branch exists locally before pushing
    if branch not in repo.heads:
        raise ValueError(f"Branch '{branch}' does not exist locally!")

    # Push changes
    origin = repo.remote(name=remote_name)
    origin.push(branch)
    print(f"Pushed changes to {remote_name}/{branch}")




def repo_status(repo_path):
    """Check the status of the repository."""
    repo = git.Repo(repo_path)
    status = repo.git.status()
    print(f"Repo Status:\n{status}")


def ensure_main_branch(repo_path):
    """Ensure the main branch exists and is set as default."""
    repo = git.Repo(repo_path)

    # Check if 'main' exists
    if "main" not in repo.branches:
        repo.git.branch("-M", "main")
        print(" 'main' branch set as the default.")

    # Set tracking if not already set
    if "origin" in repo.remotes:
        repo.git.push("--set-upstream", "origin", "main")
        print(" 'main' branch is now tracking origin/main.")
    else:
        print("Remote 'origin' not found. Please add a remote manually.")

        

def auto_add_commit(repo_path, commit_message="Auto-commit: changes saved"):
    
    repo = git.Repo(repo_path)

    # Check if there are any changes to commit
    if repo.is_dirty(untracked_files=True):
        repo.git.add(A=True)  # Stage all changes
        repo.index.commit(commit_message)
        print(f"Changes committed with message: '{commit_message}'")
    else:
        print("No changes to commit.")

def merge_branch(repo_path, source_branch, target_branch="main"):
    
    repo = git.Repo(repo_path)

    repo.git.checkout(target_branch)

    try:
        repo.git.merge(source_branch)
        print(f"Merged '{source_branch}' into '{target_branch}' successfully!")
    except git.exc.GitCommandError as e:
        print(f"Merge failed: {e}")



GITHUB_GITIGNORE_URL = "https://raw.githubusercontent.com/github/gitignore/main/"

def detect_project_type(repo_path):
    """Detect the project type based on existing files."""
    if os.path.exists(os.path.join(repo_path, "requirements.txt")):
        return "Python"
    elif os.path.exists(os.path.join(repo_path, "package.json")):
        return "Node"
    elif os.path.exists(os.path.join(repo_path, "Cargo.toml")):
        return "Rust"
    else:
        return None

def generate_gitignore(repo_path):
    """Generate a .gitignore file based on project type."""
    project_type = detect_project_type(repo_path)
    
    if not project_type:
        print("No recognizable project type found! Creating a default .gitignore.")
        gitignore_url = f"{GITHUB_GITIGNORE_URL}Global/JetBrains.gitignore"
    else:
        print(f"Detected project type: {project_type}. Fetching .gitignore...")
        gitignore_url = f"{GITHUB_GITIGNORE_URL}{project_type}.gitignore"

    response = requests.get(gitignore_url)

    if response.status_code == 200:
        gitignore_path = os.path.join(repo_path, ".gitignore")
        with open(gitignore_path, "w") as f:
            f.write(response.text)
        print(f" .gitignore created for {project_type} project!")

        # Add and commit .gitignore
        repo = Repo(repo_path)
        repo.git.add(".gitignore")
        repo.index.commit(f"Added .gitignore for {project_type} project")
        repo.remote(name="origin").push()
        print(" .gitignore committed and pushed!")
    else:
        print(" Failed to fetch .gitignore from GitHub.")




# Predefined Gitignore Templates
GITIGNORE_TEMPLATES = {
    "python": """
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Virtual environment
venv/
env/
*.egg-info/
.Python
pip-log.txt
pip-delete-this-directory.txt

# IDE settings
.vscode/
.idea/
*.swp
""",
    "node": """
# Node.js dependencies
node_modules/
npm-debug.log
yarn-error.log
""",
    "general": """
# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# OS files
.DS_Store
Thumbs.db
""",
}

def detect_project_type(repo_path):
    
    project_types = set()
    files = os.listdir(repo_path)

  
    if any(f.endswith(".py") for f in files):
        project_types.add("python")

    if any(f.endswith(".js") for f in files) or "package.json" in files:
        project_types.add("node")

    
    if not project_types:
        project_types.add("general")

    return list(project_types)



def generate_gitignore_function(repo_path):
    """
    Generates a .gitignore file by detecting the project type.
    If both Python and Node.js files exist, it combines both.
    """
    gitignore_path = os.path.join(repo_path, ".gitignore")
    project_types = detect_project_type(repo_path)

    
    gitignore_content = "\n".join(GITIGNORE_TEMPLATES[ptype] for ptype in project_types)

    with open(gitignore_path, "w") as gitignore_file:
        gitignore_file.write(gitignore_content.strip())

    print(f" .gitignore file generated successfully at {gitignore_path} for {', '.join(project_types)} projects.")
