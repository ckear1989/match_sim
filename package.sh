#!/bin/bash

# python3 -m pip install --user --upgrade setuptools wheel

sudo python3 setup.py sdist bdist_wheel

pip3 install dist/match_sim-ckear-0.0.1.tar.gz --verbose

# sudo python3 setup.py install

