import os
import subprocess
import git
from tkinter import messagebox, simpledialog

class GitHubHandler:
    def __init__(self):
        self.cwd = os.getcwd()

    def stage_changes(self):
        try:
            self.repo.git.add('.')
        except git.GitCommandError as e:
            messagebox.showerror('Error', f'Error staging changes: {e.stderr}')

    def commit_changes(self, commit_msg):
        try:
            self.repo.git.commit('-m', commit_msg)
            messagebox.showinfo('Info', 'Changes committed successfully.')
        except git.GitCommandError as e:
            messagebox.showerror(
                'Error', f'Error committing changes: {e.stderr}')

    def push_changes(self):
        try:
            self.repo.git.push('origin', 'main')
            messagebox.showinfo('Info', 'Changes pushed successfully.')
        except git.GitCommandError as e:
            messagebox.showerror('Error', f'Error pushing changes: {e.stderr}')

    def push_to_github(self):
        # Find folders starting with "session"
        session_folders = [os.path.join(self.cwd, folder) for folder in os.listdir(
            self.cwd) if os.path.isdir(os.path.join(self.cwd, folder)) and folder.startswith("session")]

        if not session_folders:
            messagebox.showerror('Error', 'No session folders found.')
            return

        for folder in session_folders:
            # os.chdir(folder)  # Change directory to the session folder

            # Verify if the current directory is a Git repository
            try:
                self.repo = git.Repo('.')
            except git.InvalidGitRepositoryError:
                subprocess.run(["git", "init"])
                self.repo = git.Repo('.')

            # Check if a remote URL is configured or update if necessary
            if not self.repo.remotes or not self.repo.remotes.origin.exists():
                remote_url = simpledialog.askstring(
                    "Remote URL", f"Enter the remote URL for {folder}:")
                if not remote_url:
                    messagebox.showerror(
                        'Error', 'Remote URL cannot be empty.')
                    return
                else:
                    # Add remote URL
                    subprocess.run(
                        ["git", "remote", "add", "origin", remote_url])
            else:
                # Update the existing remote URL if needed
                remote_url = simpledialog.askstring(
                    "Update Remote URL", f"Enter updated remote URL for {folder} (leave blank to keep existing):")
                if remote_url:
                    self.repo.remotes.origin.set_url(remote_url)

            self.stage_changes()

            # Check if the main branch exists, create it if not
            main_branch = None
            for branch in self.repo.branches:
                if branch.name == 'main':
                    main_branch = branch
                    break

            if not main_branch:
                # Create and checkout main branch
                subprocess.run(["git", "checkout", "-b", "main"])

                # Checkout the newly created main branch

                main_branch = self.repo.head.reference

            # Commit message prompt
            commit_msg = simpledialog.askstring(
                "Commit Message", f"Enter commit message for {folder}:")
            if not commit_msg:
                messagebox.showerror(
                    'Error', 'Commit message cannot be empty.')
                return

            self.commit_changes(commit_msg)
            self.push_changes()

        os.chdir(self.cwd)
