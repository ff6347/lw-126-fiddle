#!/usr/bin/env python3
"""Create a sample JPEG image for testing the compressor."""

from PIL import Image, ImageDraw, ImageFont
import random

# Create a large image with some content
width, height = 2000, 1500
image = Image.new('RGB', (width, height))
draw = ImageDraw.Draw(image)

# Create a gradient background
for y in range(height):
    r = int(255 * (y / height))
    g = int(128 * (1 - y / height))
    b = int(200 * (y / height))
    draw.rectangle([(0, y), (width, y + 1)], fill=(r, g, b))

# Add some shapes
for _ in range(50):
    x1 = random.randint(0, width)
    y1 = random.randint(0, height)
    x2 = random.randint(x1, min(x1 + 300, width))
    y2 = random.randint(y1, min(y1 + 300, height))
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    draw.rectangle([x1, y1, x2, y2], fill=color, outline='white', width=3)

# Add some circles
for _ in range(30):
    x = random.randint(0, width)
    y = random.randint(0, height)
    r = random.randint(20, 100)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    draw.ellipse([x - r, y - r, x + r, y + r], fill=color, outline='black', width=2)

# Add text
try:
    # Try to use a default font
    draw.text((width // 2 - 200, height // 2), "Sample JPEG Image", fill='white')
except:
    pass

# Save as high-quality JPEG
image.save('sample_image.jpg', 'JPEG', quality=95)
print("Created sample_image.jpg (high quality, ~2000x1500 pixels)")
