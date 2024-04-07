#!/usr/sbin/python

import os
import sys
import shutil
import argparse
from pathlib import Path


CWD = Path.cwd()
NOTES_PARENT_DIR = Path("/home/trevor/notes/Courses/PEN-200/Boxes/")
TEMPLATE_DIR = Path("/home/trevor/notes/z_templates/")

DIRECTORIES = ["vulns", "files", "nmap"]
FILES = ["users.txt", "creds.txt", "passwords.txt", "hashes.txt", "notes.txt"]
MACHINES = ["MS01", "MS02", "DC01"]
STANDALONES = ["SA1", "SA2", "SA3"]
NOTES_DIRS = ["Services", "images"]
NOTES_FILES = ["Nmap", "Notes"]


def parse_args():
    parser = argparse.ArgumentParser(
        prog="new_box.py",
        description="Create directory and notes for a new box.",
        epilog="Example: python new_box.py Flimsy",
    )

    parser.add_argument("box_name", type=str, help="Name of box.")
    parser.add_argument("-e", "--exam", action="store_true", help="Set up the folder for the exam")
    return parser.parse_args()


def create_directory(parent_path, name):
    new_dir = parent_path.joinpath(name)
    os.makedirs(new_dir, exist_ok=True)
    return new_dir


def create_files(parent_path):
    for file in FILES:
        with open(parent_path.joinpath(file), "w") as f:
            pass


def create_directories(parent_path, dir_list):
    for d in dir_list:
        create_directory(parent_path, d)


def copy_template(template_name, dest_name, parent_path):
    shutil.copyfile(TEMPLATE_DIR.joinpath(template_name), parent_path.joinpath(dest_name))


def copy_templates(box_name, parent_path, file_list):
    copy_template("Storyboard.md", f"{box_name} - Storyboard.md", parent_path)
    for f in file_list:
        copy_template(f"{f}.md", f"{f}.md", parent_path)


def create_local_structure(args):
    # Creates the local files and directories
    box_name = args.box_name
    exam = args.exam
    box_dir = create_directory(CWD, box_name)

    if exam:
        # Active Directory
        ad_dir = create_directory(box_dir, "AD")
        create_files(ad_dir)
        for m in MACHINES:
            machine_dir = create_directory(ad_dir, m)
            create_directories(machine_dir, DIRECTORIES)
            create_files(machine_dir)

        # Stand Alones
        for s in STANDALONES:
            sa_dir = create_directory(box_dir, s)
            create_files(sa_dir)
            create_directories(sa_dir, DIRECTORIES)
    else:
        create_files(box_dir)
        create_directories(box_dir, DIRECTORIES)


def create_notes_structure(args):
    # Creates the obsidian notes files and directories
    box_name = args.box_name
    exam = args.exam
    notes_dir = create_directory(NOTES_PARENT_DIR, box_name)

    if exam:
        # Active Directory
        ad_dir = create_directory(notes_dir, "AD")
        for file in ["Notes.md"]:
            with open(ad_dir.joinpath(file), "w") as f:
                pass
        copy_template("Verified Creds.md", "Verified Creds.md", ad_dir)
        for m in MACHINES:
            machine_dir = create_directory(ad_dir, m)
            create_directories(machine_dir, NOTES_DIRS)
            copy_templates(m, machine_dir, NOTES_FILES)
        # Stand Alones
        sa_dir = create_directory(notes_dir, "SA")
        for s in STANDALONES:
            machine_dir = create_directory(sa_dir, s)
            copy_templates(s, machine_dir, NOTES_FILES)
            create_directories(machine_dir, NOTES_DIRS)

    else:
        create_directories(notes_dir, NOTES_DIRS)
        copy_templates(box_name, notes_dir, NOTES_FILES)


def main(_args):
    create_local_structure(_args)
    create_notes_structure(_args)


if __name__ == "__main__":
    _args = parse_args()
    main(_args)
