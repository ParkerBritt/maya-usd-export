<h1 align="center">Maya USD Export</h1>
<p align="center">
  <img src="https://img.shields.io/badge/Maya-37A5CC?style=for-the-badge&logo=autodeskmaya&logoColor=white">
  <img src="https://img.shields.io/badge/Qt-41CD52?style=for-the-badge&logo=Qt&logoColor=white">
  <a href="https://github.com/ParkerBritt?tab=repositories&q=&type=&language=c%2B%2B&sort="><img src="https://parkerbritt.com/badge?label=C%2B%2B&icon=cpp&color=00599C"></a>
</p>

<img align="right" height=400px src="screenshots/user_interface.png" alt="interface">
<br><br>
<p>
This repository provides a standalone Maya plugin for exporting USD (Universal Scene Description) files. It also includes a lightweight GUI for convenience and quick integration into tools and workflows.
  
While the functionality is similar to Autodesk's maya-usd plugin, this version is designed for modularity and ease of use. It does not require maya-usd, but remains compatible with it. This makes it simpler to modify and embed in other projects.

Future development will aim for feature parity with maya-usd, alongside new functionality such as reverse winding orders.
</p>
<br><br><br>



## Features
- Vertex Animations
- Copies XForm
- Select Individual Prims
- Set Individual Types
- Set Output Path

## Installation From Source
> Tested on Maya 2023.3 with maya-usd 0.20.0  
> Tested on Maya 2024.2 with maya-usd 0.25.0 & OpenUSD 0.22.11

### Prerequisites
- [OpenUSD](https://github.com/PixarAnimationStudios/OpenUSD)
    - For maya-usd compatability, check [releases](https://github.com/Autodesk/maya-usd/releases) to find out which version you need
- [Maya Devkit](https://aps.autodesk.com/developer/overview/maya)
- Ninja
- Cmake
- Qt5

### Build
```bash
git clone git@github.com:ParkerBritt/maya-usd-export.git
cd maya-usd-export

# point these to your actual paths
export USD_LOCATION="/path/to/usd/build"
export DEVKIT_LOCATION="/path/to/devkit"

./build.sh
```

### Install
```bash
./install.sh
```
## API
Access the API docs here:
https://parkerbritt.github.io/maya-usd-export

Or build the docs locally with:
```bash
cd maya-usd-export
doxygen
```
