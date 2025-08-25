<h1 align="center">USD Export for Maya</h1>
<p align="center">
  <a href="https://www.autodesk.com/"><img src="https://cards.parkerbritt.com/badge?label=Maya&icon=autodeskmaya&color=37A5CC"></a>
  <a href="https://www.qt.io/"><img src="https://cards.parkerbritt.com/badge?label=Qt&icon=qt&color=41CD52"></a>
  <a href="https://github.com/ParkerBritt?tab=repositories&q=&type=&language=c%2B%2B&sort="><img src="https://cards.parkerbritt.com/badge?label=C%2B%2B&icon=cplusplus&color=00599C"></a>
</p>
<video src="https://github.com/user-attachments/assets/e336f5bf-d99c-45f9-a92d-c1b990ed5071"></video>

<p>
This repository provides a standalone Maya plugin for exporting USD (Universal Scene Description) files. It also includes a lightweight GUI for convenience and quick integration into tools and workflows.
While the functionality is similar to Autodesk's maya-usd plugin, this version is designed for modularity and ease of use. It does not require maya-usd, but remains compatible with it. This makes it simpler to modify and embed in other projects.
Future development will aim for feature parity with maya-usd, alongside new functionality such as reverse winding orders.
</p>

## Features
- Vertex Animations
- Copies XForms
- Copies UVs
- Squash shapes
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


