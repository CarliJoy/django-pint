# Makefile

# Define a help target to show the available commands and their purposes
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make dev-setup           - Setup and test the development environment (requires pyenv and Docker already installed)"
	@echo "  make install-pyenv       - Install pyenv and its dependencies"
	@echo "  make install-python      - Install supported Python versions 3.8, 3.9, 3.10, 3.11 using pyenv"
	@echo "  make install-docker      - Install Docker and add the current user to the docker group"
	@echo "  make install-pipx        - Install pipx and ensure it's on your PATH"
	@echo "  make install-pre-commit  - Install pre-commit using pipx"
	@echo "  make install-tox         - Install tox using pipx and inject tox-docker"
	@echo "  make activate-pre-commit - Activate pre-commit hooks"
	@echo "  make lint                - Run pre-commit checks on all files"
	@echo "  make test                - Run tests with tox"
	@echo "  make dev-setup           - Run all the above commands in sequence (pipx, pre-commit, tox, activate-pre-commit, lint, test)"
	@echo ""
	@echo "Suggested use:"
	@echo "  If you already have pyenv and Docker installed, run 'make dev-setup' for the python/env you need setting up!"
	@echo "  Otherwise, start with 'make install-pyenv', 'make install-python', and 'make install-docker'."
	@echo "  When everything is in place run 'make test' to do run the testing suite."

# Set the default target to help
.PHONY: all
all: help

# Target to install pyenv
.PHONY: install-pyenv
install-pyenv:
	sudo apt-get install -y make build-essential libssl-dev zlib1g-dev
	sudo apt-get install -y libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev
	sudo apt-get install -y libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python3-openssl
	@echo "Installing pyenv..."
	/bin/bash -c "$$(curl -fsSL https://pyenv.run)"
	@echo "Pyenv has been installed. Please restart your shell or run 'exec $$SHELL' to refresh your environment."

# Target to install all needed python versions
.PHONY: install-python
install-python:
	pyenv install 3.8 3.9 3.10 3.11

# Target for installing Docker
.PHONY: install-docker
install-docker:
	sudo apt update
	sudo apt install -y docker.io
	sudo usermod -aG docker $(USER)
	@echo "Please log out and log back in to apply the docker group changes."

# Target for installing pipx and ensuring the path is set
.PHONY: install-pipx
install-pipx:
	python -m pip install --user --upgrade pip
	python -m pip install --user pipx
	python -m pipx ensurepath

# Target for installing pre-commit using pipx
.PHONY: install-pre-commit
install-pre-commit: install-pipx
	pipx install pre-commit

# Target for installing tox using pipx
.PHONY: install-tox
install-tox: install-pipx
	pipx install tox
	pipx inject tox tox-docker

# Target to activate pre-commit hooks
.PHONY: activate-pre-commit
activate-pre-commit:
	pre-commit install

# Target to run pre-commit checks on all files
.PHONY: lint
lint:
	pre-commit run --all-files


# Target to run all the above commands in sequence
.PHONY: dev-setup
dev-setup: install-pipx install-pre-commit install-tox activate-pre-commit lint

# Target to run tests with tox
.PHONY: test
test:
	tox
