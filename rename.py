#!/usr/bin/env python3
"""Batch-rename files in a directory.

Rename files matching a glob pattern with a combination of operations:
replace a substring, add a prefix/suffix, change case, change the
extension, or append a zero-padded sequence number.

Usage:
    python rename.py photos/ "*.jpg" --replace "IMG_" "vacation_" --prefix "2026-"
    python rename.py docs/ "*.txt" --lower --number --start 1 --pad 3
    python rename.py . "*.md" --ext txt --dry-run

Run with --dry-run first to preview the plan; without it the renames
are applied. Collisions (a target name that already exists) are skipped
and reported instead of overwriting anything.
"""

import argparse
import sys
from pathlib import Path


def build_new_name(path: Path, args, index: int) -> str:
    """Compute the new file name for *path* given the CLI options."""
    stem = path.stem
    suffix = path.suffix

    if args.replace:
        old, new = args.replace
        stem = stem.replace(old, new)
    if args.lower:
        stem = stem.lower()
    if args.upper:
        stem = stem.upper()
    if args.prefix:
        stem = args.prefix + stem
    if args.suffix:
        stem = stem + args.suffix
    if args.number:
        stem = f"{stem}{args.separator}{index:0{args.pad}d}"
    if args.ext is not None:
        suffix = f".{args.ext.lstrip('.')}" if args.ext else ""
    return stem + suffix


def plan(directory: Path, pattern: str, args):
    """Return a list of (source, target) pairs, sorted by file name."""
    files = sorted(p for p in directory.glob(pattern) if p.is_file())
    pairs = []
    for i, path in enumerate(files, start=args.start):
        new_name = build_new_name(path, args, i)
        target = path.with_name(new_name)
        if target != path:
            pairs.append((path, target))
    return pairs


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Batch-rename files matching a pattern.")
    parser.add_argument("directory", type=Path,
                        help="directory containing the files")
    parser.add_argument("pattern", help="glob pattern, e.g. '*.jpg'")
    parser.add_argument("--replace", nargs=2, metavar=("OLD", "NEW"),
                        help="replace substring OLD with NEW in the name")
    parser.add_argument("--prefix", help="text to prepend to the name")
    parser.add_argument("--suffix", help="text to append to the name")
    parser.add_argument("--lower", action="store_true",
                        help="lowercase the file name")
    parser.add_argument("--upper", action="store_true",
                        help="uppercase the file name")
    parser.add_argument("--number", action="store_true",
                        help="append a sequence number to the name")
    parser.add_argument("--start", type=int, default=1,
                        help="first sequence number (default: 1)")
    parser.add_argument("--pad", type=int, default=3,
                        help="zero-padding width for numbers (default: 3)")
    parser.add_argument("--separator", default="_",
                        help="separator before the number (default: '_')")
    parser.add_argument("--ext", metavar="EXT",
                        help="change the extension, e.g. txt (empty string removes it)")
    parser.add_argument("--dry-run", action="store_true",
                        help="show the plan without renaming anything")
    args = parser.parse_args(argv)

    if not args.directory.is_dir():
        print(f"error: not a directory: {args.directory}", file=sys.stderr)
        return 2
    if args.lower and args.upper:
        print("error: --lower and --upper cannot be combined",
              file=sys.stderr)
        return 2

    pairs = plan(args.directory, args.pattern, args)
    if not pairs:
        print("nothing to rename")
        return 0

    renamed, skipped = 0, 0
    for source, target in pairs:
        if target.exists():
            print(f"SKIP  {source.name} -> {target.name} (target exists)")
            skipped += 1
            continue
        print(f"{'PLAN ' if args.dry_run else 'RENAME'}  "
              f"{source.name} -> {target.name}")
        if not args.dry_run:
            source.rename(target)
            renamed += 1

    if args.dry_run:
        print(f"{len(pairs)} file(s) would be renamed, {skipped} skipped")
    else:
        print(f"{renamed} renamed, {skipped} skipped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
