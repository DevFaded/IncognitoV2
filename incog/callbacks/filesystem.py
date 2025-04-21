from os import getcwd, remove, listdir, mkdir, rmdir
from os.path import join, abspath
from os.path import isfile as _isfile
from os.path import isdir as _isdir

from shutil import rmtree

WORKSPACE_DIRECTORY = join(getcwd(), "workspace")

FILENOTFOUND_ERROR = "FILENOTFOUND_ERROR"
PERMISSION_ERROR = "PERMISSION_ERROR"

def _path_no_escape(path: str):
    base_path = path.replace('/', "\\")
    full_path = abspath(join(WORKSPACE_DIRECTORY, *base_path.split("\\")))
    directory = abspath(full_path.split(base_path)[0])
    
    if directory != WORKSPACE_DIRECTORY:
        return WORKSPACE_DIRECTORY + full_path.split(directory)[0]

    return abspath(full_path)

def isfile(data):
    isafile: bool = False

    try:
        isafile = _isfile(_path_no_escape(data[0]))
    except:
        isafile = False

    return isafile

def readfile(data):
    path: str = _path_no_escape(data[0])
    
    try:
        with open(path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return FILENOTFOUND_ERROR
    except PermissionError:
        return PERMISSION_ERROR

def writefile(data):
    path: str = _path_no_escape(data[0])
    content: str = data[1]

    try:
        with open(path, 'w') as file:
            file.write(content)
            return True
        
    except FileNotFoundError:
        return FILENOTFOUND_ERROR
    except PermissionError:
        return PERMISSION_ERROR

def delfile(data):
    path: str = _path_no_escape(data[0])

    try:
        remove(path)
        return True
    except FileNotFoundError:
        return FILENOTFOUND_ERROR
    except PermissionError:
        return PERMISSION_ERROR
    
def listfiles(data):
    path: str = _path_no_escape(data[0])

    try:
        files: list[str] = []

        for i in listdir(path):
            root: str = path.split(WORKSPACE_DIRECTORY)[-1].removeprefix("\\")
            files.append(f"{root}\\{i}")

        return files
    
    except FileNotFoundError:
        return FILENOTFOUND_ERROR
    except PermissionError:
        return PERMISSION_ERROR
    
def isfolder(data):
    path: str = _path_no_escape(data[0])
    isafolder: bool = False

    try:
        isafolder = _isdir(path)
    except:
        isafolder = False

    return isafolder

def makefolder(data):
    path: str = _path_no_escape(data[0])

    try:
        mkdir(path)
    except:
        pass

    return True

def delfolder(data):
    path: str = _path_no_escape(data[0])

    try:
        rmtree(path)
        return True
    except FileNotFoundError:
        return FILENOTFOUND_ERROR
    except PermissionError:
        return PERMISSION_ERROR

__library__ = [
    isfile, readfile,
    writefile, delfile,
    listfiles, isfolder,
    makefolder, delfolder
]