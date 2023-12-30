# import time
# from respeaker import PixelRing

# pixel_ring = PixelRing()  # Initialize the pixel ring

# # pixel_ring.set_brightness(10)  # Set brightness

# # Set the LEDs to red
# pixel_ring.set_color(r=255, g=0, b=0)

# time.sleep(3)  # Keep the color for 3 seconds

# # Turn off the LEDs
# pixel_ring.off()

import time

from pixel_ring import pixel_ring


if __name__ == '__main__':
    pixel_ring.change_pattern('echo')
    while True:

        try:
            pixel_ring.wakeup()
            time.sleep(3)
            pixel_ring.think()
            time.sleep(3)
            pixel_ring.speak()
            time.sleep(6)
            pixel_ring.off()
            time.sleep(3)
        except KeyboardInterrupt:
            break


    pixel_ring.off()
    time.sleep(1)
