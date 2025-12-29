# Sphero Bolt Custom HAL (Hardware Abstraction Layer)

### Overview
This project is a custom Python driver layer for the Sphero Bolt robot. It was developed to bypass limitations and bugs in the standard open-source libraries, specifically regarding the 8x8 LED Matrix memory mapping and Bluetooth Low Energy (BLE) connection stability.

### The Problem
The standard `spherov2` library utilizes incorrect packet identifiers for the Bolt's specific LED matrix firmware, rendering the display unusable. Additionally, the default connection logic lacks robust timeout handling, leading to `TimeoutError` crashes during rapid command sequencing.

### The Solution
I reverse-engineered the raw driver commands to identify the correct `compressed_frame_player` signatures. I then built a custom Hardware Abstraction Layer (HAL) that features:

* **Custom Matrix Driver:** Direct control of the 8x8 RGB grid for animations and text, bypassing the broken high-level wrapper.
* **Robust Connection Protocol:** Implemented a **Context Manager** (`__enter__`/`__exit__`) pattern to maintain persistent Bluetooth sessions, eliminating rapid-reconnect failures.
* **Buffer Management:** A custom chunking algorithm to handle scrolling text that exceeds the hardware's internal BLE buffer limits.

### Tech Stack
* **Language:** Python 3.10+
* **Communication:** Bluetooth Low Energy (BLE) via `bleak`
* **Architecture:** Object-Oriented Driver Design

### Usage
```python
from drivers.bolt_driver import BoltDriver

# The 'with' block handles the secure connection handshake
with BoltDriver("SB-B386") as bot:
    # Direct hardware call via custom driver
    bot.scroll_text("SYSTEM ONLINE", 255, 0, 0)