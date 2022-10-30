""" display difference between a file(indexed) and another file(not indexed) """
import shelve

import util
from constants import OBJ_DIR, BRANCH_DIR, HEAD_PATH, INDEX_PATH
from hashlib import sha256
import difflib
import os


def diff_strstr(str1, str2):
    """ 
        Input:
        2 strings

        Output:
        Their difference
    """

    list1 = str1.splitlines()
    list2 = str2.splitlines()

    for line in difflib.unified_diff(list1, list2, fromfile='Commited File',
                                     tofile='Staged File', lineterm=''):
        if line[0] in ['+', '-']:
            print(line)


def diff_util(blob_hash, file_path):
    """ 
        find the diff between commited file and the file in working directory

        Input:
        blob_hash = name of blob object
        file_path = name of file in working directory

        Output:
        Their differences
    """

    # with open(os.path.join(OBJ_DIR, blob_hash), 'rb') as f:
    #     commit_obj_file = f.read()

    with open(file_path, 'r') as f:
        current_file = f.read()

    # commit_obj_file = zlib.decompress(commit_obj_file)

    commit_obj_file = util.decompress_file(blob_hash)
    print("Difference:", file_path)
    print("commit_obj_file: ", commit_obj_file)

    diff_strstr(commit_obj_file.decode('utf-8'), current_file)



def diff(file_path):
    """ 
        Input:
        file or a directory

        print the diff of a file

        if the input is a directory, 
        print diff of all the file in that directory
        (recursive)
    """
    if os.path.isfile(file_path):
        commited_file_hash = util.get_sha_from_index(file_path)

        if (commited_file_hash == None):
            print("New file:", file_path)
        else:
            diff_util(commited_file_hash, file_path)

    elif os.path.isdir(file_path):
        for filename in os.listdir(file_path):
            f = os.path.join(file_path, filename)

            if os.path.isfile(f):
                commited_file_hash = util.get_sha_from_index(f)
                if (commited_file_hash == None):
                    print("New file:", f)
                else:
                    diff_util(commited_file_hash, f)

            elif os.path.isdir(f):
                diff(f)


# if __name__ == '__main__':
#     diff(sys.argv[1])
