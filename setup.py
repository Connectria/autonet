import os
import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(here+'/autonet_ng/__version__.py', 'r') as f:
    exec(f.read(), about)

install_requires = [
    'requests'
]

test_requires = install_requires + [
    'responses',
    'pytest',
    'pytest-responses'
]

setuptools.setup(
    name="autonet_ng",
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
    python_requires=">=3.7",
    install_requires=install_requires,
    test_requires=test_requires,
    test_suite='pytest',
    exclude_package_data={'': ['autonet_ng/*/tests/test_*.py']},
    entry_points={
        'autonet_ng.drivers': ['dummy = autonet_ng.drivers.dummy_driver.driver:DummyDriver']
    }
)
