# written by Parker
# inspired by https://medium.com/@nicholasRodgers/sidestepping-pythons-reload-function-without-restarting-maya-2448bab9476e

import os, sys, inspect

def unload_package_modules():
    '''Unloads all modules from the current package
    
    This is important when developing in maya as packages will not reload until
    a restart occurs or are forcefully reloaded with importlib. After using this script
    modules will be properly reimported.

    Use this at the start of your script
    '''
    # find package name
    package_file_path = os.path.sep.join(__file__.split(os.path.sep)[0:-2])
    print("unloading packages from:", package_file_path)

    # copy to avoid size changing and thread issue as advised in docs:
    # https://docs.python.org/3/library/sys.html
    for module_name, module in sys.modules.copy().items():

        # get path of the module
        # skip built in modules that don't have a .__file__ attribute
        module_file_path = getattr(module, "__file__", None)
        if not module_file_path:
            continue

        # if the module belongs to the current package then remove from sys.modules
        if module_file_path.startswith(package_file_path):
            # prevents removing the active script
            if module_file_path == __file__:
                continue

            print("unloading:", module_file_path)
            sys.modules.pop(module_name)
