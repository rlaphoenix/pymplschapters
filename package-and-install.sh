rm -r build
rm -r dist
rm -r "pyd2v.egg-info"
python3 setup.py sdist bdist_wheel
sudo pip install .