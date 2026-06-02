# Minecraft Enchantments Generator (*mc_enchant*)

> *Little utility to facilitate with generating the code needed to spawn enchanted objects in Minecraft*

![Python version][python-version]
![Latest version][latest-version]
[![GitHub issues][issues-image]][issues-url]
[![GitHub forks][fork-image]][fork-url]
[![GitHub Stars][stars-image]][stars-url]
[![License][license-image]][license-url]

NOTE: This app was generated with [Cookiecutter](https://github.com/audreyr/cookiecutter) along with [@clamytoe's](https://github.com/clamytoe) [toepack](https://github.com/clamytoe/toepack) project template.

**mc_enchant** is a tiny utility that makes creating enchanted Minecraft items painless.
Instead of digging through wikis or remembering which enchantments go on which items, you just pick what you want from a simple interactive menu.

The tool knows every valid enchantment, level, and compatibility rule in vanilla Minecraft, and instantly builds the correct `/give` command for you — no internet required.

## Initial setup

```zsh
cd Projects
git clone https://github.com/clamytoe/mc_enchant.git
cd mc_enchant
```

### Anaconda setup

If you are an Anaconda user, this command will get you up to speed with the base installation.
```zsh
conda env create -f environment.yml
conda activate mc
```

### Regular Python setup

If you are just using normal Python, this will get you ready, but I highly recommend that you do this in a virtual environment. There are many ways to do this, the simplest using *venv*.

```zsh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Final setup

```zsh
pip install -e .
```

## Usage

```zsh
mc_enchant
```

> **NOTE**: If your shell automatically `cd`'s you into the `mc_enchant` directory, you can run the app with `python -m mc_enchant` or run `unsetopt auto_cd` at the command prompt to prevent this from happening.

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

* **v0.6.1** Made project PEP-621 compliant.
* **v0.6.0** Refactored code because app.py was getting too big.
* **v0.5.0** Rebuilt whole test suite to better hit more edge cases.
* **v0.4.0** Updated to Python 3.13.3 and improved scraping source website.
* **v0.3.0** Added conflict resolution, data caching, ease of use features.
* **v0.2.0** Refactored project and completed the code.
* **v0.1.0** Initial commit.

[python-version]:https://img.shields.io/badge/python-3.13.3-brightgreen.svg
[latest-version]:https://img.shields.io/badge/version-0.6.1-blue.svg
[issues-image]:https://img.shields.io/github/issues/clamytoe/mc_enchant.svg
[issues-url]:https://github.com/clamytoe/mc_enchant/issues
[fork-image]:https://img.shields.io/github/forks/clamytoe/mc_enchant.svg
[fork-url]:https://github.com/clamytoe/mc_enchant/network
[stars-image]:https://img.shields.io/github/stars/clamytoe/mc_enchant.svg
[stars-url]:https://github.com/clamytoe/mc_enchant/stargazers
[license-image]:https://img.shields.io/github/license/clamytoe/mc_enchant.svg
[license-url]:https://github.com/clamytoe/mc_enchant/blob/master/LICENSE
