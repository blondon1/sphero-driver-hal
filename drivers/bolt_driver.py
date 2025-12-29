import time
from spherov2 import scanner

class BoltDriver:
    def __init__(self, robot_name):
        self.robot_name = robot_name
        self.toy = None

    def __enter__(self):
        """
        SYSTEMS ENGINEERING: Resource Management
        finds the robot and LOCKS the Bluetooth connection open.
        """
        print(f"Searching for {self.robot_name}...")
        for attempt in range(1, 4):
            try:
                self.toy = scanner.find_toy(toy_name=self.robot_name)
                if self.toy:
                    print(f"[OK] Found {self.robot_name}. Connecting...")
                    # This line manually triggers the library's context manager
                    self.toy.__enter__() 
                    self.toy.wake()
                    time.sleep(2) # Allow 2s for the radio to stabilize
                    return self
                print(f"[Attempt {attempt}] Retrying scan...")
            except Exception as e:
                print(f"[Error] {e}")
            time.sleep(1)
        raise ConnectionError("Could not find robot.")

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Cleanly closes the connection when the 'with' block ends.
        """
        if self.toy:
            print("Closing connection...")
            self.toy.set_raw_motors(0, 0, 0, 0) # Safety Stop
            self.toy.__exit__(exc_type, exc_value, traceback)

    # --- ACTIONS (No longer need 'with self.toy' inside these) ---

    def draw_face(self, face_map, r, g, b):
        self.toy.set_compressed_frame_player_one_color(0, 0, 0) # Clear
        for y, row in enumerate(face_map):
            for x, pixel in enumerate(row):
                if pixel == '1':
                    self.toy.set_compressed_frame_player_pixel(x, y, r, g, b)

    def scroll_text(self, text, r, g, b, speed=10):
        if len(text) < 15:
            self.toy.set_compressed_frame_player_text_scrolling(text, r, g, b, speed, False)
            time.sleep(len(text) * 0.3)
        else:
            chunks = [text[i:i+15] for i in range(0, len(text), 15)]
            for chunk in chunks:
                print(f"  -> Scrolling chunk: '{chunk}'")
                self.toy.set_compressed_frame_player_text_scrolling(chunk, r, g, b, speed, False)
                duration = (len(chunk) * 0.25) + 1.0 
                time.sleep(duration)