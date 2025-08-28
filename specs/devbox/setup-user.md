# Setup user for development box

Goal:
1. A `chuyeow` user with passwordless sudo access.
2. Home directory at `/home/chuyeow`.
3. Bash as default shell.
4. Current user's public keys in `~/.ssh/authorized_keys` are added to `chuyeow` user's `~/.ssh/authorized_keys`.
5. Add a `code` directory in `/home/chuyeow`.

# Set up npm

Configure npm to use a directory in the home folder for global installs to avoid needing to run as root.

1. Run `mkdir -p ~/.npm-global`
2. Run `npm config set prefix '~/.npm-global'`
3. Run `echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc`
4. Run `source ~/.bashrc`

# Re-install Claude Code for this user if necessary

1. Run `npm install -g @anthropic-ai/claude-code`

# Set up Happy for remote Claude Code access

Happy: https://happy.engineering/

1. Run `npm i -g happy-coder`
