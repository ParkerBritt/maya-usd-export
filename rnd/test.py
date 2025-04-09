import sys
import maya.standalone
import maya.cmds as cmds

try:
    maya.standalone.initialize(name='python')
except Exception as e:
    sys.stderr.write("Error initializing Maya standalone: {}\n".format(e))
    sys.exit(1)

plugin_path = "/home/parker/MyRepos/maya_usd_export/rnd/build/helloWorld.so"

try:
    if not cmds.pluginInfo(plugin_path, query=True, loaded=True):
        cmds.loadPlugin(plugin_path)
        print("Plugin loaded successfully!")
    else:
        print("Plugin is already loaded.")
except Exception as e:
    sys.stderr.write("Failed to load plugin: {}\n".format(e))
    maya.standalone.uninitialize()
    sys.exit(1)

try:
    cmds.helloWorld()
    print("helloWorld command executed successfully!")
except Exception as e:
    sys.stderr.write("Error executing helloWorld: {}\n".format(e))
    maya.standalone.uninitialize()
    sys.exit(1)

maya.standalone.uninitialize()

