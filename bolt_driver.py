import time
from spherov2 import scanner
from spherov2.types import Color

class BoltDriver:
    def __init__(self, robot_name):
        self.robot_name = robot_name
        self.toy = None

    def connect(self):
        """Robust connection loop with retries."""
        print(f"Searching for {self.robot_name}...")
        for attempt in range(1, 4):
            try:
                self.toy = scanner.find_toy(toy_name=self.robot_name)
                if self.toy:
                    print(f"[OK] Found {self.robot_name}. Waking up...")
                    return self.toy
                print(f"[Attempt {attempt}] Retrying scan...")
            except Exception as e:
                print(f"[Error] {e}")
            time.sleep(1)
        raise ConnectionError("Could not find robot.")

    def wake(self):
        """Keeps the connection alive."""
        if self.toy:
            with self.toy:
                self.toy.wake()

    def draw_face(self, face_map, r, g, b):
        """Draws an 8x8 pixel map using the raw driver."""
        with self.toy:
            self.toy.set_compressed_frame_player_one_color(0, 0, 0) # Clear
            for y, row in enumerate(face_map):
                for x, pixel in enumerate(row):
                    if pixel == '1':
                        self.toy.set_compressed_frame_player_pixel(x, y, r, g, b)

    def scroll_text(self, text, r, g, b, speed=10):
        """
        Manages the 'Pedro Logic': Splits long text and handles timing.
        """
        with self.toy:
            # If text is short, just send it
            if len(text) < 15:
                self.toy.set_compressed_frame_player_text_scrolling(text, r, g, b, speed, False)
                time.sleep(len(text) * 0.3) # Auto-calc duration
            else:
                # Chunking logic for long messages
                chunks = [text[i:i+15] for i in range(0, len(text), 15)]
                for chunk in chunks:
                    print(f"  -> Scrolling chunk: '{chunk}'")
                    self.toy.set_compressed_frame_player_text_scrolling(chunk, r, g, b, speed, False)
                    # The Magic Number we learned: 0.25s per character + buffer
                    duration = (len(chunk) * 0.25) + 1.0 
                    time.sleep(duration)