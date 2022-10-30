import os
import util
from constants import BRANCH_DIR, OBJ_DIR


def create_branch(name):
    branch_file = os.path.join(BRANCH_DIR, name)
    if os.path.exists(branch_file):
        print("branch already exists")
        return

    with open(branch_file, "w") as f:
        f.write(util.get_last_commit_hash())
        print("branch created")