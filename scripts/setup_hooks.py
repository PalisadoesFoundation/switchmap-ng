import os
import shutil

# Use os.path.join for path construction
# Get the script's directory to make paths relative to the project root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
HOOKS_DIR = os.path.join(PROJECT_ROOT, ".git", "hooks")
SOURCE_HOOKS_DIR = os.path.join(PROJECT_ROOT, "hooks")
HOOK_FILE = "pre-commit"


def install_git_hooks():
    """Installs Git hooks by copying the pre-commit hook to the .git/hooks directory and making it executable.

    Ensures that the .git/hooks directory exists, copies the 'pre-commit' hook from the specified source directory
    to .git/hooks, and then sets the correct permissions for the hook file to be executable.

    Raises:
        FileNotFoundError: If the source hook file does not exist.
    """
    # Ensure .git/hooks exists
    os.makedirs(HOOKS_DIR, exist_ok=True)

    # Copy hooks to .git/hooks
    source_hook_path = os.path.join(SOURCE_HOOKS_DIR, HOOK_FILE)
    destination_hook_path = os.path.join(HOOKS_DIR, HOOK_FILE)

    if not os.path.exists(source_hook_path):
        raise FileNotFoundError(
            f"Source hook file '{source_hook_path}' not found."
        )

    shutil.copy(source_hook_path, destination_hook_path)

    # Make the hook file executable
    os.chmod(destination_hook_path, 0o755)

    print(f"Git hook '{HOOK_FILE}' installed successfully in {HOOKS_DIR}")


# Run the function to install the hooks
if __name__ == "__main__":
    install_git_hooks()
