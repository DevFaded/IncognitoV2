import os

def get_modules():
    modules = []

    directory: str = ".\\init\\modules"
    for dir_path, dir_names, file_names in os.walk(directory):
        for file_name in file_names:
            if file_name.endswith(".luau"):
                module_name = os.path.join(
                    dir_path.removeprefix(directory + "\\"), 
                    file_name.removesuffix(".luau")
                ) if dir_path != directory else file_name.removesuffix(".luau")

                module_path = f"{directory}\{module_name}.luau"
                modules.append([module_name.replace("\\", "/"), module_path])

    return modules