
ENTRY = src/main.py

CONFIG = src/config.json

.PHONY: install run debug clean

install:
	uv sync

run:
	uv run python $(ENTRY) $(CONFIG)

debug:
	uv run python -m pdb $(ENTRY) $(CONFIG)

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -rf .mypy_cache

package:
	uv run pyinstaller --add-data "src/images:images" --add-data "src/ghosts_images:ghosts_images" --add-data "src/menu_images:menu_images" --onefile src/main.py

lint:
	uv run flake8 src
	uv run mypy src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
