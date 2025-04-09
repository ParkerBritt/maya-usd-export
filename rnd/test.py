import sys, os
import maya.standalone
import maya.cmds as cmds

try:
    maya.standalone.initialize(name='python')
except Exception as e:
    sys.stderr.write("Error initializing Maya standalone: {e}\n")
    sys.exit(1)

plugin_path = sys.argv[1]

try:
    if not cmds.pluginInfo(plugin_path, query=True, loaded=True):
        cmds.loadPlugin(plugin_path)
        print("Plugin loaded successfully!")
    else:
        print("Plugin is already loaded.")
except Exception as e:
    sys.stderr.write(f"Failed to load plugin: {e}\n")
    maya.standalone.uninitialize()
    sys.exit(1)

cube1 = cmds.polyCube()
cube2 = cmds.polyCube()
cmds.select([cube1[0]])

try:
    cmds.helloWorld()
    print("helloWorld command executed successfully!")
except Exception as e:
    sys.stderr.write("Error executing helloWorld: {}\n".format(e))
    maya.standalone.uninitialize()
    sys.exit(1)

maya.standalone.uninitialize()

