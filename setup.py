from setuptools import setup, find_packages

setup(
    name="space_weather",                       
    version="0.1",                           
    packages=find_packages(where="src"), # automatically finds python packages in src
    package_dir={"": "src"}, # root for package is in src folder (not the project folder)
)