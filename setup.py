import os
import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(here+'/autonet/__version__.py', 'r') as f:
    exec(f.read(), about)

install_requires = [
    'conf-engine>=1.0',
    'Flask>=2.1.2',
    'passlib>=1.7.0',
    'pymysql>=1.0.2',
    'PyYAML~=6.0',
    'requests>=2.0.12',
    'requests-cache>=0.9.4',
    'SQLAlchemy>=1.4.36',
    'macaddress>=1.2.0'
]

test_requires = install_requires + [
    'responses',
    'pytest',
    'pytest-responses'
]

setuptools.setup(
    name="autonet-api",
    version=about['__version__'],
    author="Ken Vondersaar",
    author_email="kvondersaar@connectria.com",
    description="Network device configuration abstraction API",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/Connectria/autonet_ng",
    project_urls={
        "Bug Tracker": "https://github.com/Connectria/autonet_ng",
        "Documentation": "https://connectria.github.io/autonet_ng",
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Development Status :: 4 - Beta"
        "License :: Other/Proprietary License"
        "Operating System :: OS Independent",
    ],
    package_dir={"": "./"},
    packages=setuptools.find_packages(where='./'),
    python_requires=">=3.9",
    install_requires=install_requires,
    test_requires=test_requires,
    test_suite='pytest',
    exclude_package_data={'': ['autonet/*/tests/test_*.py']},
    entry_points={
        'console_scripts': [
            'autonet-server = autonet.core.app:run_wsgi_app',
            'autonet-createadmin = autonet.commands.createadmin:create_admin'
                            ],
        'autonet.drivers': [
            'dummy = autonet.drivers.device.dummy_driver.driver:DummyDriver'
        ],
        'autonet.backends': [
            'config = autonet.drivers.backend.deviceconf:DeviceConf',
            'yamlfile = autonet.drivers.backend.yamlfile.yamlfile:YAMLFile',
            'netbox = autonet.drivers.backend.netbox.netbox:NetBox'
        ]
    }
)
