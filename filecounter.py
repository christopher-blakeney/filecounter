import os
import re
import argparse
from pathlib import Path

__author__ = "Christopher J. Blakeney"
__version__ = "0.1.0"
__license__ = ""

"""TODO
- Test on many directories
- Test in every circumstance
- Fix txt ouput
"""


def count_files(txt, detail, path, show_hidden, show_files):
    n = 0
    hidden_files = 0
    t_hidden_files = 0
    for dirpath, dirname, filenames in os.walk(path):
        # count hidden files for each dir
        for f in filenames:
            if f[0] == ".":
                hidden_files += 1
                t_hidden_files += 1
        # if show hidden false, subtract files and dirs beginning with "." from the filenames and dirname list
        if show_hidden == False:
            for f in filenames:
                filenames = [f for f in filenames if not f[0] == "."]

        c = len(filenames) - hidden_files
        n += c

        # txt file option == True
        if txt:
            txt_file = open(f"{path}/summary.txt", "w")
            if detail:
                txt_file.write(
                    f"\nPATH: {dirpath}\n\n    >> {c} real files | {hidden_files} hidden | {c + hidden_files} total\n"
                )
            if show_files:
                for i in filenames:
                    txt_file.write(f"\n        - {i}")
                    txt_file.write("\n")

            # reset hidden files for next dir in loop
            hidden_files = 0
            txt_file.write(
                f"\nTOTALS: {n} real files | {t_hidden_files} hidden | {n + t_hidden_files} total\n"
            )
            txt_file.close()
            print("\nSuccess! Summary file placed in directory.\n")
        # cmd option
        else:
            if detail:
                print(
                    f"\nPATH: {dirpath}\n\n    >> {c} real files | {hidden_files} hidden | {c + hidden_files} total\n"
                )
            if show_files:
                for i in filenames:
                    print(f"\n        - {i}")
            hidden_files = 0
    print(
        f"\nTOTALS: {n} real files | {t_hidden_files} hidden | {n + t_hidden_files} total\n"
    )


def main():
    # CLI
    parser = argparse.ArgumentParser(
        prog="filecounter",
        description="Count the files within a directory",
        epilog="Thanks for using filecounter... Developed by Christopher Blakeney",
    )
    general = parser.add_argument_group("general output")
    general.add_argument("path")

    detailed = parser.add_argument_group("detailed output")
    detailed.add_argument(
        "-d",
        "--subdircount",
        action="store_true",
        default=False,
        help="show totals for each subdirectory within path",
    )

    out_loc = parser.add_argument_group("output location")
    out_loc.add_argument(
        "-txt",
        "--txtfile",
        action="store_true",
        default=False,
        help="output to summary.txt file in specified path",
    )
    out_loc.add_argument(
        "-cmd",
        "--cmdline",
        action="store_true",
        default=True,
        help="output to command line (default)",
    )

    parser.add_argument(
        "-f",
        "--showfilenames",
        action="store_true",
        default=False,
        help="show files within given path",
    )
    args = parser.parse_args()
    target_dir = Path(args.path)

    if not target_dir.exists():
        print("The target directory doesn't exist")
        raise SystemExit(1)

    filenames_flag = args.showfilenames
    txt_flag = args.txtfile
    detail_flag = args.subdircount
    show_hidden = True

    count_files(txt_flag, detail_flag, target_dir, show_hidden, filenames_flag)


if __name__ == "__main__":
    # This is executed when run from the command line
    main()
