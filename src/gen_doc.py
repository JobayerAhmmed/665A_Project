import fileinput
import os
import subprocess
import shutil

import config



def clone_repo():
    """Clone a repository and put the code in the px4 directory."""
    print('Cloning PX4-Autopilot repository...')
    os.chdir(config.root_dir)

    if os.path.exists(config.px4_src_dir):
        shutil.rmtree(config.px4_src_dir)
        create_dir(config.px4_src_dir)
        r = subprocess.run(["git", "clone", config.px4_repo_url,
                            config.px4_src_dir])
        if r.returncode != 0:
            print("Failed to clone repo {}".format(config.px4_repo_url))
    else:
        create_dir(config.px4_src_dir)
        r = subprocess.run(["git", "clone", config.px4_repo_url,
                            config.px4_src_dir])
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
    print('Fixing Kconfig help attribute...')
    search_text = '---help---'
    replacement_text = 'help'
    for root, dirs, files in os.walk(config.px4_src_dir):
        for filename_o in files:
            if not filename_o.endswith('Kconfig'):
                continue
            filepath = os.path.join(root, filename_o)
            with fileinput.FileInput(filepath, inplace=True) as f:
                for line in f:
                    print(line.replace(search_text, replacement_text), end='')


def fix_rsource():
    """Replace rsource attribute by source with relative paths.
    
    Few Kconfig files contain rsource to connect to other Kconfig
    files in a directory. AutoConfDoc does not work on rsource
    because it uses kextract which does not recognize rsoure.
    """
    print('Fixing rsource tags from Kconfig files...')
    pass


def copy_doxyfile():
    """Copy Doxyfile from 665A_Project directory to PX4-Autopilot."""
    print('Copying Doxyfile to PX4-Autopilot directory...')
    os.chdir(config.root_dir)
    r = subprocess.run(['cp', '665A_Project/Doxyfile', 
                        'PX4-Autopilot/Doxyfile'])
    if r.returncode != 0:
        print('Failed to copy Doxyfile to PX4-Autopilot directory!')


def run_autoconfdoc():
    """Run AutoConfDoc to generate documentation."""
    print('Running AutoConfDoc...')
    os.chdir(config.px4_src_dir)
    r = subprocess.run(['./../665A_Project/libs/doxygen', 'Doxyfile'])
    if r.returncode != 0:
        print('Failed to run AutonConfDoc!')


if __name__ == "__main__":
    clone_repo()
    fix_help()
    fix_rsource()
    copy_doxyfile()
    run_autoconfdoc()
    pass