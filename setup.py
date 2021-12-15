import os
import sys
from setuptools import setup, find_packages
import ctypes


if 'windll' not in dir(ctypes):
    print('Error: there is no ctypes.windll')
    print('Make sure that it\'s windows')
    sys.exit(1)


try:
    from pip._internal.cli.main import main as pip_main
except ImportError:
    ctypes.windll.user32.MessageBoxA(
        0,
        'Please, install pip before running winaudio installation'.encode(),
        'Critical Error'.encode(),
        0x10
    )
    sys.exit(1)


backup = (sys.argv, sys.exit)
requirements = ()
readme = ''
license_ = ''
version = '0.0.0'
to_remove = []


for i in range(len(sys.argv)):
    if sys.argv[i].lower().strip() == '-v' and len(sys.argv) > i + 1:
        version = sys.argv[i + 1].lower().strip()
        to_remove.append(sys.argv[i])
        to_remove.append(sys.argv[i + 1])
for i in tuple(to_remove):
    sys.argv.remove(i)


temp_file = open('LICENSE', 'r')
license_ = temp_file.read()
temp_file.close()


temp_file = open('README.MD', 'r')
readme = temp_file.read()
temp_file.close()


requirements = []


def fake_exit(*args, **kwargs) -> None:
    pass


def hook_sys(args: tuple) -> None:
    sys.argv = list(args)
    sys.exit = fake_exit


def unhook_sys() -> None:
    sys.argv = backup[0]
    sys.exit = backup[1]


def parse_args(cmd_string: str) -> list:
    result_str = ''
    work = str(cmd_string).strip()
    can_pass_space = False
    for i in range(len(work)):
        if work[i] == '\"':
            if not can_pass_space:
                can_pass_space = True
                result_str += '\n'
            else:
                can_pass_space = False
        elif work[i] == ' ':
            if not can_pass_space:
                result_str += '\n'
            else:
                result_str += ' '
        else:
            result_str += work[i]
    result = []
    for i in result_str.split('\n'):
        if not i == '':
            result.append(i)
    return result


def check_cmd(cmd: list) -> list:
    result = cmd
    return result


def run_pip_command(cmd) -> any:
    if not cmd:
        return True
    if type(cmd) == str:
        cmd = parse_args(cmd)
    cmd = tuple(check_cmd(list(cmd)))
    hook_sys(cmd)
    error = None
    try:
        pip_main()
    except Exception as e:
        error = e
    unhook_sys()
    return error if error else False


for i in license_.split('\n'):
    spaces = int(round(os.get_terminal_size()[0] / 2 - len(i) / 2))
    print(' ' * spaces + i)

print('\n\n', end='')

for i in requirements:
    if not i.strip().lower():
        continue
    print(f'Installing {i}...')
    run_pip_command(f'pip install "{i}"')


setup(
    name="winaudio",
    author="Pixelsuft",
    url="https://github.com/Pixelsuft/winaudio",
    project_urls={
        "Readme": "https://github.com/Pixelsuft/winaudio/blob/main/README.MD",
        "Example": "https://github.com/Pixelsuft/winaudio/blob/main/main.py",
        "Issue tracker": "https://github.com/Pixelsuft/winaudio/issues",
    },
    version=version,
    packages=find_packages(),
    license="MIT",
    description="Windows Audio API Bindings.",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.6",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    zip_safe=False,
    py_modules=["winaudio"],
    package_dir={'': '.'},
    keywords="winaudio"
)
