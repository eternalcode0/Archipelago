# The Minish Cap Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases)
- An EU copy of The Legend of Zelda: The Minish Cap. The Archipelago community cannot provide this.
- [BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory) 2.7 or later

## Optional Software

- [TMC AP Tracker by Deoxis](https://github.com/deoxis9001/tmcrando_maptracker_deoxis/releases/latest), for use with
[PopTracker](https://github.com/black-sliver/PopTracker/releases)

### Configuring BizHawk

Once you have installed BizHawk, open `EmuHawk.exe` and change the following settings:

- If you're using BizHawk 2.7 or 2.8, go to `Config > Customize`. On the Advanced tab, switch the Lua Core from
`NLua+KopiLua` to `Lua+LuaInterface`, then restart EmuHawk. (If you're using BizHawk 2.9, you can skip this step.)
- Under `Config > Customize`, check the "Run in background" option to prevent disconnecting from the client while you're
tabbed out of EmuHawk.
- Open a `.gba` file in EmuHawk and go to `Config > Controllers…` to configure your inputs. If you can't click
`Controllers…`, load any `.gba` ROM first.
- Consider clearing keybinds in `Config > Hotkeys…` if you don't intend to use them. Select the keybind and press Esc to
clear it.

## Installing the apworld

How to use an .apworld:
Place the .apworld in your Archipelago/custom_worlds folder, or double-click
the .apworld to do so automatically.
Use ArchipelagoLauncher.exe to open the Launcher, and click on Generate
Template Options to create template yamls for your custom .apworlds.
Place the desired player yamls in the Players folder, and customize them as
you see fit.
Use ArchipelagoGenerate.exe to generate the game.
Upload the generated game (in the output folder) on the website at
https://archipelago.gg/uploads and create a new room.
Refer to the individual game's setup guide for further instruction (usually in
the pins for the game's ⁠future-game-design⁠ post or its github).
Patch files can be found inside the zipped file in your output folder instead
of the room page.

## Generating and Patching a Game

1. Create your options file (YAML). You can download one from the GitHub
Releases page or create the default YAML from your Launcher with the "Generate Template Options"
2. Follow the general Archipelago instructions for [generating a game](../../Archipelago/setup/en#generating-a-game).
This will generate an output file for you. Your patch file will have the `.aptmc` file extension.
3. Open `ArchipelagoLauncher.exe`
4. Select "Open Patch" on the left side and select your patch file.
5. If this is your first time patching, you will be prompted to locate your vanilla ROM.
6. A patched `.gba` file will be created in the same place as the patch file.
7. On your first time opening a patch with BizHawk Client, you will also be asked to locate `EmuHawk.exe` in your
BizHawk install.

If you're playing a single-player seed and you don't care about autotracking or hints, you can stop here, close the
client, and load the patched ROM in any emulator. However, for multiworlds and other Archipelago features, continue
below using BizHawk as your emulator.

## Connecting to a Server

By default, opening a patch file will do steps 1-5 below for you automatically. Even so, keep them in your memory just
in case you have to close and reopen a window mid-game for some reason.

1. The Minish Cap uses Archipelago's BizHawk Client. If the client isn't still open from when you patched your game,
you can re-open it from the launcher.
2. Ensure EmuHawk is running the patched ROM.
3. In EmuHawk, go to `Tools > Lua Console`. This window must stay open while playing.
4. In the Lua Console window, go to `Script > Open Script…`.
5. Navigate to your Archipelago install folder and open `data/lua/connector_bizhawk_generic.lua`.
6. The emulator and client will eventually connect to each other. The BizHawk Client window should indicate that it
connected and recognized The Minish Cap.
7. To connect the client to the server, enter your room's address and port (e.g. `archipelago.gg:38281`) into the
top text field of the client and click Connect.

You should now be able to receive and send items. You'll need to do these steps every time you want to reconnect. It is
perfectly safe to make progress offline; everything will re-sync when you reconnect.

## Auto-Tracking

The Minish Cap has a fully functional map tracker that supports auto-tracking.

1. Download [The Minish Cap AP Tracker](https://github.com/deoxis9001/tmcrando_maptracker_deoxis/releases/latest) and
[PopTracker](https://github.com/black-sliver/PopTracker/releases).
2. Put the tracker pack into packs/ in your PopTracker install.
3. Open PopTracker, and load the Minish Cap Randomizer Map Tracker pack. If using the Map Tracker be sure to select the **AP** variant.
4. For autotracking, click on the "AP" symbol at the top.
5. Enter the Archipelago server address (the one you connected your client to), slot name, and password.
