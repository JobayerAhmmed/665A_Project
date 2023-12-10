import fileinput
import os
import subprocess
import shutil
import fnmatch

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


def find_files_with_text(start_dir, file_pattern, search_text):
    """Search for files containing specific text in a directory."""
    matching_files = []
    for root, dirs, files in os.walk(start_dir):
        for filename in fnmatch.filter(files, file_pattern):
            file_path = os.path.join(root, filename)
            with open(file_path, 'r') as file:
                if search_text in file.read():
                    matching_files.append(file_path)
    return matching_files


def find_files(start_dir, file_pattern):
    """Search specific file in a directory."""
    matching_files = []
    for root, dirs, files in os.walk(start_dir):
        for filename in fnmatch.filter(files, file_pattern):
            file_path = os.path.join(root, filename)
            matching_files.append(file_path)
    return matching_files


def fix_rsource():
    """Replace rsource attribute by source with relative paths.
    
    Few Kconfig files contain rsource to connect to other Kconfig
    files in a directory. AutoConfDoc does not work on rsource
    because it uses kextract which does not recognize rsoure.
    """
    print('Fixing rsource tags from Kconfig files...')

    file_pattern = 'Kconfig'
    search_text = 'rsource "*/Kconfig"'
    kconfig_files = find_files_with_text(config.px4_src_dir, file_pattern,
                                            search_text)

    for file_path in kconfig_files:
        file_dir = os.path.dirname(file_path)
        dir_kconfig_files = find_files(file_dir, file_pattern)
        replacement_text = ''
        for item in dir_kconfig_files:
            # Exclude Kconfig file from the current directory
            if item == file_path:
                continue
            rel_path = os.path.relpath(item, config.px4_src_dir)
            replacement_text += 'source "' + rel_path + '"\n'
        replacement_text = replacement_text.strip()
        with fileinput.FileInput(file_path, inplace=True) as f:
            for line in f:
                print(line.replace(search_text, replacement_text), end='')


def replace_text(file_path, search_text, replacement_text):
    with fileinput.FileInput(file_path, inplace=True) as f:
        for line in f:
            print(line.replace(search_text, replacement_text), end='')


def fix_others():
    """Since src/examples directory is excluded from documentation,
    exclude source attribute from top-level Kconfig file for src/examples.
    Also, fix 'rsource "Kconfig.topics"' in src/modules/zenoh/Kconfig.
    """
    file_path = os.path.join(config.px4_src_dir, 'Kconfig')
    search_text = 'source "src/examples/Kconfig"'
    replacement_text = '# source "src/examples/Kconfig"'
    replace_text(file_path, search_text, replacement_text)

    search_text = 'source "src/lib/*/Kconfig"'
    replacement_text = 'source "src/lib/cdrstream/Kconfig"'
    replace_text(file_path, search_text, replacement_text)

    file_path = os.path.join(config.px4_src_dir, 'src', 'modules', 'zenoh',
                             'Kconfig')
    search_text = 'rsource "Kconfig.topics"'
    replacement_text = 'source "src/modules/zenoh/Kconfig.topics"'
    replace_text(file_path, search_text, replacement_text)
    


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
    r = subprocess.run(['./../665A_Project/libs/autoconfdoc', 'Doxyfile'])
    if r.returncode != 0:
        print('Failed to run AutonConfDoc!')


if __name__ == "__main__":
    clone_repo()
    fix_help()
    fix_rsource()
    fix_others()
    copy_doxyfile()
    run_autoconfdoc()
    pass