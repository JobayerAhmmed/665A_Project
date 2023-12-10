# 665A Project

## Generate Documentation by AutoConfDoc

### Install Requirements

- `sudo apt update`
- `sudo apt install -y flex bison make cmake git wget unzip python3 python3-pip python3-venv python3-setuptools python3-dev`

### Install kextractor
- `mkdir px4_doc && cd px4_doc`
- `python3 -m venv px4_venv`
- `source px4_venv/bin/activate`
- `git clone -b kextract --single-branch https://github.com/JobayerAhmmed/kmax.git`
- `cd kmax`
- `python3 setup.py install`
- `cd ..`

### Install AutoConfDoc

- `git clone -b dev --single-branch https://github.com/JobayerAhmmed/kconfig_doc.git`
- `cd kconfig_doc/doxygen`
- `mkdir build && cd build`
- `cmake -G "Unix Makefiles" ..`
- `sudo make install`
- `cd ../../..`

### Setup 665A Project and Generate PX4 Documentation

- `git clone https://github.com/JobayerAhmmed/665A_Project.git`
- `git clone https://github.com/PX4/PX4-Autopilot.git`
- `cp ./665A_Project/Doxyfile ./PX4-Autopilot/Doxyfile`
- `python3 gen_doc.py`