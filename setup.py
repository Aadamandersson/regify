from setuptools import setup, find_packages

setup(
   name='regify',
   version='0.1.19',
   description="Modernized syntax for regular expressions.",
   license="MIT",
   author="Adam Andersson & Ludwig Hansson",
   url='https://regify.github.io',
   packages=find_packages('src'),
   package_dir={"": "src"}
)