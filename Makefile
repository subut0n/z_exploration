.PHONY: clean cp cpy

clean:
	rm -rf z_exploration/*

# For macOS
cp:
	@read -p "Directory to explore: " dir; \
	read -p "Exclude patterns (comma-separated, leave empty if none): " exclude; \
	read -p "Contain patterns (comma-separated, leave empty if none): " contain; \
	python3 explore_directory.py -n "$$dir" $(if $(exclude), -e "$$exclude") $(if $(contain), -c "$$contain"); \
	find z_exploration -name "*.txt" -type f -print0 | xargs -0 stat -f "%m %N" | sort -rn | head -1 | cut -f2- -d" " | xargs cat | pbcopy

# For Ubuntu
cpy:
	@read -p "Directory to explore: " dir; \
	read -p "Exclude patterns (comma-separated, leave empty if none): " exclude; \
	read -p "Contain patterns (comma-separated, leave empty if none): " contain; \
	python3 explore_directory.py -n "$$dir" $(if $(exclude), -e "$$exclude") $(if $(contain), -c "$$contain"); \
	find z_exploration -name "*.txt" -type f -printf "%T@ %p\n" | sort -n | tail -1 | cut -f2- -d" " | xargs cat | xclip -selection clipboard

