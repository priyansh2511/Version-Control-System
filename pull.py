import os
import shutil
from constants import CWD
import util
from checkout import checkout_util


def pull_from_remote(src):
    if(os.path.isfile(src)):
        print("Source should be a folder")
        return
    if os.path.exists(CWD):
        shutil.rmtree(CWD)
    shutil.copytree(src, CWD)
    commit_hash = util.get_last_commit_hash()
    print(commit_hash)
    commit = util.decompress_commit(commit_hash)
    print("commit: ", commit)
    checkout_util(commit['tree'])



# if __name__ == "__main__":
#     pull_from_remote("./folder/")
