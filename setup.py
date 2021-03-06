from setuptools import setup

setup(
    name="Castle Adventure 3D",
    options = {
        "build_apps": {
            "gui_apps": {"Castle_Adventure_3D": "main.py"},
            "include_patterns": ["**/*"],
            "plugins": ["pandagl"],
            'platforms': [
                'manylinux1_x86_64',
                'macosx_10_6_x86_64',
                'win_amd64'
            ]
        }
    }
)