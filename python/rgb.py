import time
from respeaker import PixelRing

pixel_ring = PixelRing()  # Initialize the pixel ring
print(dir(pixel_ring))

exit()

pixel_ring.set_brightness(10)  # Set brightness

# Set the LEDs to red
pixel_ring.set_color(r=255, g=0, b=0)

time.sleep(3)  # Keep the color for 3 seconds

# Turn off the LEDs
pixel_ring.off()
