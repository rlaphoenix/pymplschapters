# pymplschapters

[![License](https://img.shields.io/github/license/rlaphoenix/pymplschapters)](https://github.com/rlaphoenix/pymplschapters/blob/master/LICENSE)
[![Python version tests](https://img.shields.io/github/workflow/status/rlaphoenix/pymplschapters/Build)](https://github.com/rlaphoenix/pymplschapters/releases)
[![Python versions](https://img.shields.io/pypi/pyversions/pymplschapters)](https://pypi.python.org/pypi/pymplschapters)
[![PyPI version](https://img.shields.io/pypi/v/pymplschapters)](https://pypi.python.org/pypi/pymplschapters)
[![GitHub issues](https://img.shields.io/github/issues/rlaphoenix/pymplschapters)](https://github.com/rlaphoenix/pymplschapters/issues)
[![DeepSource issues](https://deepsource.io/gh/rlaphoenix/pymplschapters.svg/?label=active+issues)](https://deepsource.io/gh/rlaphoenix/pymplschapters)

Extract chapters from a Blu-ray .mpls to a Matroska recognized XML file.

## Installation

    pip install pymplschapters

## Usage

    pymplschapters -p "C:\Path\To\The\Playlist.mpls"

It will place any found chapters next to the input playlist file or to a specified directory with `-d`.

## Credit

Thanks [PyGuymer](https://github.com/Guymer/PyGuymer) for the MPLS parsing code, it
has been modified a bit to suit my needs.
