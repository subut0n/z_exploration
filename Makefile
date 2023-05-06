# Makefile

.PHONY: clean regen copy

clean:
	rm -rf z_exploration/*

regen: clean
	@echo "Exploration du dossier $(dir)"
	python3 explore_directory.py -n "$(dir)" -e "$(exclude)"

copy:
	find z_exploration -name "*.txt" -type f -printf "%T@ %p\n" | sort -n | tail -1 | cut -f2- -d" " | xargs cat | xclip -selection clipboard

cp:
	find z_exploration -name "*.txt" -type f -print0 | xargs -0 stat -f "%m %N" | sort -rn | head -1 | cut -f2- -d" " | xargs cat | pbcopy
