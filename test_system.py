from drivers.bolt_driver import BoltDriver
from assets.faces import SMILEY

ROBOT_NAME = "SB-B386"

def run_test():
    # usage: 'with' handles the connection automatically now
    try:
        with BoltDriver(ROBOT_NAME) as bot:
            print("Test 1: Matrix")
            bot.draw_face(SMILEY, 0, 255, 0)
            time.sleep(2) # Admire the face
            
            print("Test 2: Scrolling Text")
            bot.scroll_text("SYSTEM ONLINE", 255, 0, 0)
            
            print("Test Complete.")
            
    except Exception as e:
        print(f"\n[MISSION FAILED] {e}")

if __name__ == "__main__":
    import time # Needed for the sleep above
    run_test()