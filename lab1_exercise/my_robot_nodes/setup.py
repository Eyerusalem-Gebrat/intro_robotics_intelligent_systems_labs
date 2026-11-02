
from setuptools import find_packages, setup

package_name = 'my_robot_nodes'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/square.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Eyerusalem Gebrat',
    maintainer_email='eyerusalem.gebrat@gmail.com',
    description='Robot control nodes for Lab 1',
    license='MIT',
    entry_points={
        'console_scripts': [
            'turn_away = my_robot_nodes.turn_away:main',
            'rotate_server = my_robot_nodes.rotate_server:main',
            'square_driver = my_robot_nodes.square_driver:main',
        ],
    },
)
