import os
import shutil
from constants import CWD
import util

def push_util(tree_hash, path=CWD):
    tree = util.decompress_tree(tree_hash)
    for entry in tree['entries']:
        print("tree entry: ", entry)
        if entry['type'] == 'blob':
            util.decompress_file(entry['sha'],
                                 os.path.join(path, entry['name']))
        else:
            dir_path = os.path.join(path, entry['name'])
            print(dir_path)
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
            push_util(entry['sha'], dir_path)

def push_to_remote(des):
    if(os.path.isfile(des)):
        print("Destination should be a folder")
        return
    if os.path.exists(des):
        shutil.rmtree(des)
    shutil.copytree(CWD, des)
    commit_hash = util.get_last_commit_hash()
    commit = util.decompress_commit(commit_hash)
    print("commit: ", commit)
    push_util(commit['tree'],path=des)



# if __name__ == "__main__":
#     push_to_remote("./folder/")
