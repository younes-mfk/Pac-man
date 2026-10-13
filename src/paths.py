"""Resolve resource paths for both development and frozen executables."""

import os
import sys


class PathResolver:
    """Locate bundled resource files regardless of how the game is run."""

    @staticmethod
    def resource_path(relative_path: str) -> str:
        """Build the absolute path of a resource file.

        When the game runs as a PyInstaller executable, the path is
        built from the folder where PyInstaller placed the bundled
        files. When it runs as a normal Python script, the path is
        built from the folder containing this module.

        Args:
            relative_path (str): Path of the resource relative to the
                bundle root or project root, e.g. "menu_images/menu.png".

        Returns:
            str: The absolute path to the requested resource.
        """
        if getattr(sys, "frozen", False):
            base_path = getattr(sys, "_MEIPASS")
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        return os.path.join(base_path, relative_path)
