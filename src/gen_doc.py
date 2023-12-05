import fileinput
import os
import subprocess
import shutil

import config



def run_gen_doc():
    # clone_repo()
    fix_help()
    pass


def clone_repo():
    """Clone a repository and put the code in the temp directory."""
    os.chdir(config.temp_dir)

    if os.path.exists(config.px4_dir):
        shutil.rmtree(config.px4_dir)
        create_dir(config.px4_dir)
        r = subprocess.run(["git", "clone", config.px4_repo_url, config.px4_dir])
        if r.returncode != 0:
            print("Failed to clone repo {}".format(config.px4_repo_url))
    else:
        create_dir(config.px4_dir)
        r = subprocess.run(["git", "clone", config.px4_repo_url, config.px4_dir])
        if r.returncode != 0:
            print("Failed to clone repo {}".format(config.px4_repo_url))


def create_dir(dir: str):
    """Creates directory and subdirectories if not exist.
    
    Parameters
    ----------
    dir : str
        Pathname of the directory to be created.
    """
    if not os.path.isdir(dir):
        os.makedirs(dir)


def fix_help():
    """Remove tripple dash from the start and 
    end of help attributes in Kconfig files.
    """
    search_text = '---help---'
    replacement_text = 'help'
    for root, dirs, files in os.walk(config.px4_dir):
        for filename_o in files:
            if not filename_o.endswith('Kconfig'):
                continue
            filepath = os.path.join(root, filename_o)
            with fileinput.FileInput(filepath, inplace=True) as f:
                for line in f:
                    print(line.replace(search_text, replacement_text), end='')

