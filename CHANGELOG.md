# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.3] - 2024-03-06 &ensp; \</lgf>

### Added

- Introduced wall jump: Implemented a wall jump mechanic, expanding the player's movement repertoire and enabling more dynamic navigation and exploration.
- Improved keybinding flexibility: Restructured key storage using a dictionary, enabling easier customization and modification of key bindings for a more personalized gameplay experience.
- Introduced platform tiles: Implemented a new ``Platform Tile`` that only collides with players from the top and sides, not from below, enabling more creative and engaging platforming gameplay.
- New platform elements: Expanded platform options with the addition of Cloud_plataforms and Scaffoldings.
- Fullscreen: Automatic ``fullscreen`` based on the screen size for a more captivating gameplay experience.
Enhanced visuals: Incorporated new player assets from [Kenney Platformer Art Pixel Redux](https://kenney.nl/assets/platformer-art-pixel-redux) to enrich the game's aesthetics.
- Improved physics: Implemented functions for precise x and y collision detection for physics_tiles and plataform_tiles, enhancing gameplay feel.
- New in-game assets: Loaded new assets into the game, enabling the use of animated tiles.
Tile animations: Added animations for more tiles like flags, water, and keys, enhancing their visual appeal.
- Health System: Added a health system with 3 hearts displayed on a dedicated UI script. Players lose a heart upon colliding with death tiles (e.g., world borders).
- ``DEATH_TILES`` type: This new tile type kills the player and respawns them at thelast checkpoint.
- Enhanced Rendering: Enhanced the tilemap rendering to support both game and editor modes. Editor mode displays EDITOR_ONLY tiles, while game mode hides them.
- Efficient Rendering: Now, the render function on ``sctips/tilemap.py`` renders only the tiles that are on the map.
- Collectibles System: The collectibles itens (i.e. ``coins``, ``diamonds``, ``keys``) now can be propperly collected.
- ``UI``: Added an User Interface, controlled by ``scripts/ui.py`` that shows the ammount of collectibles and the remaining hearts.
- ``Gates`` tile type: New tile type that disappears if it's is collided by a player that has at least one key.
- ``Checkpoints`` system: Now, flags works as checkpoints, so, once a player collides with a flag, it becames its spawn point.
- fonts folder: Added a directory to put all the fonts used in the game. The current fonts are from [Kenney Fonts](https://kenney.nl/assets/kenney-fonts)

### Changed
- Refined entity update: Enhanced the clarity and efficiency of the entities.update function.
- Player Animation rebase: Changed the player animations to fit in the new assets.
- Poles Hitboxes: Tiles that are like poles (i.e. mushroom stalk) now has a propper hitbox
- Assets Division: ``crates`` assets was divided into ``crates`` and ``key_door`` due to mechanics questions.
- Assets Division: ``flag`` assets was divided into ``flag`` and ``flag pole`` due to animation questions.



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