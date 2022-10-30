import os
import shelve
import util
from constants import VCS_BASE, INDEX_PATH

# how does git add check for changes ?


# modified flag will be reset at commit


def stage(file_path, modified):
    # create a blob object
    sha = util.compress_file(file_path)['sha256']

    entry = util.Entry(file_path, sha, os.stat(file_path), modified)
    print("entry: ", entry)
    print(type(entry))

    with shelve.open(INDEX_PATH) as index:
        index[file_path] = entry


def add(path):
    if os.path.isdir(path):
        for filename in os.listdir(path):
            if filename != VCS_BASE:
                add(os.path.join(path, filename))
    else:
        try:
            # index_stat = get_entry(file_path).stat
            # modified = file_stat != index_stat
            index_sha = util.get_entry_from_index(path).sha
            # print(index_sha)
            file_sha = util.compute_sha(path)
            # print(file_sha)
            modified = file_sha != index_sha
            print(modified)
            if not modified:
                return
        except AttributeError:
            modified = True

        # if modified - create blob object of the file and add to staging area
        stage(path, modified)


# if __name__ == '__main__':
#     fpath = sys.argv[1]
#     add(fpath)

    # print(util.get_modified_entries())
    # print(util.get_modified_entries()[0].modified if util.get_modified_entries() else "")
