
ENTRY = main.py

.PHONY: install run debug clean

install:
	uv sync

run:
	uv run python $(ENTRY)

debug:
	uv run python -m pdb $(ENTRY)

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -rf .mypy_cache

package:
	uv run pyinstaller --name Pacman --add-data "images:images" --add-data "menu_images:menu_images" --add-data "ghosts_images:ghosts_images" main.py

lint:
	uv run flake8 . --exclude=.venv
	uv run mypy . --exclude='(^|/)\.venv/' --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
