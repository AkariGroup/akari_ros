import os
from glob import glob

from setuptools import setup

package_name = "m5_server"

setup(
    name=package_name,
    version="0.0.0",
    packages=[package_name],
    package_data={
        "": [
            "akari_msgs",
        ]
    },
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (
            os.path.join("share", package_name, "launch"),
            glob(os.path.join("launch", "*launch.[pxy][yma]*")),
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="akariros",
    maintainer_email="akariros@todo.todo",
    description="TODO: Package description",
    license="TODO: License declaration",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "m5_server = m5_server.m5_server:main",
        ],
    },
)
