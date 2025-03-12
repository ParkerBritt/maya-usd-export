# written by Parker
# inspired by https://medium.com/@nicholasRodgers/sidestepping-pythons-reload-function-without-restarting-maya-2448bab9476e

import os, sys, inspect

def unload_package_modules(package_name: str = None):
    '''Unloads all modules from the current package
    
    This is important when developing in maya as packages will not reload until
    a restart occurs or are forcefully reloaded with importlib. After using this script
    modules will be properly reimported.

    Use this at the start of your script
    '''

    # get package name
    if package_name is None:
        package_name = __file__.split(os.path.sep)[-3]
    print("unloading modules from package:", package_name)

    # copy to avoid size changing and thread issue as advised in docs:
    # https://docs.python.org/3/library/sys.html
    for module_name, module in sys.modules.copy().items():
        # if the module belongs to the current package then remove from sys.modules
        if module_name.startswith("maya_usd_export"):
            # get path of the module
            module_file_path = getattr(module, "__file__", None)

            # prevents removing the active script
            if module_file_path == __file__:
                continue

            print("unloading:", module_name)
            del sys.modules[module_name]
