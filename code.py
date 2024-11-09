# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# You must add a gamepad HID device inside your boot.py file
# in order to use this example.
# See this Learn Guide for details:
# https://learn.adafruit.com/customizing-usb-devices-in-circuitpython/hid-devices#custom-hid-devices-3096614-9

import usb_hid
import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from adafruit_macropad import MacroPad
from hid_gamepad import Gamepad

def axis_range_map(x):
  """Map encoder value to axis value

  Args:
      x (int): encoder value

  Returns:
      int: Mapped axis value
  """
  return (x - ENCODER_MIN) * (JOY_MAX - JOY_MIN) // (ENCODER_MAX - ENCODER_MIN) + JOY_MIN

def clamp(value, low, high):
  """Clamp value between low and high

  Args:
      value (int or float): Value to clamp
      low (int or float): Minimum value
      high (int or float): Maximum value

  Returns:
      int or float: Clamped value
  """
  return max(low, min(value, high))

macropad = MacroPad()
gamepad = Gamepad(usb_hid.devices)

# Key mapping
keymap = {
  'title' : 'PurplePad',
  'keys' : [ # List of key functions...
    # COLOR    LABEL
    # 1st row ----------
    (0x661199, '1'), (0x661199, '2'), (0x661199, '3'),
    # 2nd row ----------
    (0x660099, '4'), (0x660099, '5'), (0x660099, '6'),
    # 3rd row ----------
    (0x660099, '7'), (0x660099, '8'), (0x660099, '9'),
    # 4th row ----------
    (0x660099, '10'), (0x660099, '11'), (0x660099, '12')
  ]
}

# Set key LED brightness
macropad.pixels.brightness = 0.5

# Encoder offset
JOY_MAX = +127
JOY_MIN = -127
ENCODER_MAX = +20
ENCODER_MIN = -20
prev_encoder_value = 0.0
encoder_offset = 0

# Initialize display layout
display_group = displayio.Group()

# Key labels (0 - 11)
for key_index in range(12):
  x = key_index % 3
  y = key_index // 3
  display_group.append(
    label.Label(
      terminalio.FONT,
      text='',
      color=0xFFFFFF,
      anchored_position=((macropad.display.width - 1) * x / 2, macropad.display.height - 1 - (3 - y) * 12),
      anchor_point=(x / 2, 1.0)
    )
  )
# Title bar (12)
display_group.append(Rect(0, 0, macropad.display.width, 13, fill=0xFFFFFF))
# Title text (13)
display_group.append(label.Label(
  terminalio.FONT,
  text='',
  color=0x000000,
  anchored_position=(2, 0),
  anchor_point=(0.0, 0.0)
))
# Encoder text (14)
display_group.append(label.Label(
  terminalio.FONT,
  text='',
  color=0x000000,
  anchored_position=(macropad.display.width, 0),
  anchor_point=(1.0, 0.0)
))

# Set display layout group
macropad.display.root_group = display_group

# Set text
display_group[13].text = keymap['title']
display_group[14].text = "{}%".format(prev_encoder_value)
for i in range(12):
  macropad.pixels[i] = keymap['keys'][i][0]
  display_group[i].text = keymap['keys'][i][1]

# Main loop
while True:
  # Check for encoder switch
  macropad.encoder_switch_debounced.update()
  if macropad.encoder_switch_debounced.pressed:
    encoder_offset = -macropad.encoder
    macropad.play_tone(1000, 0.1)
    while macropad.encoder_switch: continue

  # Check if encoder has moved
  current_encoder_value = clamp(macropad.encoder + encoder_offset, ENCODER_MIN, ENCODER_MAX)
  if not current_encoder_value == prev_encoder_value:
    encoder_text = "{}%".format(current_encoder_value / ENCODER_MAX * 100)
    if current_encoder_value > 0.0: encoder_text = "+" + encoder_text
    display_group[14].text = encoder_text
  # Update previous encoder value
  prev_encoder_value = current_encoder_value

  # Move analog axis
  gamepad.move_joysticks(x=axis_range_map(current_encoder_value))

  # Check for key press
  key_event = macropad.keys.events.get()
  if not key_event: continue
  if key_event and key_event.pressed:
    display_group[key_event.key_number].text = len(keymap['keys'][key_event.key_number][1]) * "#"
    gamepad.press_buttons(key_event.key_number + 1)
  if key_event and key_event.released:
    display_group[key_event.key_number].text = keymap['keys'][key_event.key_number][1]
    gamepad.release_buttons(key_event.key_number + 1)
