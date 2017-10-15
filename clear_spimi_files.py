"""Utility command to clear SPIMI index blocks"""
import shutil
import os

def deleteblocks():
    """ Delete directories and files under ./index_blocks"""
    for root, directories, files in os.walk('./index_blocks'):
        for f in files:
            os.unlink(os.path.join(root, f))
        for directory in directories:
            shutil.rmtree(os.path.join(root, directory))

if __name__ == '__main__':
    print('Deleting existing SPIMI blocks...')
    deleteblocks()
    print('Clearing SPIMI inverted index...')
    open('spimi_inverted_index.txt', 'w').close()
    print('Complete!')
