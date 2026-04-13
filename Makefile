project_root := $(CURDIR)
gradlew := $(project_root)/gradlew

.PHONY: run-housekeeping commitizen-run-check python-test-release-version python-test-custom-plugin-repository gradle-verify

## Housekeeping
.run-brew-upgrade:
	@brew update
	@brew bundle --file ./Brewfile upgrade #--no-lock

# Helper function to update local tooling within the repo
run-housekeeping: .run-brew-upgrade

# Validate the current git commit message against Conventional Commits.
commitizen-run-check:
	@commit_msg_file="$$(git rev-parse --git-path COMMIT_EDITMSG)"; \
	if [ ! -f "$$commit_msg_file" ]; then \
		echo "Unable to find a git commit message file at $$commit_msg_file"; \
		exit 1; \
	fi; \
	cz check \
		--commit-msg-file "$$commit_msg_file" \
		--allow-abort \
		--allowed-prefixes Merge Revert fixup! squash!

# Run the Python tests that power release version calculation.
python-test-release-version:
	@python3 -m unittest scripts.test_release_version

# Run Python tests for generating a JetBrains custom plugin repository.
python-test-custom-plugin-repository:
	@python3 -m unittest scripts.test_custom_plugin_repository

# Mirror the Gradle verification used in CI before pushing changes.
gradle-verify:
	@chmod +x "$(gradlew)"
	@"$(gradlew)" test buildPlugin --stacktrace
