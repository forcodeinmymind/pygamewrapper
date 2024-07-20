from setuptools import find_packages, setup


setup(
    name="pygwrapper",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "pygame"
    ],
    include_package_data=True,
    description="A simple pygame Wrapper package",
    author="Michael Naef",
    author_email="mister_naef@hotmail.com",
    url="",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
