from git import Repo
import json
import sys, getopt
import requests
import glob, os
import getpass
import api_secrets

# ================================================
# Script Documentation
# Written by Nico Conforti
# Purpose: Pushes changes to Github and opens a pull request
# Background:
#   This script will check if there are any changes in the local repository and commit/push these to the test branch
#   A pull request is also opened (if there isn't one already)
#
# =================================================

# Variables to be defined
# gets the absolute path of the current file and goes one directory up to be at the top level
root_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..')) 
github_repo = 'github.com/nconforti93/madcap-python-example/

# Function safe_exit
# input: message - message that should be printed when exiting
# output: None - the script is aborted
# purpose:
#   Creates a file called error.txt before exiting.
#   It is not possible (in my attempts) to get the python error code in the Windows Batch Script.
#   Every attempt to do so showed the batch script successful, even though the python script failed.
#   To workaround this, the batch script will check immediately after execution of this script if
#   the error.txt file exists. If it does, it will delete the file and then return an error.
#   this way, the error is propagated to Jenkins and pipeline execution is shown as failed
def safe_exit(message):
    f = open(f"{root_dir}\Automation\error.txt", "x")
    sys.exit(message)

# Function commit_to_github
# input: None
# output: None
# purpose:
#   Compares files, sets some Git variables, and then commits and pushes any files that changed.
#   Afterwards it creates a pull request from test to master
def commit_to_github():
    # Sets an instance of the GitHub repo
    repo = Repo(root_dir)
    # Adds the list of any changed files into the changedFiles variable
    changedFiles = [item.a_path for item in repo.index.diff(None)]

    # Proceed only if there are actually changedFiles present. Otherwise nothing to commit
    if len(changedFiles) > 0:
        for item in changedFiles:
            # Display in the Jenkins log all of the files that were modified.
            print(f"Changes made to {item}")

        # Set git variables to show who is committing

        # stage all changes
        repo.git.add(all=True)

        # Commit the changes
        repo.index.commit("AUTOMATED - Updating weather info")

        # Define what the remote repository is
        origin = repo.remote(name='origin')
        origin.set_url(new_url = f"https://{user}:{token}@github.com/exasol/docs/")
        print("Pushing changes to Github")

        # Push the changes to remote
        repo.git.push('--set-upstream', 'origin', repo.active_branch.name )
        # Creates a pull request from test to main

        # creates a pull request from test -> main using the token stored in Jenkins. PR is created in Nico's name
        # because his token is being used
        print("Creating Pull Request")
        # create_pull_request(
        #    "exasol",  # project_name
        #    "docs",  # repo_name
        #    "Automated Changes (DOC-2292)",  # title
        #    "Please review all changes that were made automatically to test and merge to main ASAP. This is an automated pull request.",  # description
        #    "test",  # head_branch, "from" branch
        #    "main",  # base_branch, "to" branch
        #    token,  # git_token
        )
    else:
        print("No changes discovered, nothing to push to Github")

# Function create_pull_request
# input:
#   project_name - base folder in Github storing the docs repo
#   repo_name - name of the docs_repo
#   title - Title for the pull request
#   description - Description of the pull request
#   head_branch - The branch that is currently checked out. The "from" branch
#   base_branch - The branch you are tring to merge into. The "To" branch
#   git_token - Token used to perform the request.
# output: None
# purpose:
#   Uses the GitHub API to open a pull request
#   If a pull request for the branches already exists, then a warning is simply displayed. It will not cause the script to exit with an error.
def create_pull_request(project_name, repo_name, title, description, head_branch, base_branch, git_token):
    """Creates the pull request for the head_branch against the base_branch"""
    git_pulls_api = "https://api.github.com/repos/{0}/{1}/pulls".format(
        project_name,
        repo_name)
    headers = {
        "Authorization": "token {0}".format(git_token),
        "Content-Type": "application/json"}

    payload = {
        "title": title,
        "body": description,
        "head": head_branch,
        "base": base_branch,
    }
    r = requests.post(
        git_pulls_api,
        headers=headers,
        data=json.dumps(payload))

    # Checks if the request sent was ok. If not, then it sees if the error message says a pull request already exists
    if not r.ok:
        if 'A pull request already exists for exasol:test' in r.text:
            # Just print the message, don't exit forcefully
            print("WARNING: A pull request already exists for exasol:test. Skipping... ")
        else:
            # Some other error occurred, script should be aborted
            safe_exit("Failed to create Pull Request: {0}".format(r.text))
        
if __name__ == '__main__':

    # Check if the script was run already with parameters for user and token
    try:
        user = ''
        token = api_secrets.github_pat
        try:
            myopts, args = getopt.getopt(sys.argv[1:], "u:p:")
        except getopt.GetoptError as e:
            print(str(e))
            print("Usage: %s -u username -p password" % sys.argv[0])
            safe_exit("Bad parameters")

        for o, a in myopts:
            if o == '-u':
                user = a
            elif o == '-p':
                token = a
        # If the user was not set from a parameter, ask for the details
        if user == '':
            user = getpass.getpass(prompt='Enter your Github Username: ')

        # If the token was not when calling the script, ask for the details
        if token == '':
            token = getpass.getpass(prompt='Enter your Github PAT: ')

        # Run the commit_to_github function
        commit_to_github()

    except Exception as e:
        safe_exit(f"Unhandled ERROR: {e}")
