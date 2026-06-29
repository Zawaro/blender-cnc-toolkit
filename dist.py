#!/usr/bin/env python3
"""Build distribution packages for all addon variants."""

import argparse
import os
import subprocess
import sys
import zipfile

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(REPO_ROOT, ".dist")

TOOLKITS = {
  "hi_five": os.path.join(REPO_ROOT, "hi_five"),
  "eevee_next": os.path.join(REPO_ROOT, "eevee_next"),
  "cyclesx": os.path.join(REPO_ROOT, "cyclesx"),
}

EXCLUDE_DIRS = {".venv", "__pycache__", ".git", "docs"}
TOOLKIT_EXCLUDE_FILES = {
  "cyclesx": {"blender_manifest.toml"},
}


def get_build_number():
  try:
    result = subprocess.run(
      ["git", "rev-list", "--count", "HEAD"],
      cwd=REPO_ROOT,
      capture_output=True,
      text=True,
      check=True,
    )
    return result.stdout.strip()
  except (subprocess.CalledProcessError, FileNotFoundError):
    return "0"


def get_version():
  version_path = os.path.join(REPO_ROOT, "version.txt")
  if not os.path.exists(version_path):
    return "0.0.0"
  with open(version_path, "r") as f:
    return f.read().strip()


def zip_addon(name, addon_dir, build_number):
  version = get_version()
  filename = f"{name}_{version}_build{build_number}.zip"
  zip_path = os.path.join(DIST_DIR, filename)

  build_file = os.path.join(addon_dir, "_build.py")
  with open(build_file, "w") as f:
    f.write(f'BUILD_NUMBER = "{build_number}"\n')

  exclude = TOOLKIT_EXCLUDE_FILES.get(name, set())

  try:
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
      for foldername, dirnames, filenames in os.walk(addon_dir):
        dirnames[:] = [
          d for d in dirnames
          if d not in EXCLUDE_DIRS and not d.startswith(".")
        ]
        for filename in filenames:
          if filename in exclude:
            continue
          file_path = os.path.join(foldername, filename)
          arcname = os.path.relpath(file_path, addon_dir)
          zipf.write(file_path, arcname)

    print(f"  {zip_path}")
    return zip_path
  finally:
    if os.path.exists(build_file):
      os.remove(build_file)


def parse_args():
  variants = list(TOOLKITS.keys())
  parser = argparse.ArgumentParser(description="Build addon distribution zips")
  group = parser.add_mutually_exclusive_group()
  group.add_argument("--all", action="store_true", help="Build all variants")
  group.add_argument("--variant", choices=variants, help="Build a specific variant")
  return parser.parse_args()


def prompt_choice():
  variants = list(TOOLKITS.keys())
  print("Select toolkit to build:")
  for i, v in enumerate(variants, 1):
    print(f"  {i}) {v}")
  print(f"  {len(variants) + 1}) all")
  print()
  while True:
    choice = input(f"Enter choice [1-{len(variants) + 1}]: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(variants) + 1:
      return int(choice)
    print(f"Invalid choice. Enter 1-{len(variants) + 1}.")


def main():
  args = parse_args()
  variants = list(TOOLKITS.keys())

  if args.all:
    selected = variants[:]
  elif args.variant:
    selected = [args.variant]
  else:
    choice = prompt_choice()
    if choice <= len(variants):
      selected = [variants[choice - 1]]
    else:
      selected = variants[:]

  os.makedirs(DIST_DIR, exist_ok=True)
  build_number = get_build_number()

  print(f"\nBuild {build_number}")
  print(f"Output: {DIST_DIR}/\n")

  for name in selected:
    addon_dir = TOOLKITS[name]
    if not os.path.isdir(addon_dir):
      print(f"  ERROR: {addon_dir} not found")
      continue
    zip_addon(name, addon_dir, build_number)

  print("\nDone.")


if __name__ == "__main__":
  main()
