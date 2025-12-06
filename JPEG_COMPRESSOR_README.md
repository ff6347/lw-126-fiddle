# JPEG Image Compressor

A powerful and flexible command-line tool for compressing JPEG images with customizable quality settings.

## Features

- **Single File Compression**: Compress individual JPEG images
- **Batch Processing**: Compress all JPEGs in a directory
- **Recursive Processing**: Process subdirectories recursively
- **Quality Control**: Adjust compression quality (1-100)
- **EXIF Preservation**: Option to preserve or remove EXIF metadata
- **Optimization**: Built-in optimization for smaller file sizes
- **Progressive JPEG**: Generates progressive JPEGs for better web loading
- **Detailed Statistics**: Shows compression ratios and space saved

## Installation

1. Install Python 3.6 or higher
2. Install dependencies:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install Pillow piexif
```

## Usage

### Basic Usage

Make the script executable (Linux/Mac):
```bash
chmod +x jpeg_compressor.py
```

Compress a single image:
```bash
python jpeg_compressor.py image.jpg
```

### Command-Line Options

```
usage: jpeg_compressor.py [-h] [-o OUTPUT] [-q QUALITY] [--no-optimize]
                          [--no-exif] [-r]
                          input

positional arguments:
  input                 Input JPEG file or directory

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file or directory
  -q QUALITY, --quality QUALITY
                        JPEG quality (1-100, default: 85)
  --no-optimize         Disable optimization
  --no-exif             Do not preserve EXIF metadata
  -r, --recursive       Process directories recursively
```

### Examples

**Compress a single image with 80% quality:**
```bash
python jpeg_compressor.py image.jpg -q 80
```

**Compress and save to a different file:**
```bash
python jpeg_compressor.py input.jpg -o output.jpg -q 75
```

**Compress all JPEGs in a directory:**
```bash
python jpeg_compressor.py /path/to/images/ -q 85
```

**Compress recursively with output to a different directory:**
```bash
python jpeg_compressor.py /path/to/images/ -o /path/to/output/ -r -q 80
```

**Compress without preserving EXIF data:**
```bash
python jpeg_compressor.py image.jpg --no-exif -q 80
```

**Maximum compression (lower quality):**
```bash
python jpeg_compressor.py image.jpg -q 50
```

## Quality Guidelines

- **90-100**: Minimal compression, excellent quality (suitable for archival)
- **80-89**: Good compression, high quality (recommended for most uses)
- **70-79**: Moderate compression, good quality (suitable for web)
- **50-69**: High compression, acceptable quality (web thumbnails)
- **1-49**: Maximum compression, lower quality (not recommended)

## Output Format

The tool provides detailed compression statistics:

```
================================================================================
COMPRESSION RESULTS
================================================================================

✓ /path/to/image1.jpg
  Original: 1234.56 KB
  Compressed: 456.78 KB
  Reduction: 63.00%

✓ /path/to/image2.jpg
  Original: 2345.67 KB
  Compressed: 789.12 KB
  Reduction: 66.36%

================================================================================
Processed: 2 files
Successful: 2
Failed: 0

Total original size: 3580.23 KB
Total compressed size: 1245.90 KB
Total space saved: 2334.33 KB (65.20%)
================================================================================
```

## Use as a Python Module

You can also import and use the compressor in your Python scripts:

```python
from jpeg_compressor import compress_jpeg, compress_directory

# Compress a single image
result = compress_jpeg('input.jpg', 'output.jpg', quality=80)
print(f"Saved {result['compression_ratio']:.2f}%")

# Compress a directory
results = compress_directory('/path/to/images', quality=85, recursive=True)
for result in results:
    if result['success']:
        print(f"Compressed {result['input']}")
```

## Technical Details

- **Image Format Handling**: Automatically converts non-RGB images (RGBA, P, etc.) to RGB
- **Progressive JPEG**: All compressed images use progressive encoding for better web performance
- **EXIF Support**: Uses piexif library to preserve camera and photo metadata
- **Optimization**: Enables Pillow's built-in optimization algorithms
- **Error Handling**: Gracefully handles errors and continues processing other files

## Troubleshooting

**Issue**: "No module named 'PIL'"
- **Solution**: Install Pillow: `pip install Pillow`

**Issue**: EXIF data not preserved
- **Solution**: Ensure piexif is installed: `pip install piexif`
- **Note**: Some images may not have EXIF data or it may be corrupted

**Issue**: "Image file is truncated"
- **Solution**: The source image may be corrupted. Try opening it in an image editor first.

## License

This project is licensed under the same license as the repository.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.
