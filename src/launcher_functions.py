import os
import platform
system = platform.system()

# takes: app, file
# app - the app to close
# file - the file to launch (not including .py)

def launch_app_reg(app, file):
    match system:
        case 'Windows':
            os.system(f'python {file}')
        case 'Linux':
            os.system(f'python3 {file}')
        case _:
            print("Unsupported operating system") #!ERROR LOG NEEDED