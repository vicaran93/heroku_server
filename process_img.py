#!/usr/bin/env python
import sys
#import Image

if len(sys.argv) < 2:print("No input detected")
else:
    who = sys.argv[1]
    print("Hello the bucket received is : " + who + " .")
#image = Image.open('File.jpg')
#image.show()