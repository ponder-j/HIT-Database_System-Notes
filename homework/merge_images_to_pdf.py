#!/usr/bin/env python3
"""
merge_images_to_pdf.py

将指定图片合并为一个 PDF 文件。

用法示例:
  python3 merge_images_to_pdf.py -o out.pdf img1.jpg img2.png img3.tif
  python3 merge_images_to_pdf.py --list images.txt --output out.pdf

依赖: Pillow
  pip3 install --user pillow
"""
from pathlib import Path
import argparse
import sys
from PIL import Image


def read_list_file(list_path: Path):
    try:
        text = list_path.read_text(encoding='utf-8')
    except Exception:
        text = list_path.read_text(encoding='latin-1')
    lines = [l.strip() for l in text.splitlines()]
    return [l for l in lines if l]


def load_images(paths):
    imgs = []
    for p in paths:
        path = Path(p)
        if not path.exists():
            print(f"Warning: file not found: {p}", file=sys.stderr)
            continue
        try:
            im = Image.open(path)
            # Convert to RGB (PDF doesn't support alpha)
            if im.mode in ("RGBA", "LA") or (im.mode == "P" and 'transparency' in im.info):
                bg = Image.new("RGB", im.size, (255, 255, 255))
                bg.paste(im, mask=im.split()[-1])
                im = bg
            else:
                im = im.convert("RGB")
            imgs.append(im)
        except Exception as e:
            print(f"Error opening {p}: {e}", file=sys.stderr)
    return imgs


def merge_to_pdf(images, output_path: Path):
    if not images:
        raise ValueError("No valid images to write to PDF.")
    first, rest = images[0], images[1:]
    # Use Pillow's save with append_images
    first.save(output_path, "PDF", resolution=100.0, save_all=True, append_images=rest)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Merge images into a single PDF (preserve order).")
    parser.add_argument('images', nargs='*', help='Image files (jpg/png/...) to include, order is preserved')
    parser.add_argument('-l', '--list', dest='list_file', help='Path to a text file with one image path per line')
    parser.add_argument('-o', '--output', dest='output', default='merged.pdf', help='Output PDF file name')
    args = parser.parse_args(argv)

    paths = []
    if args.list_file:
        list_path = Path(args.list_file)
        if not list_path.exists():
            print(f"List file not found: {list_path}", file=sys.stderr)
            sys.exit(2)
        paths.extend(read_list_file(list_path))

    if args.images:
        paths.extend(args.images)

    if not paths:
        print("No images provided. Provide image paths or use --list.", file=sys.stderr)
        parser.print_help()
        sys.exit(2)

    images = load_images(paths)
    if not images:
        print("No valid images could be opened. Exiting.", file=sys.stderr)
        sys.exit(1)

    out = Path(args.output)
    try:
        merge_to_pdf(images, out)
        print(f"Saved PDF: {out}")
    except Exception as e:
        print(f"Failed to write PDF: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
