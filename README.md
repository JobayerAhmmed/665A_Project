# 665A Project

The project is developed and experimented on Linux (Ubuntu 22.04 LTS) with Python 3.10.12 

## Generate Documentation by AutoConfDoc

### Install Requirements

- `sudo apt update`
- `sudo apt install -y flex bison make cmake git wget unzip python3 python3-pip python3-venv python3-setuptools python3-dev`

### Setup Project
- `mkdir px4_doc && cd px4_doc`
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install pandas plotly lxml`
- `git clone -b kextract --single-branch https://github.com/JobayerAhmmed/kmax.git`
- `cd kmax`
- `python3 setup.py install`
- `cd ..`
- `git clone https://github.com/JobayerAhmmed/665A_Project.git`

### Generate PX4 Documentation

- `cd 665A_Project/src/`
- `python3 gen_doc.py`