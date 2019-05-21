# Minecraft Enchantments Generator (*mc_enchant*)
> *Little utility to facilitate with generating the code needed to spawn enchanted objects in Minecraft*

![Python version][python-version]
![Latest version][latest-version]
[![Build Status][travis-image]][travis-url]
[![BCH compliance][bch-image]][bch-url]
[![GitHub issues][issues-image]][issues-url]
[![GitHub forks][fork-image]][fork-url]
[![GitHub Stars][stars-image]][stars-url]
[![License][license-image]][license-url]

NOTE: This app was generated with [Cookiecutter](https://github.com/audreyr/cookiecutter) along with [@clamytoe's](https://github.com/clamytoe) [toepack](https://github.com/clamytoe/toepack) project template.

The app is currently in its Initial stages and so far only scrapes [digminecraft.com](https://www.digminecraft.com/lists/enchantment_list_pc.php) for all available enchantments in vanilla Minecraft and generates either a *CSV* or *JSON* file. I still haven't decided which format I should stick with and will decide once I've played around with them both.

### Initial setup
```zsh
cd Projects
git clone https://github.com/clamytoe/mc_enchant.git
cd mc_enchant
```

#### Anaconda setup
If you are an Anaconda user, this command will get you up to speed with the base installation.
```zsh
conda env create
conda activate mc
```

#### Regular Python setup
If you are just using normal Python, this will get you ready, but I highly recommend that you do this in a virtual environment. There are many ways to do this, the simplest using *venv*.
```zsh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Final setup
```zsh
pip install -e .
```

## Usage
```zsh
mc_enchant
```

## Contributing
Contributions are very welcome. Tests can be run with with `pytest -v`, please ensure that all tests are passing and that you've checked your code with the following packages before submitting a pull request:
* black
* isort
* mypy

I am not adhering to them strictly, but try to clean up what's reasonable.

## License
Distributed under the terms of the [MIT](https://opensource.org/licenses/MIT) license, "mc_enchant" is free and open source software.

## Issues
If you encounter any problems, please [file an issue](https://github.com/clamytoe/toepack/issues) along with a detailed description.

## Changelog
* **v0.1.0** Initial commit.

[python-version]:https://img.shields.io/badge/python-3.7-brightgreen.svg
[latest-version]:https://img.shields.io/badge/version-0.1.0-blue.svg
[travis-image]:https://travis-ci.org/clamytoe/mc_enchant.svg?branch=master
[travis-url]:https://travis-ci.org/clamytoe/mc_enchant
[bch-image]:https://bettercodehub.com/edge/badge/clamytoe/mc_enchant?branch=master
[bch-url]:https://bettercodehub.com/
[issues-image]:https://img.shields.io/github/issues/clamytoe/mc_enchant.svg
[issues-url]:https://github.com/clamytoe/mc_enchant/issues
[fork-image]:https://img.shields.io/github/forks/clamytoe/mc_enchant.svg
[fork-url]:https://github.com/clamytoe/mc_enchant/network
[stars-image]:https://img.shields.io/github/stars/clamytoe/mc_enchant.svg
[stars-url]:https://github.com/clamytoe/mc_enchant/stargazers
[license-image]:https://img.shields.io/github/license/clamytoe/mc_enchant.svg
[license-url]:https://github.com/clamytoe/mc_enchant/blob/master/LICENSE
