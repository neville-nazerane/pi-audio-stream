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
from gpiozero import LED
import inspect


power = LED(5)
power.on()

pixel_ring.set_brightness(50)

# if __name__ == '__main__':
#     while True:

#         try:
#             pixel_ring.wakeup()
#             time.sleep(3)
#             pixel_ring.think()
#             time.sleep(3)
#             pixel_ring.speak()
#             time.sleep(6)
#             pixel_ring.off()
#             time.sleep(3)
#         except KeyboardInterrupt:
#             break


#     pixel_ring.off()
#     time.sleep(1)

functions_list = inspect.getmembers(pixel_ring, inspect.isfunction)

print("Functions in pixel_ring:")
for func in functions_list:
    print(func[0])

functions_list = inspect.getmembers(power, inspect.isfunction)

print("Functions in power:")
for func in functions_list:
    print(func[0])
    
while True:
    input('LETS GO!')
    pixel_ring.wakeup()
    time.sleep(3)
    pixel_ring.off()

power.off()