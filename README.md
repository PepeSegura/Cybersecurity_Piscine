# Installation in HOST

Create a virtual enviroment to install the libraries from requirements.txt

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

# Installation with DOCKER

Create container sand-box with the required libraries for the program to work

    make

# Usage

    usage: stockholm.py [-h] [-v VERSION] [-r KEY] [-s]

    Encrypt all files in $HOME/infection

    options:
    -h, --help              show this help message and exit
    -v, --version           shows program version.
    -r KEY, --reverse KEY   key used to decrypt files.
    -s, --silent            hide program output.
