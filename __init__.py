from importlib import reload

from . import interface
reload(interface)
from .interface import start_interface
