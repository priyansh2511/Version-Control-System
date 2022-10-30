from checkout import checkout
import util

def rollback():
    checkout(util.get_head_content())