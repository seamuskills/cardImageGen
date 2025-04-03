from PIL import Image
import os
import sys

if (len(sys.argv) <= 1):
    print("arguments: <image path> [size (S/M/L)] [output directory]")

try:
    image = Image.open(sys.argv[1])
except FileNotFoundError:
    print("Image file could not be found.")
    sys.exit()

debug = "template" in sys.argv

size = sys.argv[2][0] if len(sys.argv) >= 3 else 'M'
print("target card size %s"%(size))
outPath = sys.argv[3] if len(sys.argv) >= 4 else os.path.dirname(sys.argv[1])
if (outPath == ''):
    print("target directory %s"%(os.getcwd()))
else:
    print("target directory %s"%(outPath))

print("original size %dx%d"%(image.size[0], image.size[1]))

y = 0

size = size.upper()
if not size in ["S", "M", "L"]:
    size = "M"
    print("invalid size. defaulting to M")

match (size):
    case 'S':
        y = 200
    case 'M':
        y = 250
    case 'L':
        y = 300

#this decides with based on height while keeping the existing aspect ratio of the image.
x = round((y/image.size[1]) * image.size[0])

image = image.resize((x, y))
print("new size %sx%s"%(image.size[0], image.size[1]))

final = Image.new(image.mode, (image.size[0], image.size[1] * 3), (0, 0, 0, 0))
if debug:
    final = Image.open("cardTemplate.png")
    final.paste(image, (476 - image.size[0]//2, 937 - image.size[1]))
    print("using debug template.")
else:
    final.paste(image, (0, 0))

final.save(os.path.join(outPath, "output.png"))
