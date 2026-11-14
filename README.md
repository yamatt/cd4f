# Claude Desktop for Fedora

This project repackages Anthropic's beta Claude Desktop Linux `.deb` as an RPM for Fedora. The package is built from the upstream Debian package and is distributed through a DNF repository hosted on GitHub Pages.

> [!WARNING]
> Claude Desktop for Linux is beta software. This is an independent community project, not an Anthropic product. Please report packaging or repository issues here rather than to Anthropic.

## Install

The repository is for Fedora x86_64. Add the repository configuration and install the package:

```bash
sudo tee /etc/yum.repos.d/claude-desktop.repo >/dev/null <<'EOF'
[claude-desktop]
name=Claude Desktop for Fedora
baseurl=https://yamatt.github.io/cd4f/
enabled=1
gpgcheck=1
repo_gpgcheck=0
gpgkey=https://yamatt.github.io/cd4f/RPM-GPG-KEY-claude-desktop
EOF

sudo dnf install claude-desktop
```

DNF verifies the RPM signature using the published key. The repository metadata itself is not signed. Updates are installed with the normal system update:

```bash
sudo dnf upgrade --refresh
```

To uninstall Claude Desktop and remove this repository:

```bash
sudo dnf remove claude-desktop
sudo rm /etc/yum.repos.d/claude-desktop.repo
```

The RPM becomes available after a successful repository publish. If the install command cannot find the package, check the repository's [Actions](https://github.com/yamatt/cd4f/actions) for the latest build and deployment status.

## Development

The [Fedora Dev Container](.devcontainer/devcontainer.json) provides Fedora and the tools used to unpack the Debian package, build and sign the RPM, and generate DNF repository metadata. Open this repository in VS Code and choose **Reopen in Container** to use it.

The container includes `rpm-build`, `rpm-sign`, `createrepo_c`, `binutils`, `tar`, `xz`, `curl`, and `gnupg2`. RPM builds require the packaging spec and source files; publishing additionally requires a signing key.

## Fork and publish

The GitHub Actions workflow checks the upstream Debian repository weekly and can also be started manually from the repository's **Actions** tab. It downloads the latest amd64 package, checks its SHA-256 digest, builds and signs an RPM, generates DNF repository metadata, and publishes the repository to GitHub Pages.

To publish from a fork:

1. Add a `claude-desktop.spec` RPM spec file and the packaging inputs required by that spec.
2. Create a dedicated OpenPGP signing key and configure its public and private parts as described below.
3. Add the armored private key as the repository Actions secret `GPG_PRIVATE_KEY`.
4. Enable GitHub Pages with **GitHub Actions** as the deployment source.
5. Update the repository and public-key URLs in this README and the DNF repository configuration above.
6. Run **Build and Publish DNF Repo** from **Actions** and confirm the deployment succeeded.

### Configure the RPM signing key

Use a dedicated key for this repository, not your personal signing key. The current workflow imports the key and signs RPMs unattended, so create it without a passphrase. Run this in a trusted local environment:

```bash
gpg --batch --pinentry-mode loopback --passphrase '' \
  --quick-generate-key "Claude Desktop Fedora RPM Signing" rsa4096 sign 0
```

Export the **public** key to the filename expected by the workflow, then commit that file:

```bash
gpg --armor --export "Claude Desktop Fedora RPM Signing" > RPM-GPG-KEY-claude-desktop
git add RPM-GPG-KEY-claude-desktop
git commit -m "Add RPM signing public key"
```

Export the **private** key to the ignored local file, then copy its contents into the GitHub Actions secret:

```bash
gpg --armor --export-secret-keys "Claude Desktop Fedora RPM Signing" \
  > RPM-GPG-PRIVATE-KEY.asc
chmod 600 RPM-GPG-PRIVATE-KEY.asc
```

In GitHub, open the repository's **Settings → Secrets and variables → Actions → New repository secret**. Name the secret `GPG_PRIVATE_KEY`, paste the complete contents of `RPM-GPG-PRIVATE-KEY.asc` (including the PGP block markers), and save it. The private key is unencrypted to support unattended signing. Keep the file protected, never commit or share it, and remove it from this machine when you have securely backed it up and added it to GitHub.

The public key is published with the RPM repository and is used by DNF to verify packages; the private key stays in the Actions secret. Keep a secure backup of the private key. RPM signatures cannot be verified if a published key is replaced without accounting for existing installations.

## Background

[Anthropic distributes Claude Desktop for Linux](https://code.claude.com/docs/en/desktop-linux) in beta as a Debian package for Debian- and Ubuntu-based systems. This project adapts that package for Fedora; it does not modify or provide the Claude Desktop application itself.
