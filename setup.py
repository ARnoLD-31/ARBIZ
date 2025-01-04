from setuptools import setup, find_packages

setup(
    name="arbiz",
    version="1.5.1",
    author="ARnoLD",
    author_email="pavelmilosh31@gmail.com",
    description="ARBIZ bot package",
    license="MIT",
    long_description=open("README.MD", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ARnoLD-31/ARBIZ",
    include_package_data=True,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    keywords="ARBIZ",
    python_requires=">=3.6",
    install_requires=[
        requirement.strip()
        for requirement in open(
            "requirements.txt", encoding="utf-8"
        ).readlines()
    ],
    entry_points={
        "console_scripts": [
            "arbiz=arbiz.__main__:main",
        ],
    },
)
