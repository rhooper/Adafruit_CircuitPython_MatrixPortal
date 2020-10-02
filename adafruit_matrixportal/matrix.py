# SPDX-FileCopyrightText: 2020 Melissa LeBlanc-Williams, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
`adafruit_matrixportal.matrix`
================================================================================

Helper library for the Adafruit RGB Matrix Shield + Metro M4 Airlift Lite.

* Author(s): Melissa LeBlanc-Williams

Implementation Notes
--------------------

**Hardware:**

* `Adafruit Matrix Portal <https://www.adafruit.com/product/4745>`_
* `Adafruit Metro M4 Express AirLift <https://www.adafruit.com/product/4000>`_
* `Adafruit RGB Matrix Shield <https://www.adafruit.com/product/2601>`_
* `64x32 RGB LED Matrix <https://www.adafruit.com/product/2278>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

import board
import displayio
import rgbmatrix
import framebufferio


__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MatrixPortal.git"


class Matrix:
    """Class representing the Adafruit RGB Matrix. This is used to automatically
    initialize the display.

    :param int width: The width of the display in Pixels. Defaults to 64.
    :param int height: The height of the display in Pixels. Defaults to 32.
    :param int bit_depth: The number of bits per color channel. Defaults to 2.
    :param list alt_addr_pins: An alternate set of address pins to use. Defaults to None

    """

    # pylint: disable=too-few-public-methods,too-many-branches
    def __init__(self, *, width=64, height=32, bit_depth=2, alt_addr_pins=None):

        # Detect the board type based on available pins
        if hasattr(board, "MTX_ADDRA"):
            # MatrixPortal M4
            addr_pins = [board.MTX_ADDRA, board.MTX_ADDRB, board.MTX_ADDRC]
            if height > 16:
                addr_pins.append(board.MTX_ADDRD)
            if height > 32:
                addr_pins.append(board.MTX_ADDRE)
            rgb_pins = [
                board.MTX_R1,
                board.MTX_G1,
                board.MTX_B1,
                board.MTX_R2,
                board.MTX_G2,
                board.MTX_B2,
            ]
            clock_pin = board.MTX_CLK
            latch_pin = board.MTX_LAT
            oe_pin = board.MTX_OE
        elif hasattr(board, "D7"):
            # Metro/Grand Central Style Board
            if height <= 16:
                raise RuntimeError(
                    "Pin A2 unavailable in this mode. Please specify alt_addr_pins."
                )
            addr_pins = [board.A0, board.A1, board.A2, board.A3]
            rgb_pins = [board.D2, board.D3, board.D4, board.D5, board.D6, board.D7]
            clock_pin = board.A4
            latch_pin = board.D10
            oe_pin = board.D9
        else:
            # Feather Style Board
            addr_pins = [board.A5, board.A4, board.A3]
            if height > 16:
                addr_pins.append(board.A2)
            rgb_pins = [board.D6, board.D5, board.D9, board.D11, board.D10, board.D12]
            clock_pin = board.D13
            latch_pin = board.D0
            oe_pin = board.D1

        # Alternate Address Pins
        if alt_addr_pins is not None:
            addr_pins = alt_addr_pins

        try:
            displayio.release_displays()
            matrix = rgbmatrix.RGBMatrix(
                width=width,
                height=height,
                bit_depth=bit_depth,
                rgb_pins=rgb_pins,
                addr_pins=addr_pins,
                clock_pin=clock_pin,
                latch_pin=latch_pin,
                output_enable_pin=oe_pin,
            )
            self.display = framebufferio.FramebufferDisplay(matrix)
        except ValueError:
            raise RuntimeError("Failed to initialize RGB Matrix") from ValueError
