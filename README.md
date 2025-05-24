# Casio Infinisweeper

An endless minesweeper game built for the Casio fx-9750GIII (might work for other calculators too).

Filenames are all <= 8 characters because that is the maximum on this calculator.

Due to this program not using any Casio-specific modules, it can be run on desktop
PCs. Keep in mind that the Casio calculators use MicroPython instead of CPython.
The only modules available on the calculator are Random, Math, and CasioPlot.

## Default Controls

Due to Casio's version of Python not having a `get_key` function, the shell
must be used. This means all commands end with pressing `exe` (`enter` on keyboards),
and the resolution is limited to the number of characters per line by the number of
lines minus one (one line is used for input).

Any number of commands can be input. All will be run. E.g., entering "44422"
will move the cursor or screen three tiles left and two tiles up.

- All numbers except `0` and `5`: Move the cursor or screen in that direction.
- `5`: Flag the tile that the cursor is currently on.
- `0`: Check the tile that the cursor is currently on.
- `.`: Switch movement mode between cursor or screen mode.

## Config

The `config.py` file contains various configuration variables; further configuration
requires editing the source code.
