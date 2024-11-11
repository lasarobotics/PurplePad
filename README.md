# PurplePad

Use Adafruit Macropad RP2040 as an input for FRC.
Simply makes the macropad show up as a standard game controller.

https://learn.adafruit.com/adafruit-macropad-rp2040/overview

## Default layout
```
Display |  *
01 | 02 | 03
04 | 05 | 06
07 | 08 | 09
10 | 11 | 12
```

"*" is the knob. Rotating the knob corresponds to "left stick, X axis", and pressing the knob resets that axis.

## Installation

1. Install CircuitPython 9.2:
  https://adafruit-circuit-python.s3.amazonaws.com/bin/adafruit_macropad_rp2040/en_US/adafruit-circuitpython-adafruit_macropad_rp2040-en_US-9.2.0.uf2
2. Copy this repo to the macropad's "CIRCUITPY" drive.

## Robot project integration

Simply create a `CommandXboxController` as you normally would and bind commands to buttons using the `CommandXboxController.button(int button)` method.
Access the encoder value by using `CommandXboxController.getLeftX()`.

```
private CommandXboxController m_keypad = new CommandXboxController(1);
...

m_keypad.getLeftX();
m_keypad.button(0).onTrue(Commands.print("Hello, world!"));

```
