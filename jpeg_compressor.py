#!/usr/bin/env python3
"""
JPEG Image Compressor
A tool to compress JPEG images with customizable quality settings.
"""

import os
import sys
import argparse
from pathlib import Path
from PIL import Image
import piexif


def get_file_size(filepath):
    """Get file size in KB."""
    return os.path.getsize(filepath) / 1024


def compress_jpeg(input_path, output_path=None, quality=85, optimize=True, preserve_exif=True):
    """
    Compress a JPEG image.

    Args:
        input_path: Path to input image
        output_path: Path to output image (if None, overwrites input)
        quality: JPEG quality (1-100, default 85)
        optimize: Enable optimization (default True)
        preserve_exif: Preserve EXIF metadata (default True)

    Returns:
        dict: Compression statistics
    """
    try:
        # Open image
        img = Image.open(input_path)

        # Convert to RGB if necessary (handles RGBA, P, etc.)
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Get original file size
        original_size = get_file_size(input_path)

        # Handle EXIF data
        exif_bytes = None
        if preserve_exif:
            try:
                exif_dict = piexif.load(input_path)
                exif_bytes = piexif.dump(exif_dict)
            except:
                # If EXIF loading fails, continue without it
                pass

        # Determine output path
        if output_path is None:
            output_path = input_path

        # Save compressed image
        save_kwargs = {
            'quality': quality,
            'optimize': optimize,
            'progressive': True
        }

        if exif_bytes:
            save_kwargs['exif'] = exif_bytes

        img.save(output_path, 'JPEG', **save_kwargs)

        # Get compressed file size
        compressed_size = get_file_size(output_path)

        # Calculate compression ratio
        compression_ratio = ((original_size - compressed_size) / original_size) * 100

        return {
            'success': True,
            'input': str(input_path),
            'output': str(output_path),
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': compression_ratio
        }

    except Exception as e:
        return {
            'success': False,
            'input': str(input_path),
            'error': str(e)
        }


def compress_directory(directory, output_dir=None, quality=85, optimize=True,
                       preserve_exif=True, recursive=False):
    """
    Compress all JPEG images in a directory.

    Args:
        directory: Input directory path
        output_dir: Output directory path (if None, overwrites originals)
        quality: JPEG quality (1-100)
        optimize: Enable optimization
        preserve_exif: Preserve EXIF metadata
        recursive: Process subdirectories recursively

    Returns:
        list: List of compression statistics for each file
    """
    results = []
    pattern = '**/*.jp*g' if recursive else '*.jp*g'

    # Create output directory if specified
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Find all JPEG files
    directory_path = Path(directory)
    jpeg_files = []

    for ext in ['*.jpg', '*.jpeg', '*.JPG', '*.JPEG']:
        if recursive:
            jpeg_files.extend(directory_path.rglob(ext))
        else:
            jpeg_files.extend(directory_path.glob(ext))

    # Process each file
    for input_file in jpeg_files:
        if output_dir:
            # Maintain directory structure in output
            rel_path = input_file.relative_to(directory_path)
            output_file = Path(output_dir) / rel_path
            output_file.parent.mkdir(parents=True, exist_ok=True)
        else:
            output_file = None

        result = compress_jpeg(
            input_file,
            output_file,
            quality=quality,
            optimize=optimize,
            preserve_exif=preserve_exif
        )
        results.append(result)

    return results


def print_results(results):
    """Print compression results in a formatted way."""
    total_original = 0
    total_compressed = 0
    successful = 0
    failed = 0

    print("\n" + "="*80)
    print("COMPRESSION RESULTS")
    print("="*80 + "\n")

    for result in results:
        if result['success']:
            successful += 1
            total_original += result['original_size']
            total_compressed += result['compressed_size']

            print(f"✓ {result['input']}")
            print(f"  Original: {result['original_size']:.2f} KB")
            print(f"  Compressed: {result['compressed_size']:.2f} KB")
            print(f"  Reduction: {result['compression_ratio']:.2f}%\n")
        else:
            failed += 1
            print(f"✗ {result['input']}")
            print(f"  Error: {result['error']}\n")

    print("="*80)
    print(f"Processed: {len(results)} files")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")

    if successful > 0:
        total_reduction = ((total_original - total_compressed) / total_original) * 100
        print(f"\nTotal original size: {total_original:.2f} KB")
        print(f"Total compressed size: {total_compressed:.2f} KB")
        print(f"Total space saved: {total_original - total_compressed:.2f} KB ({total_reduction:.2f}%)")
    print("="*80 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Compress JPEG images with customizable quality settings.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compress a single image with 80% quality
  %(prog)s image.jpg -q 80

  # Compress and save to a different file
  %(prog)s input.jpg -o output.jpg -q 75

  # Compress all JPEGs in a directory
  %(prog)s /path/to/images/ -q 85

  # Compress recursively and save to output directory
  %(prog)s /path/to/images/ -o /path/to/output/ -r -q 80
        """
    )

    parser.add_argument('input', help='Input JPEG file or directory')
    parser.add_argument('-o', '--output', help='Output file or directory')
    parser.add_argument('-q', '--quality', type=int, default=85,
                       help='JPEG quality (1-100, default: 85)')
    parser.add_argument('--no-optimize', action='store_true',
                       help='Disable optimization')
    parser.add_argument('--no-exif', action='store_true',
                       help='Do not preserve EXIF metadata')
    parser.add_argument('-r', '--recursive', action='store_true',
                       help='Process directories recursively')

    args = parser.parse_args()

    # Validate quality
    if not 1 <= args.quality <= 100:
        print("Error: Quality must be between 1 and 100", file=sys.stderr)
        sys.exit(1)

    # Check if input exists
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input path '{args.input}' does not exist", file=sys.stderr)
        sys.exit(1)

    # Process file or directory
    if input_path.is_file():
        # Single file compression
        result = compress_jpeg(
            args.input,
            args.output,
            quality=args.quality,
            optimize=not args.no_optimize,
            preserve_exif=not args.no_exif
        )
        print_results([result])

        if not result['success']:
            sys.exit(1)

    elif input_path.is_dir():
        # Directory compression
        results = compress_directory(
            args.input,
            args.output,
            quality=args.quality,
            optimize=not args.no_optimize,
            preserve_exif=not args.no_exif,
            recursive=args.recursive
        )

        if not results:
            print("No JPEG files found in the specified directory", file=sys.stderr)
            sys.exit(1)

        print_results(results)

        if all(not r['success'] for r in results):
            sys.exit(1)
    else:
        print(f"Error: '{args.input}' is not a valid file or directory", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
