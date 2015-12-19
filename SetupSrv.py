from cx_freeze import setup, Executable

setup(name ='PySrv',
      version ='0.2',
      description ='Simple Yet Effective Python Server',
      executables = [Executable("PySrvV2.py")])