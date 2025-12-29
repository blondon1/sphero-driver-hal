from drivers.bolt_driver import BoltDriver
from assets.faces import SMILEY

ROBOT_NAME = "SB-B386"

def run_test():
    bot = BoltDriver(ROBOT_NAME)
    bot.connect()
    
    print("Test 1: Matrix")
    bot.draw_face(SMILEY, 0, 255, 0)
    
    print("Test 2: Scrolling Text (Long)")
    # This tests the auto-chunking logic we built
    bot.scroll_text("SYSTEM ONLINE: PREPARING FOR AI INTEGRATION", 255, 0, 0)
    
    print("Test Complete.")

if __name__ == "__main__":
    run_test()