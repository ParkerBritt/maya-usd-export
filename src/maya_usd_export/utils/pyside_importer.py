import importlib
import sys

print("imported")

def import_all():
    # print("hello")
    # return importlib.import_module("math")

    pyside_versions = ["PySide6", "PySide2"]

    for version in pyside_versions:
        print("Trying pyside version:", version)
        try:
            PySide = importlib.import_module(version)
            sys.modules["PySide"] = PySide

            PySide.QtCore = importlib.import_module(f"{version}.QtCore")
            sys.modules["PySide.QtCore"] = PySide.QtCore

            PySide.QtWidgets = importlib.import_module(f"{version}.QtWidgets")
            sys.modules["PySide.QtWidgets"] =  PySide.QtWidgets

            shiboken = importlib.import_module(f"shiboken{version[-1]}")

            print("Successful import of", version)
            break
        except ModuleNotFoundError:
            continue
    else:
        raise ModuleNotFoundError("No PySide module found.")

    return (PySide, PySide.QtCore, PySide.QtWidgets, shiboken)

