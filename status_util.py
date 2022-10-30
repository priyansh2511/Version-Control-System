""" Display the status of files; Tracked, Untracked, Tracked and Modifyed """

import util
from constants import VCS_BASE, CWD
import os


# def get_modified_status(filepath):
#     with shelve.open(INDEX_PATH) as index:
#         try:
#             return index[filepath].modified
#         except KeyError:
#             return


class ANSI():
    def background(code):
        return "\33[{code}m".format(code=code)

    def style_text(code):
        return "\33[{code}m".format(code=code)

    def color_text(code):
        return "\33[{code}m".format(code=code)


def print_red(message):
    encoding = ANSI.background(1) + ANSI.color_text(49) + ANSI.style_text(
        31) + message
    encoding += ANSI.background(0) + ANSI.color_text(0) + ANSI.style_text(0)
    print(encoding)


def print_yellow(message):
    encoding = ANSI.background(0) + ANSI.color_text(49) + ANSI.style_text(
        93) + message
    encoding += ANSI.background(0) + ANSI.color_text(0) + ANSI.style_text(0)
    print(encoding)


def print_green(message):
    encoding = ANSI.background(1) + ANSI.color_text(49) + ANSI.style_text(
        32) + message
    encoding += ANSI.background(0) + ANSI.color_text(0) + ANSI.style_text(0)
    print(encoding)


def print_purple(message):
    encoding = ANSI.background(1) + ANSI.color_text(49) + ANSI.style_text(
        95) + message
    encoding += ANSI.background(0) + ANSI.color_text(0) + ANSI.style_text(0)
    print(encoding)


tracked = []
tracked_modified = []
untracked = []


def status_util(file_path):
    if os.path.isfile(file_path):
        # modified_status = get_modified_status(file_path)
        print(file_path)
        index_file_sha = util.get_sha_from_index(file_path)
        print("status util index file sha: ", index_file_sha)
        print(index_file_sha)
        if index_file_sha == None:
            untracked.append(file_path)
        else:
            file_sha = util.compute_sha(file_path)
            print("status util file sha", file_sha)
            if file_sha != index_file_sha:
                tracked_modified.append(file_path)
            else:
                tracked.append(file_path)

    elif os.path.isdir(file_path):
        for file_name in os.listdir(file_path):
            if file_name != os.path.basename(VCS_BASE):
                status_util(os.path.join(file_path, file_name))


def status():
    status_util(CWD)
    # status_util(".")

    print_purple("STATUS")
    print_green("HEAD=" + util.get_head_content())

    if len(tracked) != 0:
        print_purple("\nTracked files:")
        for file in tracked:
            print_green(file)

    if len(tracked_modified) != 0:
        print_purple("\nModified files:")
        for file in tracked_modified:
            print_red(file)

    if len(untracked) != 0:
        print_purple("\nUntracked files:")
        for file in untracked:
            print_yellow(file)
