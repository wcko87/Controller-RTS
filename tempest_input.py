import inputs
from win32api import keybd_event, mouse_event, GetCursorPos, GetKeyState
import pydirectinput # currently I import this only for shift. This uses ctypes.windll.user32.SendInput which works
import math
import statistics
import time
import sys
from vk_keys import VK_KEYS

import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from win32api import GetSystemMetrics
import win32gui
import win32con
import win32gui

import ctypes

import mss

VERBOSITY_WARN = 1
VERBOSITY_ERROR = 2

PRINT_VERBOSITY = VERBOSITY_ERROR
def log_error(message, verbosity=VERBOSITY_ERROR):
    if verbosity >= PRINT_VERBOSITY:
        print(message)

def log_key(*message):
    pass
    #print(message)

HOTKEY_MAPPING_FILE = 'hotkey_mapping.txt'
if len(sys.argv) > 1:
    HOTKEY_MAPPING_FILE = sys.argv[1]

HIDE_OVERLAY_KEY = 0x13 # PAUSE BUTTON

# Default keys
KEY_HOME_BASE = 'LS'
KEY_CENTER_MOUSE = 'RS'
KEY_LEFT_CLICK = 'A'
KEY_RIGHT_CLICK = 'B'
KEY_ATTACK_MOVE = 'X'

KEY_ABILITY_SELECTOR = 'Y'
KEY_BUILD_SELECTOR = 'LB'
KEY_CONTROL_GROUP_SELECTOR = 'RB'

KEY_MINIMAP_MOUSE = 'LT'
KEY_SHIFT = 'RT'

# KEY_TOOL_SELECTOR = 'DPAD_U'
KEY_ACTION_SELECTOR = 'DPAD_L'
KEY_CAMERA_LOCATIONS = 'DPAD_D'
KEY_ICON_SELECTOR = 'DPAD_U'
KEY_INFO_SELECTOR = 'DPAD_R'
#KEY_SELECT_TYPE = 'DPAD_R'

KEY_PAUSE = 'START'
KEY_DOCTRINES = 'SEL'

KEY_ROTATE_LEFT = 'RS_L'
KEY_ROTATE_RIGHT = 'RS_R'

# Ability Selector keys
#KEY_ABILITY_USE = 'LB'
#KEY_SUPPORT_USE = 'RB'
KEY_ABILITY_USE = 'RB'
KEY_ABILITY_ALT_USE = 'LB'

KEY_ABILITY_UPGRADE_1 = 'DPAD_U'
KEY_ABILITY_UPGRADE_2 = 'DPAD_D'


# Action Selector keys
KEY_ACTION_GUARD = 'X'
KEY_ACTION_PATROL = 'Y'
KEY_ACTION_HOLD_POSITION = 'B'
KEY_ACTION_STOP = 'A'
#KEY_ACTION_ASSAULT_MOVE = 'LB'
#KEY_ACTION_ATTACK_MOVE = 'RB'
KEY_ACTION_TOGGLE_ASSAULT = 'RB'
KEY_ACTION_TOGGLE_FORMATIONS = 'LB'

# Control Groups Selector Keys
KEY_GROUP_SELECT = 'A'
KEY_GROUP_SET = 'B'
KEY_GROUP_ADD = 'X'
KEY_GROUP_STEAL = 'Y'

KEY_GROUP_LOCAL_UNITS = 'DPAD_U'
KEY_GROUP_ALL_UNITS_OF_TYPE = 'DPAD_L'
KEY_GROUP_ALL_UNITS = 'DPAD_D'
KEY_GROUP_LAST_NOTIFICATION = 'DPAD_R'

# Tab/Build Selector Keys
KEY_BUILD_TRAIN = 'A'
KEY_BUILD_CANCEL = 'B'
KEY_BUILD_SWITCHTAB = 'Y'
#KEY_BUILD_RALLYPOINT = 'X'
KEY_BUILD_SELECT_STRUCTURES = 'X'

KEY_BUILD_REPAIR = 'DPAD_L'
KEY_BUILD_SELL = 'DPAD_U'
KEY_BUILD_POWER = 'DPAD_R'
KEY_BUILD_PLACE_STRUCTURE = 'DPAD_D'

# Unit Selections Selector Keys
KEY_SELECTION_SELECT_ONLY = 'A'
KEY_SELECTION_REMOVE = 'B'
KEY_SELECTION_SELECT_TYPE = 'X'
KEY_SELECTION_REMOVE_TYPE = 'Y'

KEY_SELECTION_SCROLL_UP = 'DPAD_U'
KEY_SELECTION_SCROLL_DOWN = 'DPAD_D'
KEY_SELECTION_TAB_FORWARD = 'DPAD_R'
KEY_SELECTION_TAB_BACKWARD = 'DPAD_L'

# Camera Locations Selector Keys
KEY_CAMERA_1 = 'A'
KEY_CAMERA_2 = 'B'
KEY_CAMERA_3 = 'X'
KEY_CAMERA_4 = 'Y'

KEY_CAMERA_SAVE = 'LB'
KEY_CAMERA_SAVE_2 = 'RB'

# Info Selector Keys
KEY_INFO_NEXT = 'RB'
KEY_INFO_PREV = 'LB'
KEY_INFO_POWER = 'B'
KEY_INFO_POPULATION = 'Y'

# Icon selector Keys
KEY_ICON_NEXT = 'RB'
KEY_ICON_PREV = 'LB'
KEY_ICON_1 = 'A'
KEY_ICON_2 = 'B'
KEY_ICON_3 = 'Y'
KEY_ICON_4 = 'X'

# Doctrine selector Keys
KEY_DOCTRINES_UP = 'DPAD_U'
KEY_DOCTRINES_DOWN = 'DPAD_D'
KEY_DOCTRINES_LEFT = 'DPAD_L'
KEY_DOCTRINES_RIGHT = 'DPAD_R'
KEY_DOCTRINES_BUY = 'A'
KEY_DOCTRINES_CANCEL = 'B'
KEY_DOCTRINES_BUY_COLUMN = 'X'


STICK_DEADZONE = 0.10**2
STICK_RADIALMENU_THRESHOLD = 0.45**2

MOUSE_SENSITIVITY_ADJUSTMENT = 1.6

KEY_INPUT_INTERVAL = 0.02
KEY_INPUT_INTERVAL_MMB = KEY_INPUT_INTERVAL*2

SWAP_ATTACK_ASSAULT_MOVE_HOTKEYS = True
FORMATION_MOVE_DEFAULT = False


HOTKEYS_TO_MAP = {
    'home_base',
    'last_notification',
    'place_structure',
    'all_units',
    'local_units',
    #'all_units_of_type',
    'repair',
    'sell',
    'power',
    'ability_1',
    'ability_2',
    'ability_3',
    'ability_4',
    'ability_5',
    'support_1',
    'support_2',
    'support_3',
    'support_4',
    'support_5',
    'attack',
    'stop',
    'guard',
    'patrol',
    'hold_position',
    'tab_structures',
    'tab_defensive',
    'tab_infantry',
    'tab_vehicles',
    'tab_aircraft',
    'pause',
    'tab',
    'rotate_left',
    'rotate_right',
    'doctrine_column_1',
    'doctrine_column_2',
    'doctrine_column_3',
    'camera_location_1',
    'camera_location_2',
    'camera_location_3',
    'camera_location_4',
}

def read_hotkey_mapping(file_name):
    with open(file_name) as f:
        lines = f.read().split('\n')
    mapping = {}
    has_error = False
    for line in lines:
        if ':' not in line: continue
        hotkey, value = line.split(':', 1)
        tokens = [s.strip() for s in value.split(',')]
        if hotkey not in HOTKEYS_TO_MAP:
            log_error(f'Unknown command: {hotkey}', VERBOSITY_ERROR)
            has_error = True
        for token in tokens:
            if token not in VK_KEYS:
                log_error(f'Unknown key: "{token}" for {hotkey}', VERBOSITY_ERROR)
                has_error = True
        if len(tokens) == 1:
            mapping[hotkey] = tokens[0]
        else:
            mapping[hotkey] = tokens
    for hotkey in HOTKEYS_TO_MAP:
        if hotkey not in mapping:
            log_error(f'Unmapped command: {hotkey}', VERBOSITY_ERROR)
            has_error = True
    if has_error:
        log_error('Errors found in configuration file. exiting...', VERBOSITY_ERROR)
        quit(1)
    return mapping

HOTKEY_MAPPING = read_hotkey_mapping(HOTKEY_MAPPING_FILE)
PRODUCTION_TABS = ['tab_structures','tab_defensive','tab_infantry','tab_vehicles','tab_aircraft']

def mouse_down(button):
    if button == 'LMB':
        mouse_event(0x0002, 0, 0)
    elif button == 'RMB':
        mouse_event(0x0008, 0, 0)
    elif button == 'MMB':
        mouse_event(0x0020, 0, 0)

def mouse_up(button):
    if button == 'LMB':
        mouse_event(0x0004, 0, 0)
    elif button == 'RMB':
        mouse_event(0x0010, 0, 0)
    elif button == 'MMB':
        mouse_event(0x0040, 0, 0)

# positive means scroll up. Typical values around 10?. It doesn't seem to matter in TR though.
def mouse_wheel(amount):
    mouse_event(0x0800, 0, 0, round(amount))

def key_down(key):
    # NOTE: keybd_event DOES NOT WORK FOR SHIFT. USE SHIFTMANAGER INSTEAD
    keybd_event(VK_KEYS[key], 0, 0, 0)
    #print('press', key);return
    log_key('press', key)
    #if key == 'LMB':
        #mouse_event(0x02, 0, 0)
    #elif key == 'RMB':
        #mouse_event(0x08, 0, 0)
    #elif key == 'MMB':
        #mouse_event(0x20, 0, 0)
    #else:
        #keybd_event(VK_KEYS[key], 0, 0, 0)

def key_up(key):
    # NOTE: keybd_event DOES NOT WORK FOR SHIFT. USE SHIFTMANAGER INSTEAD
    keybd_event(VK_KEYS[key], 0, 2, 0)
    #print('release', key);return
    log_key('release', key)
    #if key == 'LMB':
        #mouse_event(0x04, 0, 0)
    #elif key == 'RMB':
        #mouse_event(0x10, 0, 0)
    #elif key == 'MMB':
        #mouse_event(0x40, 0, 0)
    #else:
        #keybd_event(VK_KEYS[key], 0, 2, 0)

def hold_key(key):
    def func():
        key_down(key)
    return func

def release_key(key):
    def func():
        key_up(key)
    return func

def press_key_combo(combo):
    if type(combo) == str:
        def func():
            #print('press combo', combo)
            key_down(combo)
            time.sleep(KEY_INPUT_INTERVAL)
            key_up(combo)
        return func

    def func():
        #print('press combo', combo)
        keys_held = []
        for key in combo:
            if key == None:
                for k in keys_held:
                    key_up(k)
                    #time.sleep(KEY_INPUT_INTERVAL)    
                keys_held.clear()
            else:
                key_down(key)
                keys_held.append(key)
                time.sleep(KEY_INPUT_INTERVAL)                
        for k in keys_held:
            key_up(k)
            #time.sleep(KEY_INPUT_INTERVAL)    
    return func

def input_hotkey(hotkey):
    return press_key_combo(HOTKEY_MAPPING[hotkey])

def clamp(value,low,high):
    return max(low,min(high,value))

class ShiftManager(object):
    SOURCE_SHIFTBUTTON = 1
    SOURCE_BRUSHSELECT = 2
    # Manages the holding and releasing of shift.
    def __init__(self):
        self.sources = {}
        self.held = False

    def __del__(self):
        pydirectinput.keyUp('shiftleft')

    def press(self, source=None):
        if source != None:
            self.sources[source] = True
        pydirectinput.keyDown('shiftleft')
        self.held = True
        #print('press shift')

    def release(self, source=None):
        if source != None:
            self.sources[source] = False
        if not any(self.sources.values()):
            pydirectinput.keyUp('shiftleft')
            self.held = False
            #print('release shift')
        #else:
            #print('did not release')

    def refresh(self):
        if any(self.sources.values()):
            pydirectinput.keyDown('shiftleft')
            self.held = True


class MouseManager(object):
    def __init__(self, shift_manager):
        self.shift_manager = shift_manager
        self.screen_width = GetSystemMetrics(0)
        self.screen_height = GetSystemMetrics(1)
        self.tr_xywh = get_tr_window_rect()

        self.current_mouse_x = self.tr_xywh[2]//2
        self.current_mouse_y = self.tr_xywh[3]//2

        self.holding_lmb = False
        self.brush_started = False

        self.middle_mouse_down = False
        self.wait_before_next_button_press = False
        self.wait_before_next_movement = False

        self.minimap_open = False
        self.minimap_mouse_down = False

        #self.MINIMAP_SIDELENGTH = TR_BOXES['minimap'][2]
        #self.MINIMAP_SIDELENGTH = self.tr_xywh[3]*113/180

        self.MINIMAP_X1 = round(TR_BOXES['minimap'][0]*self.tr_xywh[2]/1920)+1
        self.MINIMAP_Y1 = round(TR_BOXES['minimap'][1]*self.tr_xywh[2]/1920)+2
        self.MINIMAP_X2 = round((TR_BOXES['minimap'][0]+TR_BOXES['minimap'][2])*self.tr_xywh[2]/1920)-1
        self.MINIMAP_Y2 = round((TR_BOXES['minimap'][1]+TR_BOXES['minimap'][3])*self.tr_xywh[2]/1920)-1
        self.MINIMAP_BANNED_REGION_WIDTH = math.ceil(self.tr_xywh[3]*0.014)
        self.minimap_mouse_x = (self.MINIMAP_X1 + self.MINIMAP_X2)/2
        self.minimap_mouse_y = (self.MINIMAP_Y1 + self.MINIMAP_Y2)/2

        self.MINIMAP_CURSOR_SPEED = 10

        self.brush_hold_start_time = -1
        self.last_brush_time = -1
        self.BRUSH_CYCLE_TIME = 0.35 # to avoid the doubleclick bug
        #self.BRUSH_CYCLE_TIME = 0.25
        self.BRUSH_MAX_TIME = 1
        self.BRUSH_MAX_WIDTH = 0.40
        self.BRUSH_MAX_HEIGHT = 0.35
        self.BRUSH_MIN_TIME = 0.2
        self.BRUSH_MIN_WIDTH = 0.15
        self.BRUSH_MIN_HEIGHT = self.BRUSH_MIN_WIDTH*self.BRUSH_MAX_HEIGHT/self.BRUSH_MAX_WIDTH

        self.BRUSH_MOUSE_TOLERANCE = 200

        self.pan_frame = 0

    def __del__(self):
        mouse_up('LMB')
        mouse_up('RMB')
        mouse_up('MMB')

    def move_mouse(self, thumb_x, thumb_y, slow_move=False):
        if thumb_x**2 + thumb_y**2 <= STICK_DEADZONE:
            self._disarm_for_both()
            #self.pan_frame = 0
            #self.center_mouse()
            return
        if self.minimap_open: #TODO: REMOVE THIS FALLBACK IF THIS BRANCH IS NEVER USED
            self.move_mouse_minimap(thumb_x, thumb_y, slow_move=slow_move)
            return
        return
        dist = self.screen_height*0.0001
        angle = math.atan2(thumb_y, thumb_x)
        mag = (thumb_x**2 + thumb_y**2) * dist
        if slow_move:
            self.pan_camera_kb(mag*math.cos(angle), -mag*math.sin(angle))
        else:
            self.pan_camera(mag*math.cos(angle), -mag*math.sin(angle))

    def move_mouse_minimap(self, thumb_x, thumb_y, slow_move=False):
        if thumb_x**2 + thumb_y**2 <= STICK_DEADZONE:
            self._disarm_for_both()
            return
        self.minimap_mouse_x = clamp(self.minimap_mouse_x + thumb_x*self.MINIMAP_CURSOR_SPEED, self.MINIMAP_X1, self.MINIMAP_X2)
        self.minimap_mouse_y = clamp(self.minimap_mouse_y - thumb_y*self.MINIMAP_CURSOR_SPEED, self.MINIMAP_Y1, self.MINIMAP_Y2)

        tr_distance_x = self.MINIMAP_X2 - self.minimap_mouse_x
        tr_distance_y = self.minimap_mouse_y - self.MINIMAP_Y1
        #print(tr_distance_x, tr_distance_y)
        if max(tr_distance_x, tr_distance_y) < self.MINIMAP_BANNED_REGION_WIDTH:
            if tr_distance_x > tr_distance_y:
                self.minimap_mouse_x = self.MINIMAP_X2 - self.MINIMAP_BANNED_REGION_WIDTH
            else:
                self.minimap_mouse_y = self.MINIMAP_Y1 + self.MINIMAP_BANNED_REGION_WIDTH
        #print(thumb_x, thumb_y, self.minimap_mouse_x, self.minimap_mouse_y)
        if self.minimap_mouse_down:
            self.update_minimap_mouse_position()

    def update_minimap_mouse_position(self):
        if not self.minimap_open: return
        self._teleport_mouse(self.minimap_mouse_x, self.minimap_mouse_y)

    def open_minimap(self):
        self.release_lmb(MODE_MINIMAP)
        #print('open minimap')
        self.minimap_open = True
        #self.update_minimap_mouse_position()
        self._teleport_mouse_to_center()
        #mouse_down('LMB')

    def close_minimap(self):
        #print('close minimap')
        self.minimap_open = False
        if self.minimap_mouse_down:
            mouse_up('LMB')
        self.update_mouse_position()


    """
    def move_mouse_old(self, thumb_x, thumb_y):
        if thumb_x**2 + thumb_y**2 <= STICK_DEADZONE: return
        self.current_mouse_x = clamp(self.current_mouse_x + thumb_x*CURSOR_SPEED, 1, self.tr_xywh[2]-1)
        self.current_mouse_y = clamp(self.current_mouse_y - thumb_y*CURSOR_SPEED, 1, self.tr_xywh[3]-1)
        #print(thumb_x, thumb_y, self.current_mouse_x, self.current_mouse_y)
        self.update_mouse_position()
    """

    def center_mouse(self): 
        self.current_mouse_x = self.tr_xywh[2]//2
        self.current_mouse_y = self.tr_xywh[3]//2
        self.update_mouse_position()

    def hover_box_fun(self, xywh):
        target_x = self.tr_xywh[2]/1920 * (xywh[0] + xywh[2]/2)
        target_y = self.tr_xywh[3]/1080 * (xywh[1] + xywh[3]/2)
        def fun():
            self._teleport_mouse(target_x, target_y)
        return fun

    def hover_box(self, xywh):
        target_x = self.tr_xywh[2]/1920 * (xywh[0] + xywh[2]/2)
        target_y = self.tr_xywh[3]/1080 * (xywh[1] + xywh[3]/2)
        self._teleport_mouse(target_x, target_y)

    def update_mouse_position(self):
        if self.minimap_open or self.holding_lmb: return
        self._teleport_mouse(self.current_mouse_x, self.current_mouse_y)

    def click_button(self, xywh, button, keep_position_after=False):
        target_x = self.tr_xywh[2]/1920 * (xywh[0] + xywh[2]/2)
        target_y = self.tr_xywh[3]/1080 * (xywh[1] + xywh[3]/2)

        self._teleport_mouse(target_x, target_y)
        mouse_down(button)
        time.sleep(KEY_INPUT_INTERVAL)
        mouse_up(button)
        time.sleep(KEY_INPUT_INTERVAL)
        if not keep_position_after:
            self.update_mouse_position()

    def _teleport_mouse_to_center(self):
        self._teleport_mouse(self.tr_xywh[2]/2, self.tr_xywh[3]/2)

    def _teleport_mouse(self, x, y, add_flag=0):
        # x, y are relative to tr's window
        curr_x, curr_y = GetCursorPos()
        if abs(curr_x - self.tr_xywh[0] - x) <= 2 and abs(curr_y - self.tr_xywh[1] - y) <= 2:
            return
        mouse_x = round(65535 * (self.tr_xywh[0] + x) / self.screen_width)
        mouse_y = round(65535 * (self.tr_xywh[1] + y) / self.screen_height)
        self._disarm_for_movement()
        mouse_event(0x8001 | add_flag, mouse_x, mouse_y)
        self._mouse_moved_in_current_frame()


    def _mouse_moved_in_current_frame(self):
        self.wait_before_next_button_press = True

    def _mouse_released_in_current_frame(self):
        self.wait_before_next_movement = True

    def _disarm_for_movement(self):
        if self.middle_mouse_down:
            mouse_up('MMB')
            self.middle_mouse_down = False
            self.wait_before_next_button_press = False
            self.wait_before_next_movement = False
            time.sleep(KEY_INPUT_INTERVAL_MMB)
        elif self.wait_before_next_movement:
            self.wait_before_next_button_press = False
            self.wait_before_next_movement = False
            time.sleep(KEY_INPUT_INTERVAL)

    def _disarm_for_button_press(self):
        if self.middle_mouse_down:
            mouse_up('MMB')
            self.middle_mouse_down = False
            self.wait_before_next_button_press = False
            self.wait_before_next_movement = False
            time.sleep(KEY_INPUT_INTERVAL_MMB)
        elif self.wait_before_next_button_press:
            self.wait_before_next_button_press = False
            self.wait_before_next_movement = False
            time.sleep(KEY_INPUT_INTERVAL)

    def _disarm_for_both(self, except_middle_mouse=False):
        if not except_middle_mouse and self.middle_mouse_down:
            mouse_up('MMB')
            self.middle_mouse_down = False
            self.wait_before_next_button_press = False
            self.wait_before_next_movement = False
            time.sleep(KEY_INPUT_INTERVAL_MMB)
        elif self.wait_before_next_movement or self.wait_before_next_button_press:
            self.wait_before_next_button_press = False
            self.wait_before_next_movement = False
            time.sleep(KEY_INPUT_INTERVAL)

    def hold_lmb(self):
        if self.minimap_open:
            self.minimap_mouse_down = True
            self.update_minimap_mouse_position()
            self._disarm_for_button_press()
            mouse_down('LMB')
            return
        self.center_mouse()
        self.holding_lmb = True
        self.brush_started = False
        self.brush_hold_start_time = time.time()
        self.last_brush_time = -1

    def release_lmb(self, current_mode):
        if self.minimap_open:
            self.minimap_mouse_down = False
            mouse_up('LMB')
            self._teleport_mouse_to_center()
            return
        elif self.minimap_mouse_down:
            self.minimap_mouse_down = False
            mouse_up('LMB')
            return
        if self.brush_started:
            self.shift_manager.release(source=ShiftManager.SOURCE_BRUSHSELECT)
        elif self.holding_lmb:
            self.center_mouse()
            self._disarm_for_button_press()
            mouse_down('LMB')
            time.sleep(KEY_INPUT_INTERVAL)
            mouse_up('LMB')
        self.holding_lmb = False
        self.brush_started = False
        self.brush_hold_start_time = -1
        self.last_brush_time = -1
        if current_mode == MODE_DEFAULT:
            self.center_mouse()

    def mouse_click(self, button):
        if self.minimap_open:
            self.update_minimap_mouse_position()
            self._disarm_for_button_press()
        else:
            self.center_mouse()
        mouse_down(button)
        time.sleep(KEY_INPUT_INTERVAL)
        mouse_up(button)
        time.sleep(KEY_INPUT_INTERVAL)
        #self._mouse_released_in_current_frame()


    def pan_camera_kb(self, dx, dy):
        x_time = abs(dx)*KEY_INPUT_INTERVAL*7
        y_time = abs(dy)*KEY_INPUT_INTERVAL*7
        x_key = 'LEFT' if dx < 0 else 'RIGHT'
        y_key = 'UP' if dy < 0 else 'DOWN'
        if x_time < y_time:
            time_short, time_long, key_short, key_long = x_time, y_time, x_key, y_key
        else:
            time_short, time_long, key_short, key_long = y_time, x_time, y_key, x_key
        #pydirectinput.keyDown(key_short)
        key_down(key_short)
        key_down(key_long)
        #pydirectinput.keyDown(key_long)
        time.sleep(time_short)
        key_up(key_short)
        #pydirectinput.keyUp(key_short)
        time.sleep(time_long-time_short)
        key_up(key_long)
        #pydirectinput.keyUp(key_long)
        self.shift_manager.refresh()

    def _cursor_too_far_from_center(self):
        curr_x, curr_y = GetCursorPos()
        return abs(curr_x - self.tr_xywh[0] - self.tr_xywh[2]//2) >= self.tr_xywh[2]//16 or\
            abs(curr_y - self.tr_xywh[1] - self.tr_xywh[3]//2) >= self.tr_xywh[3]//16

    def pan_camera(self, dx, dy):
        mouse_dx = round(65535 * dx / self.screen_width)
        mouse_dy = round(65535 * dy / self.screen_height)

        if self._cursor_too_far_from_center():
            time.sleep(KEY_INPUT_INTERVAL)
            self._teleport_mouse(self.tr_xywh[2]//2 - 3*mouse_dx, self.tr_xywh[3]//2 - 3*mouse_dy)
            time.sleep(KEY_INPUT_INTERVAL)
            mouse_event(0x0021, 2*mouse_dx, 2*mouse_dy)
            #mouse_event(0x0021, -70, -70)
            #mouse_event(0x0021, 40, 40)
            #self.pan_frame = 0
        else:
            self._disarm_for_both(except_middle_mouse=True)
            mouse_event(0x0021, mouse_dx, mouse_dy)
            #self.pan_frame += 1
        #mouse_down('MMB')
        #mouse_down('MMB')
        #time.sleep(KEY_INPUT_INTERVAL)
        #mouse_event(0x0021, mouse_dx, mouse_dy)
        #time.sleep(KEY_INPUT_INTERVAL)
        #mouse_event(0x0041, -mouse_dx, -mouse_dy)
        self.middle_mouse_down = True
        #self.update_mouse_position()

    def update_brush_select(self):
        if not self.holding_lmb: return
        dt = time.time() - self.brush_hold_start_time
        if dt - self.last_brush_time <= self.BRUSH_CYCLE_TIME: return
        #if dt - self.last_brush_time <= 0.1: return
        if dt < self.BRUSH_MIN_TIME: return
        self.last_brush_time = dt
        if not self.brush_started:
            first = True
            self.brush_started = True
        else:
            first = False
            self.shift_manager.press(source=ShiftManager.SOURCE_BRUSHSELECT)
        box_x, box_y = self.brush_size(dt)

        tgt_diff_x, tgt_diff_y = box_x/2*self.tr_xywh[3], box_y/2*self.tr_xywh[3]
        curr_x, curr_y = GetCursorPos()
        diff_x = curr_x - self.tr_xywh[0] - self.tr_xywh[2]//2
        diff_y = curr_y - self.tr_xywh[1] - self.tr_xywh[3]//2

        #mouse_up('MMB')
        self._disarm_for_both()
        #time.sleep(KEY_INPUT_INTERVAL*3)

        if first or abs(abs(diff_x)-tgt_diff_x) + abs(abs(diff_y)-tgt_diff_y) > self.BRUSH_MOUSE_TOLERANCE:
            self._teleport_mouse(self.tr_xywh[2]//2 + tgt_diff_x, self.tr_xywh[3]//2 + tgt_diff_y)
            #print('reset')
            diff_x, diff_y = tgt_diff_x, tgt_diff_y
            time.sleep(KEY_INPUT_INTERVAL)
        #return

        #mouse_down('LMB')
        #time.sleep(KEY_INPUT_INTERVAL)
        #time.sleep(KEY_INPUT_INTERVAL)

        move_dx, move_dy = -math.copysign(abs(diff_x) + tgt_diff_x, diff_x), -math.copysign(abs(diff_y) + tgt_diff_y, diff_y)
        #print(diff_x, diff_y, move_dx, move_dy)
        mouse_event(0x03, round(MOUSE_SENSITIVITY_ADJUSTMENT*move_dx), round(MOUSE_SENSITIVITY_ADJUSTMENT*move_dy))
        time.sleep(KEY_INPUT_INTERVAL)

        mouse_up('LMB')
        self._mouse_released_in_current_frame()
        #mouse_down('MMB')
        #time.sleep(KEY_INPUT_INTERVAL)

    def brush_size(self, dt):
        ## assume dt >= self.BRUSH_MIN_TIME
        if dt >= self.BRUSH_MAX_TIME: return self.BRUSH_MAX_WIDTH, self.BRUSH_MAX_HEIGHT
        ratio = (dt-self.BRUSH_MIN_TIME)/(self.BRUSH_MAX_TIME-self.BRUSH_MIN_TIME)
        return self.BRUSH_MIN_WIDTH + ratio*(self.BRUSH_MAX_WIDTH-self.BRUSH_MIN_WIDTH),\
            self.BRUSH_MIN_HEIGHT + ratio*(self.BRUSH_MAX_HEIGHT-self.BRUSH_MIN_HEIGHT)

    def test_mouse_input(self):
        #box_w, box_h = 0.4, 0.4
        #mouse_dx = round(65535 * self.tr_xywh[2] * box_x / self.screen_width)
        #mouse_dy = round(65535 * self.tr_xywh[3] * box_y / self.screen_height)

        box_x = 0.4
        box_y = 0.4
        mouse_dx = round(self.tr_xywh[2] * box_x) #1600 * 0.4 = 640 (actual movement: 400, 1.6x less, cursor speed 7)
        mouse_dy = round(self.tr_xywh[3] * box_y)
        self._teleport_mouse(self.tr_xywh[2]*0.3, self.tr_xywh[3]*0.3) #(1600 * 0.3 + 160) / 1920 * 65535
        time.sleep(KEY_INPUT_INTERVAL)
        mouse_down('LMB')
        time.sleep(KEY_INPUT_INTERVAL)
        mouse_event(0x0001, mouse_dx, mouse_dy)
        time.sleep(0.5)
        mouse_up('LMB')
        self.update_mouse_position()


def no_action():
    pass

MODE_ANY = -1
MODE_DEFAULT = 0
MODE_GROUPS = 1
MODE_BUILD = 2
MODE_ABILITY = 3
MODE_SELECTION = 4
MODE_ACTION = 5
MODE_CAMERA = 6
MODE_INFO = 7
MODE_ICONS = 8
MODE_MINIMAP = 9
MODE_DOCTRINES = 10

class InputTranslator(object):

    def define_inputs(self):
        self.ANGLES_ABILITIES_WHEEL = {
            -1: no_action,
            0: input_hotkey('ability_1'),
            1: input_hotkey('ability_2'),
            2: input_hotkey('ability_3'),
            3: input_hotkey('ability_4'),
            4: input_hotkey('ability_5'),
            5: lambda: self.mouse_manager.click_button(TR_BOXES['upgrade1'], 'LMB'),
            6: lambda: self.mouse_manager.click_button(TR_BOXES['upgrade2'], 'LMB'),
            7: input_hotkey('support_5'),
            8: input_hotkey('support_4'),
            9: input_hotkey('support_3'),
            10: input_hotkey('support_2'),
            11: input_hotkey('support_1'),
        }
        self.ANGLES_ABILITIES_WHEEL_ALT = {
            -1: no_action,
            0: lambda: self.mouse_manager.click_button(TR_BOXES['ability1'], 'RMB'),
            1: lambda: self.mouse_manager.click_button(TR_BOXES['ability2'], 'RMB'),
            2: lambda: self.mouse_manager.click_button(TR_BOXES['ability3'], 'RMB'),
            3: lambda: self.mouse_manager.click_button(TR_BOXES['ability4'], 'RMB'),
            4: lambda: self.mouse_manager.click_button(TR_BOXES['ability5'], 'RMB'),
            5: lambda: self.mouse_manager.click_button(TR_BOXES['upgrade1'], 'RMB'),
            6: lambda: self.mouse_manager.click_button(TR_BOXES['upgrade2'], 'RMB'),
            7: lambda: self.mouse_manager.click_button(TR_BOXES['support1'], 'RMB'),
            8: lambda: self.mouse_manager.click_button(TR_BOXES['support2'], 'RMB'),
            9: lambda: self.mouse_manager.click_button(TR_BOXES['support3'], 'RMB'),
            10: lambda: self.mouse_manager.click_button(TR_BOXES['support4'], 'RMB'),
            11: lambda: self.mouse_manager.click_button(TR_BOXES['support5'], 'RMB'),
        }
        self.OFFSET_ABILITIES_WHEEL = 0.5
        self.NUM_ABILITY_ICONS = max(self.ANGLES_ABILITIES_WHEEL)+1

        #self.ANGLES_ABILITY_WHEEL = {
            #-1: no_action,
            #0: input_hotkey('ability_1'),
            #1: input_hotkey('ability_2'),
            #2: input_hotkey('ability_3'),
            #3: input_hotkey('ability_4'),
            #4: input_hotkey('ability_5'),
        #}
        #self.NUM_ABILITIES = max(self.ANGLES_ABILITY_WHEEL)+1
        #self.ANGLES_SUPPORT_WHEEL = {
            #-1: no_action,
            #0: input_hotkey('support_1'),
            #1: input_hotkey('support_2'),
            #2: input_hotkey('support_3'),
            #3: input_hotkey('support_4'),
            #4: input_hotkey('support_5'),
        #}
        #self.NUM_SUPPORT_POWERS = max(self.ANGLES_SUPPORT_WHEEL)+1

        self.ANGLES_TAB_WHEEL = {
            -1: no_action,
            0: input_hotkey('tab_structures'),
            1: input_hotkey('tab_defensive'),
            2: input_hotkey('tab_infantry'),
            3: input_hotkey('tab_vehicles'),
            4: input_hotkey('tab_aircraft'),
        }
        self.NUM_TABS = max(self.ANGLES_TAB_WHEEL)+1

        self.NUM_GROUPS = 8
        self.NUM_BUILD_ICONS = 12
        self.NUM_SELECTION_ICONS = 18
        self.NUM_CAMERAS = 4

        self.ON_PRESS = {
            MODE_ANY: {
                #KEY_MINIMAP_MOUSE: self.mouse_manager.open_minimap,
                KEY_SHIFT: lambda : self.shift_manager.press(source=ShiftManager.SOURCE_SHIFTBUTTON),
                KEY_PAUSE: input_hotkey('pause'),
            },
            MODE_MINIMAP: {
                KEY_HOME_BASE: input_hotkey('home_base'),
                KEY_LEFT_CLICK: self.mouse_manager.hold_lmb,
                KEY_RIGHT_CLICK: self.command_move,
                KEY_ATTACK_MOVE: self.command_attack_move,
            },
            MODE_DEFAULT: {
                KEY_MINIMAP_MOUSE: self.open_minimap,
                KEY_CENTER_MOUSE: self.mouse_manager.center_mouse,
                KEY_HOME_BASE: input_hotkey('home_base'),
                KEY_LEFT_CLICK: self.mouse_manager.hold_lmb,
                KEY_RIGHT_CLICK: self.command_move,
                KEY_ATTACK_MOVE: self.command_attack_move,
                KEY_ABILITY_SELECTOR: lambda: self.open_selector(MODE_ABILITY),
                KEY_CONTROL_GROUP_SELECTOR: lambda: self.open_selector(MODE_GROUPS),
                KEY_BUILD_SELECTOR: lambda: self.open_selector(MODE_BUILD),
                KEY_ACTION_SELECTOR: lambda: self.open_selector(MODE_ACTION),
                KEY_CAMERA_LOCATIONS: lambda: self.open_selector(MODE_CAMERA),
                KEY_INFO_SELECTOR: lambda: self.open_selector(MODE_INFO),
                KEY_ICON_SELECTOR: lambda: self.open_selector(MODE_ICONS),
                KEY_DOCTRINES: lambda: self.open_selector(MODE_DOCTRINES),
                KEY_ROTATE_LEFT: input_hotkey('rotate_left'),
                KEY_ROTATE_RIGHT: input_hotkey('rotate_right'),
            },
            MODE_ABILITY : {
                KEY_ABILITY_USE: self.click_ability_wheel(alt=False),
                KEY_ABILITY_ALT_USE: self.click_ability_wheel(alt=True),
            },
            MODE_ACTION : {
                KEY_ACTION_GUARD: input_hotkey('guard'),
                KEY_ACTION_PATROL: input_hotkey('patrol'),
                KEY_ACTION_HOLD_POSITION: input_hotkey('hold_position'),
                KEY_ACTION_STOP: input_hotkey('stop'),
                KEY_ACTION_TOGGLE_ASSAULT: self.toggle_assault_move,
                KEY_ACTION_TOGGLE_FORMATIONS: self.toggle_formations,
                #KEY_ACTION_ASSAULT_MOVE: input_hotkey('assault_move'),
                #KEY_ACTION_ATTACK_MOVE: input_hotkey('attack_move'),
            },
            MODE_GROUPS : {
                KEY_GROUP_SELECT: self.select_group,
                KEY_GROUP_ADD: self.add_group,
                KEY_GROUP_SET: self.create_group,
                KEY_GROUP_STEAL: self.steal_group,
                KEY_BUILD_SELECTOR: lambda: self.open_selector(MODE_SELECTION),

                KEY_GROUP_ALL_UNITS: input_hotkey('all_units'),
                KEY_GROUP_LOCAL_UNITS: input_hotkey('local_units'),
                KEY_GROUP_ALL_UNITS_OF_TYPE: self.select_all_units_of_type,
                KEY_GROUP_LAST_NOTIFICATION: input_hotkey('last_notification'),
                },
            MODE_BUILD : {
                KEY_BUILD_TRAIN: self.train_unit,
                KEY_BUILD_CANCEL: self.cancel_unit,
                KEY_BUILD_SWITCHTAB: self.switch_tab,
                #KEY_BUILD_RALLYPOINT: self.rally_point_tab,
                KEY_BUILD_SELECT_STRUCTURES: self.select_production_tab_structures,
                KEY_CONTROL_GROUP_SELECTOR: lambda: self.open_selector(MODE_SELECTION),

                KEY_BUILD_REPAIR: input_hotkey('repair'),
                KEY_BUILD_SELL: input_hotkey('sell'),
                KEY_BUILD_POWER: input_hotkey('power'),
                KEY_BUILD_PLACE_STRUCTURE: input_hotkey('place_structure'),
            },
            MODE_SELECTION : {
                KEY_SELECTION_SELECT_ONLY: lambda: self.click_selection_icon(ctrl=False, shift=False),
                KEY_SELECTION_REMOVE: lambda: self.click_selection_icon(ctrl=False, shift=True),
                #KEY_SELECTION_SELECT_TYPE: lambda: self.click_selection_icon(ctrl=True, shift=False),
                #KEY_SELECTION_REMOVE_TYPE: lambda: self.click_selection_icon(ctrl=True, shift=True),
                KEY_SELECTION_SCROLL_UP: lambda: self.mouse_manager.click_button(TR_BOXES['selection_uparrow'], 'LMB'),
                KEY_SELECTION_SCROLL_DOWN: lambda: self.mouse_manager.click_button(TR_BOXES['selection_downarrow'], 'LMB'),
                KEY_SELECTION_TAB_FORWARD: input_hotkey('tab'),
                KEY_SELECTION_TAB_BACKWARD: self.tab_backward,
            },
            MODE_CAMERA : {
                KEY_CAMERA_1: lambda: self.camera_location(0),
                KEY_CAMERA_2: lambda: self.camera_location(1),
                KEY_CAMERA_3: lambda: self.camera_location(2),
                KEY_CAMERA_4: lambda: self.camera_location(3),
                KEY_CAMERA_SAVE: no_action,
                KEY_CAMERA_SAVE_2: no_action,
            },
            MODE_INFO : {
                KEY_INFO_NEXT: self.info_viewer_menu.right,
                KEY_INFO_PREV: self.info_viewer_menu.left,
                KEY_INFO_POWER: self.mouse_manager.hover_box_fun(TR_BOXES['power_meter']),
                KEY_INFO_POPULATION: self.mouse_manager.hover_box_fun(TR_BOXES['population_hover']),
            },
            MODE_ICONS : {
                KEY_ICON_NEXT: self.icon_selector_menu.next_page,
                KEY_ICON_PREV: self.icon_selector_menu.prev_page,
                KEY_ICON_1: lambda: self.icon_selector_menu.click_icon(0),
                KEY_ICON_2: lambda: self.icon_selector_menu.click_icon(1),
                KEY_ICON_3: lambda: self.icon_selector_menu.click_icon(2),
                KEY_ICON_4: lambda: self.icon_selector_menu.click_icon(3),
            },
            MODE_DOCTRINES : {
                KEY_DOCTRINES: lambda: self.close_selector(MODE_DOCTRINES),
                KEY_DOCTRINES_UP: lambda: self.doctrine_menu.move(0,-1),
                KEY_DOCTRINES_DOWN: lambda: self.doctrine_menu.move(0,1),
                KEY_DOCTRINES_LEFT: lambda: self.doctrine_menu.move(-1,0),
                KEY_DOCTRINES_RIGHT: lambda: self.doctrine_menu.move(1,0),
                KEY_DOCTRINES_BUY: self.doctrine_menu.buy,
                KEY_DOCTRINES_CANCEL: self.doctrine_menu.cancel,
                KEY_DOCTRINES_BUY_COLUMN: self.doctrine_menu.buy_column,
            },
        }

        self.ON_RELEASE = {
            MODE_ANY: {
                #KEY_MINIMAP_MOUSE: self.mouse_manager.close_minimap,
                KEY_LEFT_CLICK: lambda: self.mouse_manager.release_lmb(self.current_mode),
                KEY_SHIFT: lambda : self.shift_manager.release(source=ShiftManager.SOURCE_SHIFTBUTTON),
            },
            MODE_MINIMAP: {
                KEY_MINIMAP_MOUSE: self.close_minimap,
            },
            MODE_DEFAULT: {
            },
            MODE_ABILITY : {
                KEY_ABILITY_SELECTOR: lambda: self.close_selector(MODE_ABILITY),
            },
            MODE_ACTION : {
                KEY_ACTION_SELECTOR: lambda: self.close_selector(MODE_ACTION),
            },
            MODE_GROUPS : {
                KEY_CONTROL_GROUP_SELECTOR: lambda: self.close_selector(MODE_GROUPS),
            },
            MODE_BUILD : {
                KEY_BUILD_SELECTOR: lambda: self.close_selector(MODE_BUILD),
            },
            MODE_SELECTION : {
                KEY_BUILD_SELECTOR: lambda: self.open_selector(MODE_GROUPS),
                KEY_CONTROL_GROUP_SELECTOR: lambda: self.open_selector(MODE_BUILD),
            },
            MODE_CAMERA : {
                KEY_CAMERA_LOCATIONS: lambda: self.close_selector(MODE_CAMERA),
            },
            MODE_INFO : {
                KEY_INFO_SELECTOR: lambda: self.close_selector(MODE_INFO),
            },
            MODE_ICONS : {
                KEY_ICON_SELECTOR: lambda: self.close_selector(MODE_ICONS),
            },
            MODE_DOCTRINES : {
            },
        }

        #self.ATTACK_MOVE = input_hotkey('attack_move')
        #self.ASSAULT_MOVE = input_hotkey('assault_move')
        #self.FORMATION_ATTACK_MOVE = input_hotkey('formation_attack_move')
        #self.FORMATION_ASSAULT_MOVE = input_hotkey('formation_assault_move')
        #self.MOVE = press_key_combo('RMB')
        #self.FORMATION_MOVE = input_hotkey('formation_move')

        self.SELECT_GROUP = [press_key_combo(str(i+1)) for i in range(self.NUM_GROUPS)]
        self.CREATE_GROUP = [press_key_combo(('LCONTROL', str(i+1))) for i in range(self.NUM_GROUPS)]
        self.STEAL_GROUP = [press_key_combo(('LMENU', str(i+1))) for i in range(self.NUM_GROUPS)]

        self.SAVE_CAMERA = [press_key_combo(('LCONTROL', HOTKEY_MAPPING['camera_location_'+str(i+1)]))
            for i in range(self.NUM_CAMERAS)]
        self.LOAD_CAMERA = [press_key_combo(HOTKEY_MAPPING['camera_location_'+str(i+1)])
            for i in range(self.NUM_CAMERAS)]


        self.HOVER_BUILD_WHEEL = {
            i: self.mouse_manager.hover_box_fun(TR_BOXES['prod%d'%(i+1)])
            for i in range(self.NUM_BUILD_ICONS)
        }

        self.HOVER_ABILITY_WHEEL = dict(
            [(i, self.mouse_manager.hover_box_fun(TR_BOXES['ability%d'%(i+1)])) for i in range(5)] +
            [(5+i, self.mouse_manager.hover_box_fun(TR_BOXES['upgrade%d'%(i+1)])) for i in range(2)] +
            [(11-i, self.mouse_manager.hover_box_fun(TR_BOXES['support%d'%(i+1)])) for i in range(5)]
        )

        self.HOVER_SELECTION_WHEEL = {
            i: self.mouse_manager.hover_box_fun(TR_BOXES['selection%d'%(i+1)])
            for i in range(self.NUM_SELECTION_ICONS)
        }

    def __init__(self):
        self.shift_manager = ShiftManager()
        self.input_status = None
        self.input_last_time = None
        self.zoom_ticks = 0
        self.current_mode = MODE_DEFAULT
        self.current_hover_option = None
        self.mouse_manager = MouseManager(self.shift_manager)
        self.doctrine_menu = DoctrineMenu(self)
        self.icon_selector_menu = IconSelectorMenu(self)
        self.info_viewer_menu = InfoViewerMenu(self)
        self.define_inputs()
        self.UPGRADE_DOUBLECLICK_INTERVAL = 0.4
        """
        self.last_upgrade_click_time = -1
        self.last_upgrade_button_click = 0
        """

        self.attack_buildings = False
        self.formation_move = False

        self.SUPPORT_POWER_PHASE_OFFSET = 0

    def left_stick_properties(self):
        keys = self.input_status
        magnitude = keys['left_analog_y']**2 + keys['left_analog_x']**2
        return magnitude**0.5, (magnitude >= STICK_RADIALMENU_THRESHOLD),\
            math.atan2(keys['left_analog_y'], keys['left_analog_x'])

    def left_stick_angle(self):
        keys = self.input_status
        magnitude = keys['left_analog_y']**2 + keys['left_analog_x']**2
        if magnitude < STICK_RADIALMENU_THRESHOLD:
            return None
        return math.atan2(keys['left_analog_y'], keys['left_analog_x']) * 180 / math.pi

    def left_stick_option(self, num_options, phase_offset=0):
        angle = self.left_stick_angle()
        if angle == None:
            option = -1
        else:
            option = int((angle/360*num_options + 0.5 - phase_offset) % num_options)
        return option

    def update_right_stick_movement(self, thumb_x, thumb_y):
        if thumb_x**2 + thumb_y**2 <= STICK_DEADZONE: return
        self.zoom_ticks += thumb_y*0.5
        while self.zoom_ticks > 1:
            mouse_wheel(1)
            self.zoom_ticks -= 1
        while self.zoom_ticks < -1:
            mouse_wheel(-1)
            self.zoom_ticks += 1

    def toggle_assault_move(self):
        self.attack_buildings = not self.attack_buildings

    def toggle_formations(self):
        self.formation_move = not self.formation_move

    def command_move(self):
        if self.formation_move == FORMATION_MOVE_DEFAULT:
            self.move_default()
        else:
            self.move_alt()

    def command_attack_move(self):
        if self.attack_buildings == SWAP_ATTACK_ASSAULT_MOVE_HOTKEYS:
            if self.formation_move == FORMATION_MOVE_DEFAULT:
                self.attack_move_default()
            else:
                self.attack_move_default_alt()
        else:
            if self.formation_move == FORMATION_MOVE_DEFAULT:
                self.attack_move_ctrl()
            else:
                self.attack_move_ctrl_alt()

    def attack_move_default(self):
        key_down(HOTKEY_MAPPING['attack'])
        time.sleep(KEY_INPUT_INTERVAL)
        key_up(HOTKEY_MAPPING['attack'])
        self.mouse_manager.mouse_click('LMB')

    def attack_move_ctrl(self):
        key_down('LCONTROL')
        self.mouse_manager.mouse_click('RMB')
        time.sleep(KEY_INPUT_INTERVAL)
        key_up('LCONTROL')

    def attack_move_default_alt(self):
        key_down(HOTKEY_MAPPING['attack'])
        time.sleep(KEY_INPUT_INTERVAL)
        key_down('LMENU')
        key_up(HOTKEY_MAPPING['attack'])
        self.mouse_manager.mouse_click('LMB')
        time.sleep(KEY_INPUT_INTERVAL)
        key_up('LMENU')

    def attack_move_ctrl_alt(self):
        key_down('LCONTROL')
        key_down('LMENU')
        self.mouse_manager.mouse_click('RMB')
        time.sleep(KEY_INPUT_INTERVAL)
        key_up('LCONTROL')
        key_up('LMENU')

    def move_default(self):
        self.mouse_manager.mouse_click('RMB')

    def move_alt(self):
        key_down('LMENU')
        self.mouse_manager.mouse_click('RMB')
        time.sleep(KEY_INPUT_INTERVAL)
        key_up('LMENU')

    def camera_location(self, index):
        save = self.input_status[KEY_CAMERA_SAVE] or self.input_status[KEY_CAMERA_SAVE_2]
        if save:
            self.SAVE_CAMERA[index]()
        else:
            self.LOAD_CAMERA[index]()

    def tab_backward(self):
        self.shift_manager.press()
        key_down(HOTKEY_MAPPING['tab'])
        time.sleep(KEY_INPUT_INTERVAL)
        key_up(HOTKEY_MAPPING['tab'])
        time.sleep(KEY_INPUT_INTERVAL)
        self.shift_manager.release()

    """
    def click_upgrade(self, num):
        t = time.time()
        if self.last_upgrade_button_click == num and t < self.last_upgrade_click_time + self.UPGRADE_DOUBLECLICK_INTERVAL:
            self.mouse_manager.click_button(TR_BOXES['upgrade%d'%num], 'RMB')
        else:
            self.mouse_manager.click_button(TR_BOXES['upgrade%d'%num], 'LMB')
        self.last_upgrade_click_time = t
        self.last_upgrade_button_click = num
    """

    def click_ability_wheel(self, alt=False):
        def fun():
            option = self.left_stick_option(self.NUM_ABILITY_ICONS, phase_offset=self.OFFSET_ABILITIES_WHEEL)
            if option == -1: return
            if alt:
                self.ANGLES_ABILITIES_WHEEL_ALT.get(option, no_action)()
            else:
                self.ANGLES_ABILITIES_WHEEL.get(option, no_action)()
        return fun
        
    """
    def use_ability(self):
        option = self.left_stick_option(self.NUM_ABILITIES)
        if option == -1: return
        self.ANGLES_ABILITY_WHEEL[option]()

    def use_support_power(self):
        option = self.left_stick_option(self.NUM_SUPPORT_POWERS, phase_offset=self.SUPPORT_POWER_PHASE_OFFSET)
        if option == -1: return
        self.ANGLES_SUPPORT_WHEEL[option]()
    """

    def click_selection_icon(self, ctrl, shift):
        option = self.left_stick_option(self.NUM_SELECTION_ICONS)
        if option == -1: return
        if ctrl: key_down('LCONTROL')
        if shift: self.shift_manager.press()
        #time.sleep(KEY_INPUT_INTERVAL)
        self.mouse_manager.click_button(TR_BOXES['selection%d'%(option+1)], 'LMB')
        time.sleep(KEY_INPUT_INTERVAL)
        if ctrl: key_up('LCONTROL')
        if shift: self.shift_manager.release()

    def create_group(self):
        option = self.left_stick_option(self.NUM_GROUPS)
        if option == -1: return
        self.CREATE_GROUP[option]()

    def select_group(self):
        option = self.left_stick_option(self.NUM_GROUPS)
        if option == -1: return
        self.SELECT_GROUP[option]()

    def add_group(self):
        option = self.left_stick_option(self.NUM_GROUPS)
        if option == -1: return
        key = str(option+1)
        self.shift_manager.press()
        key_down(key)
        time.sleep(KEY_INPUT_INTERVAL)
        key_up(key)
        time.sleep(KEY_INPUT_INTERVAL)
        self.shift_manager.release()
        #press_key_combo(('LSHIFT', str(option+1)))()

    def steal_group(self):
        option = self.left_stick_option(self.NUM_GROUPS)
        if option == -1: return
        self.STEAL_GROUP[option]()

    def select_all_units_of_type(self):
        self.shift_manager.press()
        key_down('S')
        time.sleep(KEY_INPUT_INTERVAL)
        key_up('S')
        time.sleep(KEY_INPUT_INTERVAL)
        self.shift_manager.release()


    def train_unit(self):
        option = self.left_stick_option(self.NUM_BUILD_ICONS)
        if option == -1: return
        press_key_combo('F%d' % (option+1))()

    def cancel_unit(self):
        option = self.left_stick_option(self.NUM_BUILD_ICONS)
        if option == -1: return
        self.mouse_manager.click_button(TR_BOXES['prod%d'%(option+1)], 'RMB')

    def switch_tab(self):
        option = self.left_stick_option(self.NUM_TABS)
        if option == -1: return
        self.ANGLES_TAB_WHEEL[option]()

    def rally_point_tab(self):
        option = self.left_stick_option(self.NUM_TABS)
        if option == -1: return
        key_down(HOTKEY_MAPPING[PRODUCTION_TABS[option]])
        mouse_down('LMB')
        time.sleep(KEY_INPUT_INTERVAL)
        mouse_up('LMB')
        time.sleep(KEY_INPUT_INTERVAL)
        key_up(HOTKEY_MAPPING[PRODUCTION_TABS[option]])

    def select_production_tab_structures(self):
        option = self.left_stick_option(self.NUM_TABS)
        if option == -1: return
        key_down('LCONTROL')
        self.ANGLES_TAB_WHEEL[option]()
        time.sleep(KEY_INPUT_INTERVAL)
        key_up('LCONTROL')

    def open_minimap(self):
        self.open_selector(MODE_MINIMAP)
        self.mouse_manager.open_minimap()

    def close_minimap(self):
        self.close_selector(MODE_MINIMAP)
        self.mouse_manager.close_minimap()

    def open_selector(self, mode):
        self.current_mode = mode
        #print('open selector', mode)
        if self.current_mode == MODE_INFO:
            self.info_viewer_menu.on_open()
        elif self.current_mode == MODE_ICONS:
            self.icon_selector_menu.on_open()
        elif self.current_mode == MODE_DOCTRINES:
            self.doctrine_menu.on_open()
        
    def close_selector(self, mode):
        if self.current_mode == mode:
            if self.current_mode == MODE_DOCTRINES:
                self.doctrine_menu.on_close()
            """
            if mode == MODE_ABILITY:
                option = self.left_stick_option(self.NUM_ABILITIES)
                self.ANGLES_ABILITY_WHEEL[option]()
            if mode == MODE_ACTION:
                option = self.left_stick_option(self.NUM_ACTIONS)
                self.ANGLES_ACTION_WHEEL[option]() 
            """
            self.current_mode = MODE_DEFAULT
        #print('close selector', mode)
        self.mouse_manager.center_mouse()
        
    def input_press(self, key, input_status, input_last_time):
        self.input_status = input_status
        self.input_last_time = input_last_time
        fun = self.ON_PRESS[MODE_ANY].get(key)
        if fun != None: fun()
        fun = self.ON_PRESS[self.current_mode].get(key)
        if fun != None: fun()
        
    def input_release(self, key, input_status, input_last_time):
        self.input_status = input_status
        self.input_last_time = input_last_time
        fun = self.ON_RELEASE[MODE_ANY].get(key)
        if fun != None: fun()
        fun = self.ON_RELEASE[self.current_mode].get(key)
        if fun != None: fun()

    def update_input(self, input_status, input_last_time):
        self.input_status = input_status
        self.input_last_time = input_last_time

    def update_hover(self, num_icons, hover_actions, phase_offset=0):
        option = self.left_stick_option(num_icons, phase_offset=phase_offset)
        if option != self.current_hover_option:
            if option == -1:
                self.mouse_manager.center_mouse()
            else:
                hover_actions[option]()

    def loop(self):
        in_s = self.input_status
        if self.current_mode == MODE_DEFAULT:
            self.mouse_manager.move_mouse(in_s['left_analog_x'], in_s['left_analog_y'], slow_move=in_s['RS'])
            self.mouse_manager.update_brush_select()
            self.update_right_stick_movement(in_s['right_analog_x'], in_s['right_analog_y'])
        elif self.current_mode == MODE_MINIMAP:
            self.mouse_manager.move_mouse_minimap(in_s['left_analog_x'], in_s['left_analog_y'], slow_move=in_s['RS'])
        elif self.current_mode == MODE_BUILD:
            self.update_hover(self.NUM_BUILD_ICONS, self.HOVER_BUILD_WHEEL)
        elif self.current_mode == MODE_ABILITY:
            self.update_hover(self.NUM_ABILITY_ICONS, self.HOVER_ABILITY_WHEEL, phase_offset=self.OFFSET_ABILITIES_WHEEL)
        elif self.current_mode == MODE_SELECTION:
            self.update_hover(self.NUM_SELECTION_ICONS, self.HOVER_SELECTION_WHEEL)

class DoctrineMenu(object):
    def __init__(self, input_translator):
        self.in_tr = input_translator
        self.select_x = 1
        self.select_y = 0

        self.COLUMN_BUY_ACTIONS = {
            0: input_hotkey('doctrine_column_1'),
            1: input_hotkey('doctrine_column_2'),
            2: input_hotkey('doctrine_column_3'),
        }

    def on_open(self):
        self.in_tr.mouse_manager.click_button(TR_BOXES['doctrines_panel'], 'LMB')
        self.hover_doctrine()

    def on_close(self):
        self.in_tr.mouse_manager.click_button(TR_BOXES['build_panel'], 'LMB')

    def move(self, dx, dy):
        self.select_x = clamp(self.select_x + dx, 0, 2)
        self.select_y = clamp(self.select_y + dy, 0, 5)
        self.hover_doctrine()

    def buy(self):
        self.in_tr.mouse_manager.click_button(doctrine_box(self.select_x,self.select_y), 'LMB', keep_position_after=True)

    def cancel(self):
        self.in_tr.mouse_manager.click_button(doctrine_box(self.select_x,self.select_y), 'RMB', keep_position_after=True)

    def buy_column(self):
        self.COLUMN_BUY_ACTIONS[self.select_x]()

    def hover_doctrine(self):
        self.in_tr.mouse_manager.hover_box(doctrine_box(self.select_x,self.select_y))

class InfoViewerMenu(object):
    def __init__(self, input_translator):
        self.in_tr = input_translator
        self.NUM_STATS = 4
        self.init()

        self.BBOXES = {
            0: TR_BOXES['unitportrait'],
            1: TR_BOXES['unitweapon'],
            2: TR_BOXES['unitdefense'],
            3: TR_BOXES['unitproperties'],
        }

    def init(self):
        self.current_stat_index = 0

    def on_open(self):
        self.init()
        self.hover_info()

    def left(self):
        self.current_stat_index = (self.current_stat_index+self.NUM_STATS-1)%self.NUM_STATS
        self.hover_info()

    def right(self):
        self.current_stat_index = (self.current_stat_index+1)%self.NUM_STATS
        self.hover_info()

    def hover_info(self):
        self.in_tr.mouse_manager.hover_box(self.BBOXES[self.current_stat_index])


class IconSelectorMenu(object):
    def __init__(self, input_translator):
        self.in_tr = input_translator
        self.init()

    def init(self):
        self.last_selected_bbox = None
        self.current_row = 0

    def on_open(self):
        pass
        #self.init()

    def next_page(self):
        if self.last_selected_bbox == None: return
        self.current_row += 1

    def prev_page(self):
        if self.last_selected_bbox == None: return 
        self.current_row = max(0, self.current_row-1)

    def get_page_str(self):
        if self.current_row:
            return 'Page ' + str(self.current_row)
        return ''

    def get_icon_bbox(self, index):
        if self.current_row <= 0:
            return TR_BOXES['quickicon%d'%(index+1)]
        return quick_icon_relative_box(self.last_selected_bbox, self.current_row, index)

    def click_icon(self, index):
        if self.current_row <= 0:
            self.last_selected_bbox = TR_BOXES['quickicon%d'%(index+1)]
        self.in_tr.mouse_manager.click_button(self.get_icon_bbox(index), 'LMB', keep_position_after=True)

# In resolution 1920x1080
TR_BOXES = {
    'minimap': (1653+10,29,226,226),
    'doctrine_view': (1661,385,228,444),
    'prod1': (1666,533,71,71),
    'prod2': (1740,533,71,71),
    'prod3': (1814,533,71,71),
    'prod4': (1666,607,71,71),
    'prod5': (1740,607,71,71),
    'prod6': (1814,607,71,71),
    'prod7': (1666,681,71,71),
    'prod8': (1740,681,71,71),
    'prod9': (1814,681,71,71),
    'prod10': (1666,755,71,71),
    'prod11': (1740,755,71,71),
    'prod12': (1814,755,71,71),
    'ability1': (42,700,40,40),
    'ability2': (84,700,40,40),
    'ability3': (126,700,40,40),
    'ability4': (168,700,40,40),
    'ability5': (210,700,40,40),
    'support1': (5,393,40,40),
    'support2': (5,436,40,40),
    'support3': (5,479,40,40),
    'support4': (5,522,40,40),
    'support5': (5,565,40,40),
    'build_panel': (1675,349,98,26),
    'doctrines_panel': (1777,349,98,26),
    'tab1': (1665,389,41,89),
    'tab2': (1710,389,41,89),
    'tab3': (1755,389,41,89),
    'tab4': (1800,389,41,89),
    'tab5': (1845,389,41,89),
    'selection_uparrow': (285,805,16,28),
    'selection_downarrow': (285,840,16,28),
    'upgrade1': (291,765,57,57),
    'upgrade2': (291,823,57,57),
    'production_queues': (1676,489,199,32),
    'unitportrait': (27,801,100,100),
    'unitweapon': (133,828,38,44),
    'unitdefense': (178,828,38,44),
    'unitproperties': (223,828,38,44),
    'quickicon4': (1386+10,64,48,55),
    'quickicon3': (1442+10,64,48,55),
    'quickicon2': (1500+10,64,48,55),
    'quickicon1': (1552+10,64,48,55),
    'power_meter': (1626+10,35,17,186),
    'population_hover': (1566+10,36,33,13),
}
def add_selection_boxes():
    for i in range(18):
        sel_x = 24 + 41*(i%6)
        sel_y = 772 + 45*(i//6)
        TR_BOXES['selection%d'%(i+1)] = (sel_x, sel_y, 38, 41)
add_selection_boxes()

def doctrine_box(column, row):
    return (1672 + 74*column, 417 + 68*row, 57, 52)

def quick_icon_relative_box(base_box, row, column):
    assert row >= 1
    x_offset = 1382 - 1386
    y_offset = 132 - 64
    x_gap = 53
    y_gap = 52
    width = 45
    height = 48
    return (
        base_box[0] + x_offset - x_gap*column,
        base_box[1] + y_offset + y_gap*(row-1),
        width,height
    )

def quick_icon_arrow(index):
    bbox = TR_BOXES['quickicon%d'%index]
    return (bbox[0]+20, bbox[1]+46, 4, 4)

class ScreenGrabber(object):
    def __init__(self, rect):
        self.sct = mss.mss()
        self.screen_image = None
        self.screen_rect = rect

    def update_rect(self, rect):
        self.screen_rect = rect

    def refresh_screen_image(self):
        if False: # PLACEHOLDER
            self.screen_image = Image.open('preview.png')
            return
        sr = self.screen_rect
        monitor = {"left": sr[0], "top": sr[1], "width": sr[2], "height": sr[3]}
        sct_img = self.sct.grab(monitor)
        self.screen_image = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        #self.screen_image.save('test_output.png')

    def crop_screen_image(self, xywh):
        x_ratio = self.screen_image.size[0]/1920
        y_ratio = self.screen_image.size[1]/1080
        xyxy = (
            round(x_ratio*(xywh[0])),
            round(y_ratio*(xywh[1])),
            round(x_ratio*(xywh[0]+xywh[2])),
            round(y_ratio*(xywh[1]+xywh[3])),
        )
        return self.screen_image.crop(xyxy)

    def grab(self,x,y,w,h):
        # avoid using. this is slow for multiple screen grabs
        monitor = {"top": y, "left": x, "width": w, "height": h}
        sct_img = self.sct.grab(monitor)
        return Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

def find_tempest_rising_window():
    hwnd = win32gui.FindWindowEx(None, None, None, 'Tempest  ')
    if hwnd != 0:
        return hwnd

    log_error('Unable to find Tempest Rising window, broadening search...', VERBOSITY_WARN)

    hwnd_ptr = []
    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            text = win32gui.GetWindowText(hwnd)
            if text.strip().lower() == 'tempest':
                hwnd_ptr.append(hwnd)
    win32gui.EnumWindows(winEnumHandler,None)
    if len(hwnd_ptr) > 0:
        log_error('Tempest Rising window found', VERBOSITY_WARN)
        return hwnd_ptr[0]

    log_error('Failed to find Tempest Rising window.', VERBOSITY_WARN)
    return None

from ctypes import windll
def get_tr_window_rect():
    ## Returns x, y, w, h
    hwnd = find_tempest_rising_window()
    if hwnd == None: return (160, 75, 1600, 900) # Placeholder
    if hwnd == None: return None
    rect = win32gui.GetClientRect(hwnd)
    #rect = win32gui.GetWindowRect(hwnd)
    topleft = win32gui.ClientToScreen(hwnd, (0,0))
    return topleft[0], topleft[1], rect[2], rect[3]

def set_click_through(win):
    hwnd = windll.user32.GetParent(win.winfo_id())
    ex_style = windll.user32.GetWindowLongW(hwnd, win32con.GWL_EXSTYLE)
    ex_style |= win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
    windll.user32.SetWindowLongW(hwnd, win32con.GWL_EXSTYLE, ex_style)

class OverlayUI(object):
    def __init__(self, input_translator, controller_input):
        self.input_translator = input_translator
        self.controller_input = controller_input
        self.screen_grabber = ScreenGrabber(get_tr_window_rect())

        tr_x, tr_y, self.width, self.height = get_tr_window_rect()
        #self.width = 1600
        #self.height = 900
        #self.screen_width = GetSystemMetrics(0)
        #self.screen_height = GetSystemMetrics(1)
        self.center_x, self.center_y = (self.width//2, self.height//2)

        root = tk.Tk()
        root.overrideredirect(True) # Disables title bar
        root.geometry('%dx%d+%d+%d' % (self.width, self.height, tr_x, tr_y))
        #root.geometry('%dx%d+%d+%d' % (self.width, self.height, (self.screen_width-self.width)//2, (self.screen_height-self.height)//2))
        root.title('TR Overlay UI')
        root.attributes('-transparentcolor', 'black', '-topmost', 1)
        root.config(bg='black') 
        #root.attributes("-alpha", 0.75)
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg='black', highlightthickness=0)
        self.canvas.pack()

        #setClickthrough(self.canvas.winfo_id())
        self.root = root
        self.image = Image.new('RGB', size=(self.width,self.height))
        self.draw = ImageDraw.Draw(self.image, 'RGB')

        self.tk_img = ImageTk.PhotoImage(self.image)
        #self.tk_img = ImageTk.PhotoImage(file='Image1.png')
        self.canvas_image = self.canvas.create_image(self.width/2,self.height/2, image=self.tk_img)
        #self.label = tk.Label(self.root, image=self.tk_img, bg='black')
        #self.label.pack()

        self.root.after(100, set_click_through, self.root)
        font_scale = self.width/1920

        self.WHEEL_LINE_COLOR = (252,243,127)
        self.WHEEL_DIVIDER_COLOR = (240,240,224)
        self.WHEEL_HIGHLIGHT_COLOR = (175,164,75)
        self.INPUT_LINE_COLOR = (191,238,225)
        self.MINIMAP_BORDER_COLOR = (238,238,255)
        self.CLEAR_COLOR = (0,0,0,255)
        self.TEXT_FONT_LARGE = ImageFont.truetype("Typestar Black.otf", round(60*font_scale))
        self.TEXT_FONT = ImageFont.truetype("Typestar Black.otf", round(36*font_scale))
        self.TEXT_FONT_SMALL = ImageFont.truetype("Typestar Black.otf", round(28*font_scale))
        self.TEXT_FONT_SMALLER = ImageFont.truetype("Typestar Black.otf", round(20*font_scale))
        #self.TEXT_FONT = ImageFont.truetype("Evogria.otf", 40)
        self.HIGHLIGHTED_TEXT_COLOR = (255,255,160)
        self.TEXT_COLOR = (160,191,225)
        self.TEXT_COLOR_ALT = (191,240,255)
        self.ENABLED_TEXT_COLOR = (64,255,127)
        self.DISABLED_TEXT_COLOR = (255,64,64)
        self.BRUSH_SELECT_COLOR = (127,240,225)
        self.MINIMAP_MOUSE_COLOR = (0,255,64)

        self.frame_draw_time = 0
        self.show_overlay_keystate = GetKeyState(HIDE_OVERLAY_KEY)%2


    def _refresh_tr_window_position(self):
        self.screen_grabber.update_rect(get_tr_window_rect())

    def _refresh_screengrab(self):
        self.screen_grabber.refresh_screen_image()
        
    def _paste_screengrab(self, cx, cy, screen_xywh, center=False, scale=None, rotate=None):
        im_crop = self.screen_grabber.crop_screen_image(screen_xywh)
        if scale != None:
            if type(scale) == tuple:
                im_crop = im_crop.resize((round(im_crop.size[0]*scale[0]), round(im_crop.size[1]*scale[1])))
            else:
                im_crop = im_crop.resize((round(im_crop.size[0]*scale), round(im_crop.size[1]*scale)))
        if rotate != None:
            im_crop = im_crop.rotate(rotate, expand=1)
        if center:
            self.image.paste(im_crop, (round(cx-im_crop.width/2), round(cy-im_crop.height/2)))
        else:
            self.image.paste(im_crop, (round(cx), round(cy)))
        
    def _clear_image(self):
        self.draw.rectangle((0,0,self.width,self.height), fill=self.CLEAR_COLOR)

    def _update_image(self):
        #self.tk_img = ImageTk.PhotoImage(file='Image1.png')
        self.tk_img = ImageTk.PhotoImage(self.image)
        self.canvas.itemconfigure(self.canvas_image, image=self.tk_img)
        #self.label.configure(image=self.tk_img)

    def _draw_wheel(self, cx, cy, in_radius, out_radius, num_options, draw_neutral=False, phase_offset=0):
        interval = 2*math.pi/num_options

        option = self.input_translator.left_stick_option(num_options, phase_offset=phase_offset)
        if option == -1:
            if draw_neutral:
                self.draw.circle((cx,cy), round(in_radius*0.9), outline=self.WHEEL_HIGHLIGHT_COLOR, width=round(in_radius*0.4))
        else:
            angle1 = -(option-0.5+phase_offset)*interval
            angle2 = -(option+0.5+phase_offset)*interval
            cos1, sin1, cos2, sin2 = math.cos(angle1), math.sin(angle1), math.cos(angle2), math.sin(angle2)
            h_radius1 = in_radius + 0.15*(out_radius-in_radius)
            h_radius2 = in_radius + 0.95*(out_radius-in_radius)
            self.draw.polygon((
                    cx + h_radius1*cos1, cy + h_radius1*sin1, cx + h_radius2*cos1, cy + h_radius2*sin1,
                    cx + h_radius2*cos2, cy + h_radius2*sin2, cx + h_radius1*cos2, cy + h_radius1*sin2
            ), fill=self.WHEEL_HIGHLIGHT_COLOR)

        for i in range(num_options):
            angle = -(i-0.5+phase_offset)*interval
            cos, sin = math.cos(angle), math.sin(angle)
            self.draw.line((cx + in_radius*cos, cy + in_radius*sin, cx + out_radius*cos, cy + out_radius*sin), width=5, fill=self.WHEEL_LINE_COLOR)

    def _draw_thumbstick_input_line(self, cx, cy, radius=None):
        if radius == None: radius = self.height*0.25
        magnitude, is_above_threshold, angle = self.input_translator.left_stick_properties()
        if not is_above_threshold: return

        cos, sin = math.cos(angle), -math.sin(angle)
        out_radius = magnitude*radius
        in_radius = (magnitude*radius)*0.25
        self.draw.line((cx + in_radius*cos, cy + in_radius*sin, cx + out_radius*cos, cy + out_radius*sin), width=5, fill=self.INPUT_LINE_COLOR)

    def _wheel_icon_location(self, option, cx, cy, icon_radius, num_options, phase_offset=0):
        angle = -(option+phase_offset)*2*math.pi/num_options
        cos, sin = math.cos(angle), math.sin(angle)
        return cx + icon_radius*cos, cy + icon_radius*sin

    def _polar(self, cx, cy, angle, distance):
        cos, sin = math.cos(angle), -math.sin(angle)
        return cx + distance*cos, cy + distance*sin

    def _draw_text_large(self, cx, cy, text, anchor='mm', color=None):
        if color == None: color = self.TEXT_COLOR
        #self.draw.text((cx, cy), text, anchor=anchor, align='center', font=self.TEXT_FONT, fill=color)
        self.draw.multiline_text((cx, cy), text, anchor=anchor, align='center', font=self.TEXT_FONT_LARGE, fill=color)

    def _draw_text(self, cx, cy, text, anchor='mm', color=None):
        if color == None: color = self.TEXT_COLOR
        #self.draw.text((cx, cy), text, anchor=anchor, align='center', font=self.TEXT_FONT, fill=color)
        self.draw.multiline_text((cx, cy), text, anchor=anchor, align='center', font=self.TEXT_FONT, fill=color)

    def _draw_text_small(self, cx, cy, text, anchor='mm', color=None):
        if color == None: color = self.TEXT_COLOR
        #self.draw.text((cx, cy), text, anchor=anchor, align='center', font=self.TEXT_FONT, fill=color)
        self.draw.multiline_text((cx, cy), text, anchor=anchor, align='center', font=self.TEXT_FONT_SMALL, fill=color)

    def _draw_text_smaller(self, cx, cy, text, anchor='mm', color=None):
        if color == None: color = self.TEXT_COLOR
        #self.draw.text((cx, cy), text, anchor=anchor, align='center', font=self.TEXT_FONT, fill=color)
        self.draw.multiline_text((cx, cy), text, anchor=anchor, align='center', font=self.TEXT_FONT_SMALLER, fill=color)

    def _draw_button_icon(self, cx, cy, key):
        highlight = self.frame_draw_time - self.input_translator.input_last_time[key] < 0.05
        if highlight or self.input_translator.input_status[key]:
            self.draw.multiline_text((cx, cy), '[%s]'%key, anchor='mm', align='center', font=self.TEXT_FONT, fill=self.HIGHLIGHTED_TEXT_COLOR)
        else:
            self.draw.multiline_text((cx, cy), '[%s]'%key, anchor='mm', align='center', font=self.TEXT_FONT, fill=self.TEXT_COLOR)

    def _draw_dpad(self, cx, cy):
        dpad_w = 0.01*self.height
        dpad_l = 0.04*self.height
        dpad_bl = dpad_l - dpad_w

        self.draw.rectangle((cx-dpad_w, cy-dpad_l, cx+dpad_w, cy+dpad_l), fill=self.TEXT_COLOR)
        self.draw.rectangle((cx-dpad_l, cy-dpad_w, cx+dpad_l, cy+dpad_w), fill=self.TEXT_COLOR)

        highlight = self.frame_draw_time - self.input_translator.input_last_time['DPAD_U'] < 0.05
        if highlight or self.input_translator.input_status['DPAD_U']:
            self.draw.rectangle((cx-dpad_w, cy-dpad_l, cx+dpad_w, cy-dpad_l+dpad_bl), fill=self.HIGHLIGHTED_TEXT_COLOR)
        
        highlight = self.frame_draw_time - self.input_translator.input_last_time['DPAD_D'] < 0.05
        if highlight or self.input_translator.input_status['DPAD_D']:
            self.draw.rectangle((cx-dpad_w, cy+dpad_l-dpad_bl, cx+dpad_w, cy+dpad_l), fill=self.HIGHLIGHTED_TEXT_COLOR)
        
        highlight = self.frame_draw_time - self.input_translator.input_last_time['DPAD_L'] < 0.05
        if highlight or self.input_translator.input_status['DPAD_L']:
            self.draw.rectangle((cx-dpad_l, cy-dpad_w, cx-dpad_l+dpad_bl, cy+dpad_w), fill=self.HIGHLIGHTED_TEXT_COLOR)
        
        highlight = self.frame_draw_time - self.input_translator.input_last_time['DPAD_R'] < 0.05
        if highlight or self.input_translator.input_status['DPAD_R']:
            self.draw.rectangle((cx+dpad_l-dpad_bl, cy-dpad_w, cx+dpad_l, cy+dpad_w), fill=self.HIGHLIGHTED_TEXT_COLOR)


    def _draw(self):
        self.frame_draw_time = time.time()
        if GetKeyState(HIDE_OVERLAY_KEY)%2 != self.show_overlay_keystate:
            return

        in_tr = self.input_translator
        mm = in_tr.mouse_manager

        self._draw_cursor()
        self._draw_brush_select()

        if mm.minimap_open: # note: minimap_open is currently double tracked by mm.minimap_open and self.current_mode
            minimap_scale = 3.3
            self._paste_screengrab(self.center_x, self.center_y, TR_BOXES['minimap'], center=True, scale=minimap_scale)
            minimap_sidelength = TR_BOXES['minimap'][2]*self.width/1920 * minimap_scale
            mouse_x = (mm.minimap_mouse_x - mm.MINIMAP_X1)*minimap_scale + self.center_x - minimap_sidelength/2
            mouse_y = (mm.minimap_mouse_y - mm.MINIMAP_Y1)*minimap_scale + self.center_y - minimap_sidelength/2
            self.draw.circle((mouse_x, mouse_y), self.height*0.01, fill=self.MINIMAP_MOUSE_COLOR)
            self.draw.circle((mouse_x, mouse_y), self.height*0.02, outline=self.MINIMAP_MOUSE_COLOR, width=3)
            self.draw.circle((mouse_x, mouse_y), self.height*0.04, outline=self.MINIMAP_MOUSE_COLOR, width=4)
            self.draw.circle((mouse_x, mouse_y), self.height*0.06, outline=self.MINIMAP_MOUSE_COLOR, width=5)
            self.draw.rectangle((self.center_x-minimap_sidelength/2,self.center_y-minimap_sidelength/2,
                self.center_x+minimap_sidelength/2,self.center_y+minimap_sidelength/2,), width=2, outline=self.MINIMAP_BORDER_COLOR)

        in_radius, out_radius = self.height*0.1, self.height*0.25
        wheel_label_x, wheel_label_y = self.center_x, self.center_y - self.height*0.3
        if in_tr.current_mode == MODE_ABILITY:
            self._draw_wheel(self.center_x, self.center_y, self.height*0.20, self.height*0.35, in_tr.NUM_ABILITY_ICONS, phase_offset=in_tr.OFFSET_ABILITIES_WHEEL)
            for i in range(in_tr.NUM_ABILITY_ICONS):
                cx, cy = self._wheel_icon_location(i, self.center_x, self.center_y, self.height*0.27, in_tr.NUM_ABILITY_ICONS, phase_offset=in_tr.OFFSET_ABILITIES_WHEEL)
                if i < 5:
                    self._paste_screengrab(cx, cy, TR_BOXES['ability%d'%(i+1)], center=True, scale=1.8)
                elif i == 5:
                    self._paste_screengrab(cx, cy, TR_BOXES['upgrade1'], center=True, scale=1.2)
                elif i == 6:
                    self._paste_screengrab(cx, cy, TR_BOXES['upgrade2'], center=True, scale=1.2)
                else:
                    self._paste_screengrab(cx, cy, TR_BOXES['support%d'%(12-i)], center=True, scale=1.8)

            # Divider lines for wheel
            interval = 2*math.pi/in_tr.NUM_ABILITY_ICONS
            in_radius = self.height*0
            out_radius = self.height*0.40
            for i in (0,5,7):
                angle = -(i-0.5+in_tr.OFFSET_ABILITIES_WHEEL)*interval
                cos, sin = math.cos(angle), math.sin(angle)
                self.draw.line((self.center_x + in_radius*cos, self.center_y + in_radius*sin, self.center_x + out_radius*cos, self.center_y + out_radius*sin), width=8, fill=self.WHEEL_DIVIDER_COLOR)

            text_radius = self.height*0.115
            angle = -(2.5-0.5+in_tr.OFFSET_ABILITIES_WHEEL)*interval
            cos, sin = math.cos(angle), math.sin(angle)
            self._draw_text(self.center_x + text_radius*cos, self.center_y + text_radius*sin, 'Unit\nAbilities', anchor='mm')

            angle = -(9.5-0.5+in_tr.OFFSET_ABILITIES_WHEEL)*interval
            cos, sin = math.cos(angle), math.sin(angle)
            self._draw_text(self.center_x + text_radius*cos, self.center_y + text_radius*sin, 'Support\nPowers', anchor='mm')

            angle = -(6-0.5+in_tr.OFFSET_ABILITIES_WHEEL)*interval
            cos, sin = math.cos(angle), math.sin(angle)
            self._draw_text(self.center_x + text_radius*cos, self.center_y + text_radius*sin, 'Upgrades', anchor='mm')


            text_y = self.center_y + 0.27*self.height
            offset_x = 0.35*self.height
            offset_text = 0.05*self.height

            self._draw_button_icon(self.center_x+offset_x, text_y, 'RB')
            self._draw_text_small(self.center_x+offset_x, text_y+offset_text, 'Use / Upgrade', anchor='mm')

            self._draw_button_icon(self.center_x-offset_x, text_y, 'LB')
            self._draw_text_small(self.center_x-offset_x, text_y+offset_text, 'Cancel (Upgrades)', anchor='mm')

            self._draw_text(wheel_label_x, wheel_label_y - 0.08*self.height, 'Abilities / Upgrades / Support Powers')
            self._draw_thumbstick_input_line(self.center_x, self.center_y)

        elif in_tr.current_mode == MODE_ACTION:
            self._draw_text(wheel_label_x, wheel_label_y + 0.05*self.height, 'Actions')
            dist = 0.11*self.height
            dist2 = 0.2*self.height
            offset_text = 0.04*self.height
            offset_text2 = 0.07*self.height
            cx, cy = self.center_x - dist, self.center_y
            self._draw_button_icon(cx, cy, 'X')
            self._draw_text_small(cx, cy+offset_text, 'Guard', anchor='mm')

            cx, cy = self.center_x, self.center_y - dist
            self._draw_button_icon(cx, cy, 'Y')
            self._draw_text_small(cx, cy+offset_text, 'Patrol', anchor='mm')

            cx, cy = self.center_x + dist, self.center_y
            self._draw_button_icon(cx, cy, 'B')
            self._draw_text_small(cx, cy+offset_text, 'Hold Position', anchor='mm')

            cx, cy = self.center_x, self.center_y + dist
            self._draw_button_icon(cx, cy, 'A')
            self._draw_text_small(cx, cy+offset_text, 'Stop', anchor='mm')

            cx, cy = self.center_x - dist2, self.center_y - dist2
            self._draw_button_icon(cx, cy, 'LB')
            color = self.ENABLED_TEXT_COLOR if in_tr.formation_move else self.DISABLED_TEXT_COLOR
            self._draw_text_smaller(cx, cy+offset_text, 'Toggle Formation Move', anchor='mm')
            self._draw_text_smaller(cx, cy+offset_text2, 'Formations: ' + ('ON' if in_tr.formation_move else 'OFF'), anchor='mm', color=color)

            cx, cy = self.center_x + dist2, self.center_y - dist2
            self._draw_button_icon(cx, cy, 'RB')
            color = self.ENABLED_TEXT_COLOR if in_tr.attack_buildings else self.DISABLED_TEXT_COLOR
            self._draw_text_smaller(cx, cy+offset_text, 'Toggle Attack Move', anchor='mm')
            self._draw_text_smaller(cx, cy+offset_text2, 'Attack Structures: ' + ('ON' if in_tr.attack_buildings else 'OFF'), anchor='mm', color=color)

        elif in_tr.current_mode == MODE_GROUPS:
            in_radius, out_radius = self.height*0.13, self.height*0.22
            self._draw_wheel(self.center_x, self.center_y, in_radius, out_radius, in_tr.NUM_GROUPS)
            option = self.input_translator.left_stick_option(in_tr.NUM_GROUPS)
            for i in range(in_tr.NUM_GROUPS):
                cx, cy = self._wheel_icon_location(i, self.center_x, self.center_y, self.height*0.17, in_tr.NUM_GROUPS)
                self._draw_text_large(cx, cy, str(i+1), color=self.TEXT_COLOR_ALT)

            if option != -1:
                self._draw_text(self.center_x, self.center_y - 0.05*self.height, f'Group {option+1}', color=self.TEXT_COLOR_ALT)

            if self.frame_draw_time - self.input_translator.input_last_time[KEY_GROUP_SET] < 0.25:
                self._draw_text(self.center_x, self.center_y + 0.05*self.height, f'set', color=self.TEXT_COLOR_ALT)

            if self.frame_draw_time - self.input_translator.input_last_time[KEY_GROUP_SELECT] < 0.25:
                self._draw_text(self.center_x, self.center_y + 0.05*self.height, f'select', color=self.TEXT_COLOR_ALT)

            if self.frame_draw_time - self.input_translator.input_last_time[KEY_GROUP_STEAL] < 0.25:
                self._draw_text(self.center_x, self.center_y + 0.05*self.height, f'set (steal)', color=self.TEXT_COLOR_ALT)

            if self.frame_draw_time - self.input_translator.input_last_time[KEY_GROUP_ADD] < 0.25:
                self._draw_text(self.center_x, self.center_y + 0.05*self.height, f'select (add)', color=self.TEXT_COLOR_ALT)

            dist = 0.075*self.height
            offset_text = 0.04*self.height
            offset_x = 0.34*self.height
            offset_y = 0.13*self.height

            cx, cy = self.center_x+offset_x, self.center_y+offset_y + dist
            self._draw_button_icon(cx, cy, 'A')
            self._draw_text_small(cx, cy+offset_text, 'Select', anchor='mm')

            cx, cy = self.center_x+offset_x + dist, self.center_y+offset_y
            self._draw_button_icon(cx, cy, 'B')
            self._draw_text_small(cx, cy+offset_text, 'Set', anchor='mm')

            cx, cy = self.center_x+offset_x - dist, self.center_y+offset_y
            self._draw_button_icon(cx, cy, 'X')
            self._draw_text_small(cx, cy+offset_text, 'Combine', anchor='mm')

            cx, cy = self.center_x+offset_x, self.center_y+offset_y - dist
            self._draw_button_icon(cx, cy, 'Y')
            self._draw_text_small(cx, cy+offset_text, 'Steal', anchor='mm')


            dpad_pos_x = self.center_x - 0.32*self.height
            dpad_pos_y = self.center_y + offset_y
            dpad_text_offset_h1 = 0.11*self.height
            dpad_text_offset_h2 = 0.09*self.height
            dpad_text_offset_v = 0.07*self.height

            self._draw_dpad(dpad_pos_x, dpad_pos_y)
            self._draw_text_smaller(dpad_pos_x, dpad_pos_y - dpad_text_offset_v, 'LOCAL UNITS', anchor='mm')
            self._draw_text_smaller(dpad_pos_x - dpad_text_offset_h1, dpad_pos_y, 'SELECT UNITS\nOF TYPE', anchor='mm')
            self._draw_text_smaller(dpad_pos_x, dpad_pos_y + dpad_text_offset_v, 'ALL UNITS', anchor='mm')
            self._draw_text_smaller(dpad_pos_x + dpad_text_offset_h2, dpad_pos_y, 'CENTER\nCAMERA', anchor='mm')

            self._draw_text(wheel_label_x, wheel_label_y, 'Control Groups')
            self._draw_thumbstick_input_line(self.center_x, self.center_y)


        elif in_tr.current_mode == MODE_BUILD:
            self._draw_wheel(self.center_x, self.center_y, self.height*0.08, self.height*0.19, in_tr.NUM_TABS)
            self._draw_wheel(self.center_x, self.center_y, self.height*0.2, self.height*0.35, in_tr.NUM_BUILD_ICONS)

            for i in range(in_tr.NUM_BUILD_ICONS):
                cx, cy = self._wheel_icon_location(i, self.center_x, self.center_y, self.height*0.28, in_tr.NUM_BUILD_ICONS)
                self._paste_screengrab(cx, cy, TR_BOXES['prod%d'%(i+1)], center=True, scale=1.5)

            oution_outer = self.input_translator.left_stick_option(in_tr.NUM_BUILD_ICONS)
            offset_text = 0.035*self.height
            if oution_outer != -1:
                angle = oution_outer*2*math.pi/in_tr.NUM_BUILD_ICONS
                angle_offset = 2*math.pi/in_tr.NUM_BUILD_ICONS/4
                distance = self.height*0.38
                cx, cy = self._polar(self.center_x, self.center_y, angle+angle_offset, distance)
                self._draw_button_icon(cx, cy, 'A')
                if in_tr.shift_manager.held:
                    self._draw_text_smaller(cx, cy+offset_text, 'Train x5', anchor='mm', color=self.HIGHLIGHTED_TEXT_COLOR)
                else:
                    self._draw_text_smaller(cx, cy+offset_text, 'Train', anchor='mm')

                cx, cy = self._polar(self.center_x, self.center_y, angle-angle_offset, distance)
                self._draw_button_icon(cx, cy, 'B')
                if in_tr.shift_manager.held:
                    self._draw_text_smaller(cx, cy+offset_text, 'Pause/Cancel x5', anchor='mm', color=self.HIGHLIGHTED_TEXT_COLOR)
                else:
                    self._draw_text_smaller(cx, cy+offset_text, 'Pause/Cancel', anchor='mm')

            for i in range(5):
                cx, cy = self._wheel_icon_location(i, self.center_x, self.center_y, self.height*0.12, in_tr.NUM_TABS)
                self._paste_screengrab(cx, cy, TR_BOXES['tab%d'%(i+1)], center=True, scale=(1.5,1), rotate=-90)

            option_inner = self.input_translator.left_stick_option(in_tr.NUM_TABS)
            offset_text = 0.04*self.height
            if option_inner != -1:
                angle = option_inner*2*math.pi/in_tr.NUM_TABS
                cx, cy = self._polar(self.center_x, self.center_y, angle, self.height*0.04)
                self._draw_button_icon(cx, cy, 'Y')
                self._draw_text_smaller(cx, cy+offset_text, 'Switch Tab', anchor='mm')

            extra_options_x = self.center_x - 0.50*self.height
            extra_options_y = self.center_y - 0.10*self.height
            self._draw_button_icon(extra_options_x, extra_options_y, 'X')
            #self._draw_text_smaller(extra_options_x, extra_options_y+0.05*self.height, 'Set rally point\n(for production tab)', anchor='mm')
            self._draw_text_smaller(extra_options_x, extra_options_y+0.05*self.height, 'Select structures\n(for production tab)', anchor='mm')

            self._paste_screengrab(self.center_x, self.center_y-self.height*0.2, TR_BOXES['production_queues'], center=True)


            dpad_pos_x = self.center_x - 0.50*self.height
            dpad_pos_y = self.center_y + 0.14*self.height
            dpad_text_offset_h = 0.08*self.height
            dpad_text_offset_v = 0.07*self.height

            self._draw_dpad(dpad_pos_x, dpad_pos_y)
            self._draw_text_smaller(dpad_pos_x - dpad_text_offset_h, dpad_pos_y, 'REPAIR', anchor='mm')
            self._draw_text_smaller(dpad_pos_x, dpad_pos_y - dpad_text_offset_v, 'SELL', anchor='mm')
            self._draw_text_smaller(dpad_pos_x + dpad_text_offset_h, dpad_pos_y, 'POWER', anchor='mm')
            self._draw_text_smaller(dpad_pos_x, dpad_pos_y + dpad_text_offset_v, 'PLACE STRUCTURE', anchor='mm')

            self._draw_text(wheel_label_x, wheel_label_y - self.height*0.12, 'Build')
            self._draw_thumbstick_input_line(self.center_x, self.center_y)

        elif in_tr.current_mode == MODE_SELECTION:
            self._draw_wheel(self.center_x, self.center_y, self.height*0.23, self.height*0.34, in_tr.NUM_SELECTION_ICONS)

            for i in range(in_tr.NUM_SELECTION_ICONS):
                cx, cy = self._wheel_icon_location(i, self.center_x, self.center_y, self.height*0.28, in_tr.NUM_SELECTION_ICONS)
                self._paste_screengrab(cx, cy, TR_BOXES['selection%d'%(i+1)], center=True, scale=1.7)

            dist = 0.12*self.height
            offset_text = 0.04*self.height
            cx, cy = self.center_x, self.center_y + dist
            self._draw_button_icon(cx, cy, 'A')
            self._draw_text_small(cx, cy+offset_text, 'Select Only', anchor='mm')

            cx, cy = self.center_x + dist, self.center_y
            self._draw_button_icon(cx, cy, 'B')
            self._draw_text_small(cx, cy+offset_text, 'Remove', anchor='mm')

            #cx, cy = self.center_x - dist, self.center_y
            #self._draw_button_icon(cx, cy, 'X')
            #self._draw_text_small(cx, cy+offset_text, 'Select Type', anchor='mm')

            #cx, cy = self.center_x, self.center_y - dist
            #self._draw_button_icon(cx, cy, 'Y')
            #self._draw_text_small(cx, cy+offset_text, 'Remove Type', anchor='mm')

            dpad_pos_x = self.center_x - 0.55*self.height
            dpad_pos_y = self.center_y + 0.05*self.height
            dpad_text_offset_h = 0.10*self.height
            dpad_text_offset_v = 0.08*self.height

            self._draw_dpad(dpad_pos_x, dpad_pos_y)
            self._draw_text_smaller(dpad_pos_x + dpad_text_offset_h, dpad_pos_y, 'Subselect\nnext')
            self._draw_text_smaller(dpad_pos_x - dpad_text_offset_h, dpad_pos_y, 'Subselect\nprevious')
            self._paste_screengrab(dpad_pos_x, dpad_pos_y - dpad_text_offset_v, TR_BOXES['selection_uparrow'], center=True, scale=2)
            self._paste_screengrab(dpad_pos_x, dpad_pos_y + dpad_text_offset_v, TR_BOXES['selection_downarrow'], center=True, scale=2)

            self._draw_text(wheel_label_x, wheel_label_y - 0.07*self.height, 'Selection')
            self._draw_thumbstick_input_line(self.center_x, self.center_y)

        elif in_tr.current_mode == MODE_CAMERA:
            self._draw_text(wheel_label_x, wheel_label_y + 0.05*self.height, 'Camera')
            dist = 0.11*self.height
            dist2 = 0.2*self.height
            offset_text = 0.05*self.height
            cx, cy = self.center_x - dist, self.center_y
            self._draw_button_icon(cx, cy, 'X')
            self._draw_text_small(cx, cy+offset_text, 'Location 4', anchor='mm')

            cx, cy = self.center_x, self.center_y - dist
            self._draw_button_icon(cx, cy, 'Y')
            self._draw_text_small(cx, cy+offset_text, 'Location 3', anchor='mm')

            cx, cy = self.center_x + dist, self.center_y
            self._draw_button_icon(cx, cy, 'B')
            self._draw_text_small(cx, cy+offset_text, 'Location 2', anchor='mm')

            cx, cy = self.center_x, self.center_y + dist
            self._draw_button_icon(cx, cy, 'A')
            self._draw_text_small(cx, cy+offset_text, 'Location 1', anchor='mm')

            cx, cy = self.center_x - dist2, self.center_y - dist2
            self._draw_button_icon(cx, cy, 'LB')
            self._draw_text_smaller(cx, cy+offset_text, '(Hold) Save\ncamera location', anchor='mm')

            cx, cy = self.center_x + dist2, self.center_y - dist2
            self._draw_button_icon(cx, cy, 'RB')
            self._draw_text_smaller(cx, cy+offset_text, '(Hold) Save\ncamera location', anchor='mm')

        elif in_tr.current_mode == MODE_INFO:
            self._draw_text(wheel_label_x, wheel_label_y + 0.05*self.height, 'Info')
            dist = 0.11*self.height
            dist2 = 0.2*self.height
            offset_text = 0.05*self.height
            cx, cy = self.center_x, self.center_y - dist
            self._draw_button_icon(cx, cy, 'Y')
            self._draw_text_small(cx, cy+offset_text, 'View Population', anchor='mm')

            cx, cy = self.center_x + dist, self.center_y
            self._draw_button_icon(cx, cy, 'B')
            self._draw_text_small(cx, cy+offset_text, 'View Power', anchor='mm')

            cx, cy = self.center_x - dist2, self.center_y - dist2
            self._draw_button_icon(cx, cy, 'LB')
            self._draw_text_smaller(cx, cy+offset_text, 'Unit Info\nPrevious', anchor='mm')

            cx, cy = self.center_x + dist2, self.center_y - dist2
            self._draw_button_icon(cx, cy, 'RB')
            self._draw_text_smaller(cx, cy+offset_text, 'Unit Info\nNext', anchor='mm')

        elif in_tr.current_mode == MODE_ICONS:
            self._draw_text(wheel_label_x, wheel_label_y + 0.02*self.height, 'Quick Icons')
            dist = 0.13*self.height
            dist2 = 0.2*self.height
            offset_text = 0.05*self.height
            offset_button = -0.03*self.height
            offset_icon = 0.05*self.height
            self._draw_text(self.center_x, self.center_y+0.03*self.height, in_tr.icon_selector_menu.get_page_str())
            
            cx, cy = self.center_x - dist, self.center_y
            self._draw_button_icon(cx, cy+offset_button, 'X')
            self._paste_screengrab(cx, cy+offset_icon, in_tr.icon_selector_menu.get_icon_bbox(3), center=True, scale=2)

            cx, cy = self.center_x, self.center_y - dist
            self._draw_button_icon(cx, cy+offset_button, 'Y')
            self._paste_screengrab(cx, cy+offset_icon, in_tr.icon_selector_menu.get_icon_bbox(2), center=True, scale=2)

            cx, cy = self.center_x + dist, self.center_y
            self._draw_button_icon(cx, cy+offset_button, 'B')
            self._paste_screengrab(cx, cy+offset_icon, in_tr.icon_selector_menu.get_icon_bbox(1), center=True, scale=2)

            cx, cy = self.center_x, self.center_y + dist
            self._draw_button_icon(cx, cy+offset_button, 'A')
            self._paste_screengrab(cx, cy+offset_icon, in_tr.icon_selector_menu.get_icon_bbox(0), center=True, scale=2)

            cx, cy = self.center_x - dist2, self.center_y - dist2
            self._draw_button_icon(cx, cy, 'LB')
            self._draw_text_smaller(cx, cy+offset_text, 'Previous Page', anchor='mm')

            cx, cy = self.center_x + dist2, self.center_y - dist2
            self._draw_button_icon(cx, cy, 'RB')
            self._draw_text_smaller(cx, cy+offset_text, 'Next Page', anchor='mm')

        elif in_tr.current_mode == MODE_DOCTRINES:
            self._draw_text(wheel_label_x, wheel_label_y + 0.05*self.height, 'Doctrines')
            self._paste_screengrab(self.center_x, self.center_y, TR_BOXES['doctrine_view'], center=True, scale=2)


    def _draw_cursor(self):
        mm = self.input_translator.mouse_manager
        if not mm.minimap_open and not mm.brush_started:
            self.draw.circle((self.center_x, self.center_y), self.height*0.001, fill=self.MINIMAP_MOUSE_COLOR)
            self.draw.circle((self.center_x, self.center_y), self.height*0.01, outline=self.MINIMAP_MOUSE_COLOR, width=2)

    def _draw_brush_select(self):
        mm = self.input_translator.mouse_manager
        if mm.brush_started:
            box_x, box_y = mm.brush_size(time.time()-mm.brush_hold_start_time)
            dx, dy = box_x/2*mm.tr_xywh[3], box_y/2*mm.tr_xywh[3]
            self.draw.rectangle((self.center_x-dx,self.center_y-dy,self.center_x+dx,self.center_y+dy),
                outline=self.BRUSH_SELECT_COLOR, width=2)

    def loop(self):
        self.controller_input.loop()
        self.input_translator.loop()

        if self.redraw_skip%8 == 0:
            self._refresh_tr_window_position()
            self._refresh_screengrab()

        if self.redraw_skip%4 == 0:
            s = time.time()
            self._clear_image()
            self._draw()
            self._update_image()
            self.total_render_time = time.time()-s
            self.rendered_frames += 1
        self.redraw_skip += 1
        #if self.redraw_skip%100 == 0: print('average render time: %g' % (self.total_render_time/self.rendered_frames))
        #self.redraw_skip = (self.redraw_skip+1)%3

        self.root.after(5, self.loop)

    def start(self):
        self.redraw_skip = 0
        self.rendered_frames = 0
        self.total_render_time = 0
        #self.root.after(0, after_func)
        self.root.after(10, self.loop)
        self.root.mainloop()


BUTTON_INPUTS = {'LT','RT','LB','RB','A','Y','X','B','LS','RS','SEL','START','DPAD_L','DPAD_R','DPAD_U','DPAD_D','LS_U','LS_D','LS_L','LS_R','RS_U','RS_D','RS_L','RS_R',}

GAMEPAD_INPUT_TRANSLATION = {
    #'ABS_Y': '',
    #'ABS_X': '',
    #'ABS_RY': '',
    #'ABS_RX': '',
    #'ABS_Z': '',
    #'ABS_RZ': '',
    'BTN_TL': 'LB',
    'BTN_TR': 'RB',
    'BTN_SOUTH': 'A',
    'BTN_NORTH': 'Y',
    'BTN_WEST': 'X',
    'BTN_EAST': 'B',
    'BTN_THUMBL': 'LS',
    'BTN_THUMBR': 'RS',
    'BTN_SELECT': 'START',
    'BTN_START': 'SEL',
    #'BTN_TRIGGER_HAPPY1': 'DPAD_L',
    #'BTN_TRIGGER_HAPPY2': 'DPAD_R',
    #'BTN_TRIGGER_HAPPY3': 'DPAD_U',
    #'BTN_TRIGGER_HAPPY4': 'DPAD_D',
}

import threading
event_list = []

def monitor_gamepad():
    while True:
        try:
            for e in inputs.get_gamepad():
                event_list.append(e)
        except inputs.UnpluggedError:
            time.sleep(0.5)

gamepad_thread = threading.Thread(target=monitor_gamepad)
gamepad_thread.daemon = True
gamepad_thread.start()

def gamepadEvents():
    copy = event_list[:]
    event_list.clear()
    return copy

class XboxController(object):
    def __init__(self, input_translator):
        self.input_translator = input_translator
        self.input_status = {key: False for key in BUTTON_INPUTS}
        self.current_time = 0
        self.input_last_time = {key: 0 for key in BUTTON_INPUTS}
        self.input_status['left_analog_x'] = 0
        self.input_status['left_analog_y'] = 0
        self.input_status['right_analog_x'] = 0
        self.input_status['right_analog_y'] = 0
        input_translator.update_input(self.input_status, self.input_last_time)

        self.ANALOG_THRESHOLD_LOW = 0.55
        self.ANALOG_THRESHOLD_HIGH = 0.6
        self.MAX_TRIG_VAL = math.pow(2, 8)
        self.MAX_JOY_VAL = math.pow(2, 15)
        self.TRIG_THRESHOLD_HIGH = 0.25
        self.TRIG_THRESHOLD_LOW = 0.2

        self.last_poll_time = None
        self.polling_time_log = [0]*300
        self.polling_time_log_position = 0
        self.polling_time_log_length = 0

    def release_key_if_held(self, key):
        if self.input_status[key]:
            self.input_status[key] = False
            self.input_last_time[key] = self.current_time
            self.input_translator.input_release(key, self.input_status, self.input_last_time)

    def press_key(self, key):
        self.input_status[key] = True
        self.input_last_time[key] = self.current_time
        self.input_translator.input_press(key, self.input_status, self.input_last_time)

    def release_key(self, key):
        self.input_status[key] = False
        self.input_last_time[key] = self.current_time
        self.input_translator.input_release(key, self.input_status, self.input_last_time)

    def analog_detect(self, value, key):
        if value/self.MAX_JOY_VAL >= self.ANALOG_THRESHOLD_HIGH and not self.input_status[key]:
            self.press_key(key)
            #print('press', key)
        if value/self.MAX_JOY_VAL < self.ANALOG_THRESHOLD_LOW and self.input_status[key]:
            self.release_key(key)
            #print('release', key)

    def log_poll_time(self):
        if self.last_poll_time != None:
            self.polling_time_log[self.polling_time_log_position] = (self.current_time - self.last_poll_time)
            self.polling_time_log_position = (self.polling_time_log_position + 1)%len(self.polling_time_log)
            self.polling_time_log_length += 1
            if False and self.polling_time_log_position == 0:
                print(statistics.mean(self.polling_time_log), statistics.stdev(self.polling_time_log))
                print([int(i*1000) for i in self.polling_time_log])
        self.last_poll_time = self.current_time

    def loop(self):
        input_translator = self.input_translator
        self.current_time = time.time()
        self.log_poll_time()

        #events = get_gamepad()
        events = gamepadEvents()
        #print(len(events))
        for event in events:
            if event.code == 'ABS_Y':
                self.input_status['left_analog_y'] = event.state / self.MAX_JOY_VAL
                input_translator.update_input(self.input_status, self.input_last_time)
                self.analog_detect(-event.state, 'LS_D')
                self.analog_detect(event.state, 'LS_U')
            elif event.code == 'ABS_X':
                self.input_status['left_analog_x'] = event.state / self.MAX_JOY_VAL
                input_translator.update_input(self.input_status, self.input_last_time)
                self.analog_detect(-event.state, 'LS_L')
                self.analog_detect(event.state, 'LS_R')
            elif event.code == 'ABS_RY':
                self.input_status['right_analog_y'] = event.state / self.MAX_JOY_VAL
                input_translator.update_input(self.input_status, self.input_last_time)
                self.analog_detect(-event.state, 'RS_D')
                self.analog_detect(event.state, 'RS_U')
            elif event.code == 'ABS_RX':
                self.input_status['right_analog_x'] = event.state / self.MAX_JOY_VAL
                input_translator.update_input(self.input_status, self.input_last_time)
                self.analog_detect(-event.state, 'RS_L')
                self.analog_detect(event.state, 'RS_R')
            elif event.code == 'ABS_Z':
                if event.state/self.MAX_TRIG_VAL >= self.TRIG_THRESHOLD_HIGH and not self.input_status['LT']:
                    self.press_key('LT')
                if event.state/self.MAX_TRIG_VAL < self.TRIG_THRESHOLD_LOW and self.input_status['LT']:
                    self.release_key('LT')
                #print(event.state / self.MAX_TRIG_VAL)
            elif event.code == 'ABS_RZ':
                if event.state/self.MAX_TRIG_VAL >= self.TRIG_THRESHOLD_HIGH and not self.input_status['RT']:
                    self.press_key('RT')
                if event.state/self.MAX_TRIG_VAL < self.TRIG_THRESHOLD_LOW and self.input_status['RT']:
                    self.release_key('RT')
            elif event.code == 'ABS_HAT0X':
                if event.state < 0:
                    self.release_key_if_held('DPAD_R')
                    self.press_key('DPAD_L')
                elif event.state > 0:
                    self.release_key_if_held('DPAD_L')
                    self.press_key('DPAD_R')
                else:
                    self.release_key_if_held('DPAD_R')
                    self.release_key_if_held('DPAD_L')
            elif event.code == 'ABS_HAT0Y':
                if event.state < 0:
                    self.release_key_if_held('DPAD_D')
                    self.press_key('DPAD_U')
                elif event.state > 0:
                    self.release_key_if_held('DPAD_U')
                    self.press_key('DPAD_D')
                else:
                    self.release_key_if_held('DPAD_D')
                    self.release_key_if_held('DPAD_U')
            else:
                if event.code in GAMEPAD_INPUT_TRANSLATION:
                    key = GAMEPAD_INPUT_TRANSLATION[event.code]
                    self.input_status[key] = bool(event.state)
                    self.input_last_time[key] = self.current_time
                    if event.state == 1:
                        input_translator.input_press(key, self.input_status, self.input_last_time)
                    else:
                        input_translator.input_release(key, self.input_status, self.input_last_time)
                elif event.code != 'SYN_REPORT':
                    print('??', event.code, event.state)
                #print(GAMEPAD_INPUT_TRANSLATION
            #print(event.ev_type, event.code, event.state)

def main():
    input_translator = InputTranslator()
    controller_input = XboxController(input_translator)
    overlay_ui = OverlayUI(input_translator, controller_input)
    overlay_ui.start()


if __name__ == "__main__":
    main()
