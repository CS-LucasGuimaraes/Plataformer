# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.2] - 2024-02-28 &ensp; \</lgf>

### Added

- Map editor integration: Introduced a dedicated map editor for intuitive and efficient level creation.
- Seamless map management: Implemented a read/write function using JSON files, enabling easy map creation, sharing, and modification. The game automatically loads the map.json file within its folder for convenient level access.
- Following camera: Implemented a camera that follows the player, leaving it always on the center on the screen.

### Changed

- ``tilemap.render`` function now renders only the tiles that are on the screen, avoiding unnecessary memory and cpu usage.



## [0.0.1] - 2024-02-27 &ensp; \</lgf>

### Added

- Comprehensive documentation: Introduced a LICENSE file specifying permissions, and a .gitignore file for efficient version control.
- Detailed change log: Added a CHANGELOG.md file to track project development and updates.
- Core assets and functionalities: Incorporated basic data and assets (subject to future changes) and implemented the main game functionality within ``game.py``.
- Modular structure: Organized code into a ``Scripts`` folder containing ``.py`` files for specific functionalities:
  - ``entities.py``: Controls entities and the player.
  - ``tilemap.py``: Handles the game map.
  - ``utils.py``: Provides utility functions l ike animation and image loading.