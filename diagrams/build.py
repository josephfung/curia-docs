#!/usr/bin/env python3
"""Regenerate the docs diagrams in assets/ from the scripts in this folder.

    python3 diagrams/build.py                  # write every diagram to assets/
    python3 diagrams/build.py --check          # fail if any asset differs from its script
    python3 diagrams/build.py --preview DIR    # write square previews (and PNGs on macOS) to DIR

Standard library only; no install step.
"""
import argparse
import importlib
import os
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True  # keep __pycache__ out of the repo (there's no .gitignore)

HERE =os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")

# One module per diagram. Each defines OUT (the file name in assets/) and build(square=False) -> str.
DIAGRAMS = [
    "deployment_architecture",
    "multi_agent_architecture",
    "architecture_message_flow",
    "governance_gates",
    "autonomy_bands",
]


def load(name):
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    return importlib.import_module(name)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("names", nargs="*", help="diagram modules to build (default: all)")
    p.add_argument("--check", action="store_true", help="compare with assets/ instead of writing")
    p.add_argument("--preview", metavar="DIR", help="write square preview SVGs (and PNGs via Quick Look on macOS)")
    args = p.parse_args()

    names = args.names or DIAGRAMS
    unknown = [n for n in names if n not in DIAGRAMS]
    if unknown:
        p.error(f"unknown diagram(s): {', '.join(unknown)}. Known: {', '.join(DIAGRAMS)}")

    stale = []
    for name in names:
        mod = load(name)
        if args.preview:
            os.makedirs(args.preview, exist_ok=True)
            path = os.path.join(args.preview, mod.OUT)
            with open(path, "w") as f:
                f.write(mod.build(square=True))
            print(f"preview  {path}")
            continue
        svg = mod.build()
        path = os.path.join(ASSETS, mod.OUT)
        current = open(path).read() if os.path.exists(path) else None
        if args.check:
            if current != svg:
                stale.append(mod.OUT)
                print(f"STALE    assets/{mod.OUT} (edited by hand, or its script changed without a rebuild)")
            else:
                print(f"ok       assets/{mod.OUT}")
            continue
        with open(path, "w") as f:
            f.write(svg)
        print(f"{'wrote' if current != svg else 'same '}    assets/{mod.OUT}")

    if args.preview and shutil.which("qlmanage"):
        files = [os.path.join(args.preview, load(n).OUT) for n in names]
        subprocess.run(["qlmanage", "-t", "-s", "2200", "-o", args.preview, *files],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        print(f"PNGs     {args.preview}/*.svg.png (Quick Look)")

    if stale:
        print(f"\n{len(stale)} diagram(s) out of date. Run: python3 diagrams/build.py", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
