project_root="$(CURDIR)"

## Housekeeping
.run-brew-upgrade:
	@brew update
	@brew bundle --file ./Brewfile upgrade #--no-lock

# Helper function to update local tooling within the repo
run-housekeeping: .run-brew-upgrade