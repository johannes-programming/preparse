rstrip:
	find . -type f -name "*.toml" -exec sed -i '' -e 's/[[:space:]]*$//' "{}" +
	#sed -i '' -e 's/[[:space:]]*$//' "pyproject.toml"