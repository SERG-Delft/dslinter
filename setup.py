"""Setup script."""
from setuptools import find_packages, setup

# Get the long description from the README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="dslinter",
    version="1.0.2",
    description="Pylint plugin for linting data science and machine learning code, focussed on the libraries pandas and scikit-learn.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hynn01/dslinter",
    author="Mark Haakman, Haiyin Zhang, Daoyao Wang, Chadha Degachi",
    packages=find_packages(),
    package_data={"": ["*.pickle"]},
    python_requires="~=3.5",
    install_requires=["pylint~=2.0", "astroid~=2.4", "mypy", "data-science-types", "pyspark-stubs"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
