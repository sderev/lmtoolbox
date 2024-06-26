
# 2024-06-17

## Fixed

`commitgen` now exits when there are no staged changes to commit.

# 2024-06-09

## Changed

* Added non-interactive mode for commit message generation via `commitgen`:
    * Automatically generates and prints the commit message when standard output is not a TTY, then exits.
    * Ensures smoother integration in automated environments by bypassing user prompts in non-interactive contexts.
    * Improves usability in text editors like Vim with plugins such as vim-fugitive:
        * After using the `cc` keybinding to commit, running `!commitgen` in a non-interactive shell now directly inserts the commit message without displaying any additional output.
        * In an interactive shell, `commitgen` continues to display its entire output as before.
