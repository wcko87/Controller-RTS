[![Build status](https://ci.appveyor.com/api/projects/status/w1qqnxpe1y2lu5o4?svg=true)](https://ci.appveyor.com/project/wcko87/controller-rts)

# Download
https://github.com/wcko87/Controller-RTS/releases

# Introduction
This program works by translating controller inputs into simulated mouse+keyboard inputs.

This is more of a proof of concept than anything, so expect quite a bit of jank, like occasional missed inputs or slow inputs because of how the input simulation works. I had to make quite a number of concessions as well due to the limitations of doing things this way. See below for a comparison of this program to how it would actually be like if the controls were implemented natively into the game.

Note that some things may break if Tempest Rising updates some of its controls/UI, unless I update this program to match. For now, this program works as of May 2026.

Note that only in-game actions work. Menus etc. are not supported, so you have to use the mouse or keyboard for those.

# How to Set up
Here are the main steps:
1. Modify hotkey_mapping.txt to match your game's hotkey settings.
	- Refer to vk_keys.py for the names of the keyboard keys. Some keyboard keys like the semicolon (;) will have strange names like OEM_1.
	- See [Virtual-Key Codes](https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes) if you are unsure what some of the keys refer to.
	- This is because many inputs are simulated with hotkeys, and this will absolutely depend on what you have your hotkeys set to.
2. Steam input:
	- Use the layout **TR Controller Input Setup** from the community store.
	- How: Right click Tempest Rising on steam, click **Properties**, click the **Controller** tab, enable Steam Input, click the underlined **Controller Configurator**, click on your current layout, click either **Community Layouts** or **Search**, then search for the layout.
		- What this layout does: Makes the left stick control the right stick (the right stick controls the camera by default), disables the right stick's ability to control the camera, disables camera movement via stick while holding LT, LB, RB or Y.
3. Plug in controller, open game, run program.
	- The program should automatically detect the open game and overlay a cursor in the middle.


# Controls
```
      _____                                     _____
      \ LT \ Minimap                     Shift / RT /
       \____\                                 /____/
       _______                               _______
      (__LB__/ ----------------------------- \__RB__)
     /       Build menu           Ctrl Groups Menu   \
    / Camera                                          \
   /  (LS)         Doctrines     Pause      Ability Menu
  /                  (SEL)       (ST.)           (Y)    \
 /         Quick Icons                                   \
|              _                             (X)     (B)  |
|    Action  _| |_  View             Attack Move       Move
|     Menu  |_   _| Info        (RS)             (A)      |
|             |_|            Zoom/Rotate        Select    |
|           Camera                                        |
|          Positions.-----------------.                   |
 \              _.-'                   '-._              /
  \          .-'                           '-.          /
```

### Main
- **LS**: Camera/Cursor
- **LS CLICK**: Center camera on conyard
- **RS UP/DOWN**: Zoom
- **RS LEFT/RIGHT**: Rotate structure
- **RS CLICK**: Unused
- **A**: Select unit (left click)
- **B**: Command unit (right click)
- **X**: Attack move
- **Y**: Ability/support powers/upgrades wheel

- **LB**: Build wheel
- **RB**: Control groups wheel
- **LB+RB**: Unit selection wheel
- **LT**: Minimap / Fast pan (by holding A)
- **RT**: Shift

- **DPAD UP**: Quick icons menu
- **DPAD LEFT**: Actions menu
- **DPAD RIGHT**: Info menu
- **DPAD DOWN**: Camera menu

- **SELECT**: Doctrines menu
- **START**: Pause

### Ability/Support Power/Upgrade Wheel (Y):
**Wheel**: abilities(5), support powers(5), upgrades(2)
- **LB**: cancel / toggle auto-cast (right click)
- **RB**: use (left click)

- **DPAD LEFT**: Subselect previous (shift+tab)
- **DPAD RIGHT**: Subselect next (tab)

### Control Groups Wheel (RB):
**Wheel**: choose control group number 1-8
- **A**: Select group (double tap to center camera)
- **B**: Set group
- **X**: Add to group
- **Y**: Steal group

- **DPAD UP**: Select all army on screen
- **DPAD LEFT**: Select all units of type
- **DPAD RIGHT**: Center camera on army
- **DPAD DOWN**: Select all army


### Build Wheel (LB):
**Wheel**: choose unit to produce (outer), production type (inner)
- **A**: Train (hold RT)
- **B**: Pause/Cancel
- **X**: Select all structures from production tab (for setting rally points)
- **Y**: Switch Tab

- **DPAD UP**: Sell Tool
- **DPAD LEFT**: Repair Tool
- **DPAD RIGHT**: Power On/Off Tool
- **DPAD DOWN**: Place Structure (Dynasty only)

### Selection Wheel (LB+RB):
**Wheel**: choose unit from current selection
- **A**: Pick unit from selection
- **B**: Remove unit from selection
- **X**: Expand/collapse selection
- **Y**: Center camera on unit

- **DPAD UP**: Previous page
- **DPAD DOWN**: Next page

### Minimap (LT):
- **LS**: move cursor around minimap
- **A**: Jump to position (you can also hold A while moving LS)

### Quick Icons Menu (DPAD UP):
This menu is for quick-selecting specialists, harvesters, caretakers (veti), and superweapons
- **ABYX**: click on icon
- **LB**: Previous Page
- **RB**: Next Page

### Actions Menu (DPAD LEFT):
- **A**: Stop
- **B**: Hold Position
- **X**: Guard
- **Y**: Patrol
- **LB**: Toggle formation move (a little bugged)
- **RB**: Toggle attack/assault move (a little bugged)

### Info Menu (DPAD RIGHT):
This menu is for viewing tooltip information
- **B**: View power tooltip
- **Y**: View population tooltip
- **LB**: Previous unit info
- **RB**: Next unit info

### Camera Menu (DPAD DOWN):
- **ABYZ**: camera location 1/2/3/4
- **LB/RB**: Hold to save camera location instead of jumping to cameraa location

### Doctrines Menu (SELECT):
- **SELECT**: Close doctrines menu
- **DPAD**: Navigate doctrines menu
- **A**: Buy doctrine
- **B**: Sell doctrine
- **X**: Buy doctrine from current column


# Some Limitations/Bugs
1. I have only tested this on an Xbox series X controller.
2. The interface currently only works on 16:9 screens
3. Sometimes, you lose control of the camera after closing the LT, LB, RB or Y menu. To fix this, press LT, LB, RB or Y again.
4. The formation move is a little buggy.
	- The formation move makes you hold ALT while giving move/attack move commands, which makes direct attack commands not work because holding ALT and right clicking on a unit is a crush move command, not a formation direct attack command.

# Comparison to a Native Implementation
This section discusses some of the limitations of the program compared to if controller controls were implemented directly into the game.

Because this is an input translation and inputting keyboard+mouse commands too quickly in tempest rising can cause it to drop inputs, combo commands like CTRL+A+LEFTCLICK require intentional delays to be inserted between the keypresses, which leads to a slight input delay when using this controller interface (even though you are pressing only one button on the controller).

The interface reads screen data to display icons on the wheels (e.g. unit icons). Because this is not directly part of the game's renderer, so that my overlay does not impact performance too much, I use a relatively slow refresh rate for the icons (so unit production progress will refresh at a low fps). It also looks a little more janky/ugly than it should be.

Due to limitations in what I can do with the overlay, I had to make a few compromises with some of the features. They are described below:

### Cursor magnetism
- Cursor magnetism is when the cursor at the center of the screen slightly gravitates towards and sticks to nearby units, which makes it easier to select units. This is usually also adjustable.
- My control scheme has no awareness of unit or building locations, so I can't implement cursor magnetism.

### Brush select
- In brush select, holding A should generate a slowly-expanding circle that shift-selects all units you brush over. This should work even while panning the camera.
- The brush circle delay and expansion rate should also be adjustable.
- The closest I could do to having something similar to brush select is to rapidly do shift-box selects of increasing size while you hold A.
- Because of the double-click bug, I cannot box select too quickly, so the brush select will also be a lot less sensitive than it should be.

### Minimap quick pan
- Holding LT (and A) should allow you to quick-pan around the map while looking at an expanded minimap.
- There is a subtle difference between my implementation and the correct implementation. In the correct implementation, if you hold LT, the cursor should start at where your camera currently is on the minimap. I can't access that information, so in my implementation, the cursor starts at where the cursor last was when you last closed the minimap.

### Quick icons
- Clicking on a quick icon (harvesters, specialists etc) should directly open their submenus.
	- I couldn't do this because the superweapon quick icon does not have a submenu, and I have no idea whether the player is clicking on the superweapon quick icon or something else.

### Tooltips
- Tooltips should display beside the wheel or on the wheel
	- My workaround is to make the mouse hover over the corresponding icon when pointing the thumbstick at the unit/ability/support power/upgrade, so that the tooltip appears.
	- Tooltips are important for the new player experience

### Info button
- The info button should display all of the information (e.g. power info) at the same time, instead of making the player click buttons to view it. This is not something I can do with Tempest Rising's current interface.

### Right Thumbstick
- Right thumbstick should function as both camera rotate and building rotate. I can't make it do both, so it is currently only building rotate.


