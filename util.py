import hashlib
import zlib
import os
import pickle
import shelve
from constants import OBJ_DIR, INDEX_PATH, HEAD_PATH, BRANCH_DIR


class Entry:
    def __init__(self, file_path, sha, stat, modified=False):
        self.file_path = file_path
        self.sha = sha
        self.stat = stat
        self.modified = modified


def compute_sha(path):
    with open(path, 'rb') as file:
        data = file.read()
        hash = hashlib.sha256(data).hexdigest()
        return hash


def compress_file(path):
    data = open(path, 'rb').read()
    hash = hashlib.sha256(data).hexdigest()
    c_data = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
    f = open(os.path.join(OBJ_DIR, hash), 'wb')
    f.write(c_data)
    f.close()
    perm = oct(os.stat(path).st_mode)[2:]
    fname = os.path.basename(path)
    dic = {}
    dic['filename'] = fname
    dic['permissions'] = perm
    dic['sha256'] = hash
    return dic


def compress_tree(dic):
    data = pickle.dumps(dic)
    hash = hashlib.sha256(data).hexdigest()
    c_data = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
    f = open(os.path.join(OBJ_DIR, hash), 'wb')
    f.write(c_data)
    f.close()
    # perm = oct(os.stat(os.path.join(OBJ_DIR, hash)).st_mode)[2:]
    # fname = os.path.basename(os.path.join(OBJ_DIR, hash))
    # dic = {}
    # dic['filename'] = fname
    # dic['permissions'] = perm
    # dic['sha256'] = hash
    return hash


def decompress_file(hash, path=None):
    data = open(os.path.join(OBJ_DIR, hash), 'rb').read()
    data = zlib.decompress(data)
    print('path: ', path)
    print("decompress file: ", data)
    if path is not None:
        f = open(path, 'wb')
        f.write(data)
        f.close()
    return data


def decompress_tree(hash):
    data = open(os.path.join(OBJ_DIR, hash), 'rb').read()
    data = zlib.decompress(data)
    dic = pickle.loads(data)
    return dic


def get_head_content():
    data = open(HEAD_PATH).read()
    print("get_head: ", data)
    return data


def set_head_content(content):
    with open(HEAD_PATH, "w") as head:
        head.write(content)


def get_branch_content(name):
    try:
        print(name)
        data = open(os.path.join(BRANCH_DIR, name)).read()
        print(data)
        return data
    except Exception as e:
        return


def set_branch_content(name, content):
    with open(os.path.join(BRANCH_DIR, name), "w") as branch:
        branch.write(content)


def create_branch(name):
    content = get_branch_content(get_head_content())
    set_branch_content(name, content)


def delete_branch(name):
    if name == get_head_content():
        print("cannot delete current branch")
        return
    os.remove(os.path.join(BRANCH_DIR, name))


def get_last_commit_hash():
    head_content = get_head_content()
    branch_content = get_branch_content(head_content)
    if branch_content is None:
        return head_content

    return branch_content


def get_modified_entries():
    """
    :return: list of entries that are new or modified in the index file
    """
    modified_entries = []
    with shelve.open(INDEX_PATH) as index:
        for key in index.keys():
            print(key)
            entry = index[key]
            if entry.modified:
                modified_entries.append(entry)
    return modified_entries


def get_sha_from_index(filepath):
    with shelve.open(INDEX_PATH) as index:
        try:
            sha = index[filepath].sha
            return sha
        except KeyError:
            return


def set_modified_status(filepath, modified):
    with shelve.open(INDEX_PATH) as index:
        try:
            entry = index[filepath]
            entry.modified = modified
            index[filepath] = entry
        except KeyError:
            return


def decompress_commit(commit_hash):
    try:
        with open(os.path.join(OBJ_DIR, commit_hash), 'rb') as commit_obj:
            data = zlib.decompress(commit_obj.read())
            return pickle.loads(data)
    except:
        return


def get_entry_from_index(filepath):
    with shelve.open(INDEX_PATH) as index:
        try:
            return index[filepath]
        except KeyError:
            return


def update_index_entry(filepath, entry):
    with shelve.open(INDEX_PATH) as index:
        index[filepath] = entry
