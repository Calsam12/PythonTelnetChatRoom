from cx_freeze import setup, Executable

setup(name ='PySrv',
      version ='0.1',
      description ='Simple Yet Effective Python Server',
      executables = [Executable("PyClient.py")])