import os
import util
from constants import CWD

# obj_directory = '.objs'
directory = ".vcs"



# entry = {
#     'mode' : '',
#     'name' : "",
#     "sha" : '',
#     'type' : ''
# }

# get_staged_files
# {
# 'base':{
#     'files' : {'index.html',}   #dict
#     'dirs':{
#         'lib':{
#             'files' : {}   #dict
#               'dirs':{}
#         },
#         'lib2':{

#         }
#     }
# }
# }



def reform_commit_tree(staged_files: dict, tree_dict: dict, tree_path: str) -> str:
    """Reformation of a tree based on the staged files

    Args:
        staged_files (dict): tree hierarchy directory structure object
        tree_dict (dict): tree object which was stored in the previous commit
        tree_path (str): file path

    Returns:
        str: returns the sha of the directory tree
    """
    tree = dict()
    tree["name"] = tree_dict["name"]
    tree_entries = []

    new_entries = set()

    for entry in tree_dict["entries"]:
        if staged_files['dirs'] and entry["name"] in staged_files["dirs"].keys():
            sub_tree_dict = util.decompress_tree(entry["sha"])
            
            if not sub_tree_dict:
                print("error, tree dict not found for hash- ", entry["sha"])

            tree_obj = dict()
            tree_obj["name"] = entry["name"]
            tree_obj["sha"] = reform_commit_tree(
                staged_files["dirs"][entry["name"]],
                sub_tree_dict,
                os.path.join(tree_path, entry["name"]),
            )
            tree_obj["mode"] = os.stat(
                os.path.join(CWD, os.path.join(tree_path, entry["name"]))
            ).st_mode
            tree_obj["type"] = "tree"
            tree_entries.append(tree_obj)
            new_entries.add(entry["name"])

        elif staged_files['files'] and entry["name"] in staged_files["files"].keys():
            blob_obj = dict()
            blob_obj["name"] = entry["name"]
            blob_obj["sha"] = staged_files["files"][entry["name"]].sha
            blob_obj["mode"] = staged_files["files"][entry["name"]].stat.st_mode
            blob_obj["type"] = "blob"
            tree_entries.append(blob_obj)
            new_entries.add(entry["name"])

    if staged_files["dirs"]:
        for entry in staged_files["dirs"].keys():
            if entry not in new_entries:
                tree_obj = dict()
                tree_obj["sha"] = new_commit_tree_helper(
                    staged_files["dirs"][entry], os.path.join(tree_path, entry)
                )
                tree_obj["type"] = "tree"
                tree_obj["mode"] = os.stat(
                    os.path.join(CWD, os.path.join(tree_path, entry))
                ).st_mode
                tree_obj["name"] = entry

                tree_entries.append(tree_obj)

    if staged_files["files"]:
        for entry in staged_files["files"].keys():
            if entry not in new_entries:
                blob_obj = dict()
                blob_obj["name"] = entry
                blob_obj["sha"] = staged_files["files"][entry].sha
                blob_obj["mode"] = staged_files["files"][entry].stat.st_mode
                blob_obj["type"] = "blob"

                tree_entries.append(blob_obj)

    for entry in tree_dict["entries"]:
        if entry["name"] not in new_entries:
            tree_entries.append(entry)

    tree["entries"] = tree_entries

    return util.compress_tree(tree)


def new_commit_tree_helper(staged_files: dict, tree_path: str) -> str:
    """Formation of a new tree based on the staged files

    Args:
        staged_files (dict): tree hierarchy directory structure object
        tree_path (str): file path

    Returns:
        str: returns the sha of the directory tree
    """
    tree = dict()
    tree["name"] = os.path.split(tree_path)[1]
    tree_entries = list()

    if staged_files["dirs"]:
        for entry in staged_files["dirs"].keys():
            tree_obj = dict()
            tree_obj["sha"] = new_commit_tree_helper(
                staged_files["dirs"][entry], os.path.join(tree_path, entry)
            )
            tree_obj["type"] = "tree"
            tree_obj["mode"] = os.stat(
                os.path.join(CWD, os.path.join(tree_path, entry))
            ).st_mode
            tree_obj["name"] = entry

            tree_entries.append(tree_obj)

    if staged_files["files"]:
        for entry in staged_files["files"].keys():
            blob_obj = dict()
            blob_obj["name"] = entry
            blob_obj["sha"] = staged_files["files"][entry].sha
            blob_obj["mode"] = staged_files["files"][entry].stat.st_mode
            blob_obj["type"] = "blob"
            tree_entries.append(blob_obj)

    tree["entries"] = tree_entries

    return util.compress_tree(tree)


def new_commit_tree(staged_files: dict) -> str:
    """For a new root tree formation
    mainly for the first commit.

    Args:
        staged_files (dict): tree hierarchy directory structure object

    Returns:
        str: returns the sha of the directory tree
    """
    tree_name = ''
    # tree_name = os.path.split(CWD)[1]
    # print(tree_name)
    return new_commit_tree_helper(staged_files[tree_name], tree_name)


def commit_tree() -> str:
    """Used for the formation of the new tree object.
    Called each time we make a new commit.

    Returns:
        str: sha of the newly formed tree. None if there are no files to commit
    """
    added_values = get_staged_tree()
    
    if not added_values:
        print('Nothing to commit')
        return
    main_tree_sha = util.get_last_commit_hash()
    if main_tree_sha:
        main_tree = util.decompress_tree(util.decompress_tree(main_tree_sha)['tree'])
        # print(main_tree)
        if main_tree["name"] in added_values.keys():
            return reform_commit_tree(added_values[main_tree["name"]], main_tree,
                          main_tree["name"])

    return new_commit_tree(added_values)


def get_staged_tree() -> dict:
    """Convert List of Entries to tree structure

    Returns:
        dict: modified/staged tree object
    """
    modified_entries = util.get_modified_entries()
    if len(modified_entries) == 0:
        return
    staged_tree = dict()
    common_object = {"files": None, "dirs": None}
    root_dir_name = ''
    # root_dir_name = os.path.split(CWD)[1]
    staged_tree[root_dir_name] = {**common_object}

    for entry in modified_entries:
        file_path_parts = os.path.normpath(entry.file_path).split(os.sep)
        i = 0
        while i < len(file_path_parts):
            if file_path_parts[i] == '.':
                file_path_parts.pop(i)
            else:
                i += 1
        file_path_parts = file_path_parts[1:]
        curr_dir = staged_tree[root_dir_name]
        for part in file_path_parts[:-1]:
            if not curr_dir["dirs"]:
                curr_dir["dirs"] = dict()
            if part not in curr_dir["dirs"]:
                curr_dir["dirs"][part] = {**common_object}
            curr_dir = curr_dir["dirs"][part]

        if not curr_dir["files"]:
            curr_dir["files"] = dict()
        curr_dir["files"][file_path_parts[-1]] = entry

    print("get_staged_tree ", staged_tree)
    return staged_tree


# def commit_tree():
# objs = os.listdir()
# if not objs:
#     #objs folder empty
#     print('nothing to commit')
#     return

# def initial_check():
#     #check if .vcs folder is present in the same directory
#     if(os.path.exists(path)):
#         os.chdir(path)

#         #check if objs folder present
#         if os.path.exists(obj_path):
#             os.chdir(obj_path)
#             commit_tree()
#     else:
#         print('first run init')


# def new_commit_tree_helper(filepath):
#     tree_entries = list()

#     for something in list(os.listdir(filepath)):
#         new_path = os.path.join(filepath, something)
#         if(os.path.isdir(new_path)):
#             entry = new_commit_tree_helper(new_path)
#             entry['type'] = 'tree'
#             tree.append(entry)

#         elif(os.path.isfile(new_path)):
#             entry = addblob(new_path)
#             entry['type'] = 'blob'
#             tree.append(entry)

#     tree = dict()
#     tree['name'] = os.path.split(filepath)[1]
#     tree['entries'] = tree_entries
#     entry = add_blob(tree)
#     return entry
