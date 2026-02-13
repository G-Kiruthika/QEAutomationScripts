import subprocess
import os
from typing import List, Dict, Optional


class GitIntegration:
    """Git integration utilities for automation framework"""

    def __init__(self, repo_path: str = None):
        """Initialize GitIntegration with repository path"""
        self.repo_path = repo_path or os.getcwd()

    def execute_git_command(self, command: List[str]) -> Dict[str, any]:
        """Execute git command and return result"""
        try:
            result = subprocess.run(
                command,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return {
                "success": True,
                "output": result.stdout,
                "error": None
            }
        except subprocess.CalledProcessError as e:
            return {
                "success": False,
                "output": e.stdout,
                "error": e.stderr
            }

    def get_current_branch(self) -> Optional[str]:
        """Get current git branch"""
        result = self.execute_git_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
        if result['success']:
            return result['output'].strip()
        return None

    def get_commit_hash(self) -> Optional[str]:
        """Get current commit hash"""
        result = self.execute_git_command(['git', 'rev-parse', 'HEAD'])
        if result['success']:
            return result['output'].strip()
        return None

    def get_changed_files(self) -> List[str]:
        """Get list of changed files"""
        result = self.execute_git_command(['git', 'diff', '--name-only'])
        if result['success']:
            return [f.strip() for f in result['output'].split('\n') if f.strip()]
        return []

    def get_staged_files(self) -> List[str]:
        """Get list of staged files"""
        result = self.execute_git_command(['git', 'diff', '--name-only', '--cached'])
        if result['success']:
            return [f.strip() for f in result['output'].split('\n') if f.strip()]
        return []

    def stage_files(self, files: List[str]) -> bool:
        """Stage files for commit"""
        if not files:
            return False
        
        command = ['git', 'add'] + files
        result = self.execute_git_command(command)
        return result['success']

    def commit_changes(self, message: str) -> bool:
        """Commit staged changes"""
        result = self.execute_git_command(['git', 'commit', '-m', message])
        return result['success']

    def push_changes(self, remote: str = 'origin', branch: str = None) -> bool:
        """Push changes to remote"""
        if branch is None:
            branch = self.get_current_branch()
        
        if not branch:
            return False
        
        result = self.execute_git_command(['git', 'push', remote, branch])
        return result['success']

    def create_branch(self, branch_name: str) -> bool:
        """Create new branch"""
        result = self.execute_git_command(['git', 'checkout', '-b', branch_name])
        return result['success']

    def checkout_branch(self, branch_name: str) -> bool:
        """Checkout existing branch"""
        result = self.execute_git_command(['git', 'checkout', branch_name])
        return result['success']

    def get_repo_status(self) -> Dict[str, any]:
        """Get repository status"""
        return {
            "branch": self.get_current_branch(),
            "commit_hash": self.get_commit_hash(),
            "changed_files": self.get_changed_files(),
            "staged_files": self.get_staged_files()
        }
