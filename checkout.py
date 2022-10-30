import util
import shutil
from constants import CWD
import os
import shelve

# TODO: instead of CWD relative path should be here
# TODO: or change the entire file path pattern
def checkout_util(tree_hash, path=CWD):
    tree = util.decompress_tree(tree_hash)
    print(tree)
    for entry in tree['entries']:
        print("tree entry: ", entry)
        if entry['type'] == 'blob':
            file_path = os.path.join(path, entry['name'])
            util.decompress_file(entry['sha'], file_path)

            # update index entry
            print("checkou util: ", entry['sha'])
            print("checkout util file path", file_path)
            new_entry = util.Entry(file_path,
                                   entry['sha'],
                                   os.stat(file_path),
                                   False)
            util.update_index_entry(file_path, new_entry)
        else:
            dir_path = os.path.join(path, entry['name'])
            print(dir_path)
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
            checkout_util(entry['sha'], dir_path)


def checkout(name):
    # do nothing if current commit hash is passed
    commit_hash = name
    branch_content = util.get_branch_content(name)
    if branch_content is not None:
        # # if same branch, do nothing
        # if name == util.get_head_content():
        #     return
        commit_hash = branch_content

    # if commit_hash != util.get_branch_content(util.get_head_content()):
    # decompress commit
    commit = util.decompress_commit(commit_hash)
    if commit is None:
        print("No such branch or commit")
        return
    print("commit: ", commit)

    # delete existing files
    for filename in os.listdir(CWD):
        if filename != '.vcs':
            filepath = os.path.join(CWD, filename)
            if os.path.isdir(filepath):
                shutil.rmtree(filepath)
            else:
                os.remove(filepath)

    # create files from checkout
    checkout_util(commit['tree'])

    # modify HEAD
    if branch_content is not None:
        util.set_head_content(name)
    else:
        util.set_head_content(commit_hash)


# if __name__ == '__main__':
#     # commit_hash = util.get_branch_content(util.get_head_content())
#     print(sys.argv[1])
#     checkout(sys.argv[1])
