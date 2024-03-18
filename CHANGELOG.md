# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [0.0.10] - 2024-03-18 &ensp; \</~mdon>

### Added

- Enemy collisions: Now, the enemy just kill the player if the collision occurs from one of the sides or from bottom-up. Otherwise (if the collision is top-down), the enemy is killed.

### Changed

- BUGFIX: Restart Function order was changed to fix a bug when the player dies at the place that a enemy would spawn.

## [0.0.9] - 2024-03-18 &ensp; \</~lgf>

### Added

- Sound Effects: Added the possibility to play SFX when some action occurs.
- Backhround sounds: Added a background music and background ambience sounds.

### Changed

- Diferent editor levels: Now the editor support editing different leves. It asks the user wich level he want to eddit on run.


## [0.0.8] - 2024-03-18 &ensp; \</~lgf>

### Added

- More Levels: Added a levels folder, wich stores each map of the game.
- Save games: Now, the game has saves that store where the player was on it's last gameplay.
- Next Level: Blue flag added to trasport the player to the next level.

### Changed

- SpawPoint tile: New ``editor only`` tile added that allows the editor to chose where the player should start the level.
- Restart Level: Function created to properly organize everything in level restarting.

## [0.0.7] - 2024-03-14 &ensp; \</~lgf>

### Added

- Enemies Spawn: Added an enemies tile that spawn an enemy on map loading.


## [0.0.6] - 2024-03-14 &ensp; \</~lgf>

### Added

- Enemies: Added an enemy class that renders a Mario-like enemy.
- Spikes: Now, the spikes as a propper hitbox and kill the player on collision.



## [0.0.5] - 2024-03-07 &ensp; \</~lgf>

### Changed

- Editor rendering order: Changed the order of rendering functions to show the preview correctly.
- Dictation rename: ``any_came_From_bottom`` renamed to ``inside_plataform`` for clarity.
- Useless check: Removed the useless instruction that checks if the player is inside a ``platform`` when colliding with ``physical tiles``. This also resolved some bugs with this mixed collision type.



## [0.0.4] - 2024-03-06 &ensp; \</~lgf>

### Added

- Joystick integration: Implemented initial support for joysticks, starting with the Xbox Controller, providing players with alternative control options for a more comfortable and immersive experience.


### Changed

- Event verification order: Changed the order of the ``event.type`` verification. The most likely comes first, the others later. This can improve a little bit the performance.
- Compartmented Game Functions: Now the ``Game`` Class has different functions to start each necessary part and to control the Game in ``run``. This makes the code easier to read and understand.
- Compartmented Editor Functions: Now the ``Editor`` Class has different functions to start each necessary part and to control the editor in ``run``. This makes the code easier to read and understand.
- Clear the code: Removed unnecessary prints.
- New background: Changed the background color to a blue tone.
- Better Collisions Functions: the collision_check functions are stored on a dict for better comprehension purposes.
- Better function names: some ``entities`` functions were renamed for better understading. (i.e. side_plataform_collide_update -> any_came_from_bottom) 
- Max jump controller: The player now has the ``self.max_jumps`` attribute to quickly change the number of maximum jumps instead of always being 2.



## [0.0.3] - 2024-03-06 &ensp; \</~lgf>

### Added

- Introduced wall jump: Implemented a wall jump mechanic, expanding the player's movement repertoire and enabling more dynamic navigation and exploration.
- Improved keybinding flexibility: Restructured key storage using a dictionary, enabling easier customization and modification of key bindings for a more personalized gameplay experience.
- Introduced platform tiles: Implemented a new ``Platform Tile`` that only collides with players from the top and sides, not from below, enabling more creative and engaging platforming gameplay.
- New platform elements: Expanded platform options with the addition of Cloud_plataforms and Scaffoldings.
- Fullscreen: Automatic ``fullscreen`` based on the screen size for a more captivating gameplay experience.
- Enhanced visuals: Incorporated new player assets from [Kenney Platformer Art Pixel Redux](https://kenney.nl/assets/platformer-art-pixel-redux) to enrich the game's aesthetics.
- Improved physics: Implemented functions for precise x and y collision detection for physics_tiles and plataform_tiles, enhancing gameplay feel.
- New in-game assets: Loaded new assets into the game, enabling the use of animated tiles.
- Tile animations: Added animations for more tiles like flags, water, and keys, enhancing their visual appeal.
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



## [0.0.2] - 2024-02-28 &ensp; \</~lgf>

### Added

- Map editor integration: Introduced a dedicated map editor for intuitive and efficient level creation.
- Seamless map management: Implemented a read/write function using JSON files, enabling easy map creation, sharing, and modification. The game automatically loads the map.json file within its folder for convenient level access.
- Following camera: Implemented a camera that follows the player, leaving it always on the center on the screen.

### Changed

- ``tilemap.render`` function now renders only the tiles that are on the screen, avoiding unnecessary memory and cpu usage.



## [0.0.1] - 2024-02-27 &ensp; \</~lgf>

### Added

- Comprehensive documentation: Introduced a LICENSE file specifying permissions, and a .gitignore file for efficient version control.
- Detailed change log: Added a CHANGELOG.md file to track project development and updates.
- Core assets and functionalities: Incorporated basic data and assets (subject to future changes) and implemented the main game functionality within ``game.py``.
- Modular structure: Organized code into a ``Scripts`` folder containing ``.py`` files for specific functionalities:
  - ``entities.py``: Controls entities and the player.
  - ``tilemap.py``: Handles the game map.
  - ``utils.py``: Provides utility functions l ike animation and image loading.