#!/usr/bin/env python3
"""Build distribution packages for hi_five and/or eevee_next addons."""

import ast
import os
import re
import shutil
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
EXCLUDE_FILES = {"zip_hi_five.py", "zip_eevee_next.py", "_build.py"}


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


def get_version(addon_dir):
  init_path = os.path.join(addon_dir, "__init__.py")
  with open(init_path, "r") as f:
    content = f.read()
  match = re.search(r'bl_info\s*=\s*(\{.*?\})', content, re.DOTALL)
  if not match:
    return "0.0.0"
  bl_info = ast.literal_eval(match.group(1))
  version = bl_info.get("version", (0, 0, 0))
  return ".".join(str(v) for v in version)


def zip_addon(name, addon_dir, build_number):
  version = get_version(addon_dir)
  filename = f"{name}_{version}_build{build_number}.zip"
  zip_path = os.path.join(DIST_DIR, filename)

  build_file = os.path.join(addon_dir, "_build.py")
  with open(build_file, "w") as f:
    f.write(f'BUILD_NUMBER = "{build_number}"\n')

  try:
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
      for foldername, dirnames, filenames in os.walk(addon_dir):
        dirnames[:] = [
          d for d in dirnames
          if d not in EXCLUDE_DIRS and not d.startswith(".")
        ]
        for filename in filenames:
          if filename in EXCLUDE_FILES:
            continue
          file_path = os.path.join(foldername, filename)
          arcname = os.path.relpath(file_path, addon_dir)
          zipf.write(file_path, arcname)

    print(f"  {zip_path}")
    return zip_path
  finally:
    if os.path.exists(build_file):
      os.remove(build_file)


def prompt_choice():
  print("Select toolkit to build:")
  print("  1) hi_five")
  print("  2) eevee_next")
  print("  3) cyclesx")
  print("  4) all")
  print()
  while True:
    choice = input("Enter choice [1-4]: ").strip()
    if choice in ("1", "2", "3", "4"):
      return choice
    print("Invalid choice. Enter 1, 2, 3, or 4.")


def main():
  choice = prompt_choice()
  if choice == "1":
    selected = ["hi_five"]
  elif choice == "2":
    selected = ["eevee_next"]
  elif choice == "3":
    selected = ["cyclesx"]
  else:
    selected = ["hi_five", "eevee_next", "cyclesx"]

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
