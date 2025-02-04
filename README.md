<h1 align="center">Maya USD Export</h1>
<p align="center"}>
  <img src="https://img.shields.io/badge/Maya-37A5CC?style=for-the-badge&logo=autodeskmaya&logoColor=white">
  <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue">
  <img src="https://img.shields.io/badge/Qt-41CD52?style=for-the-badge&logo=Qt&logoColor=white">
</p>

This repo contains shelf tools for exporting **Maya** animations as **USD** files.

<div align="center">
    <img src="screenshots/user_interface.png" alt="interface">
</div>

## Features
- **Simplified inteface for exporting animated assets**
- **Capable of exporting static, animated, or cfx meshes**
- **Custom export location**
- **Custom frame range**

## Installation
### Requirements
- Autodesk Maya
- Maya USD Plugin
- Maya Alembic Plugin

### Step 1. Add to maya scripts directory
located at '''~/maya/scripts``` on linux
### Step 2. Run the code within mayas script editor or shelf tool
```python
import maya_usd_export
maya_usd_export.start_interface()
```

## Rig Requirements
**Following groups in heirarchy require specific attributes for CFX export:**
- USD_typeName:
  - grp_rig
  - geo
  - render
  - muscle
  - bone
- joints_grp
  - skin_joint

Currently grp_joints must exist for joints_grp attr to be found

**The current selection algorithm expects a rig with the following heirarcy naming:**
<div align="left">
  <img src="screenshots/rig_hierarchy.png" alt="Rig Hierarchy" style="border-radius: 50px;" width="400">
</div>

# Development
### Dependencies
**pytest**  
```sh
/usr/autodesk/maya/bin/mayapy -m pip install pytest
```
### Resources
[usd export command](https://github.com/Autodesk/maya-usd/tree/dev/lib/mayaUsd/commands)
