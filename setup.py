import setuptools

setuptools.setup(
    name="gitcommit",
    version='0.1',
    url="https://github.com/newellp2019/gitcommit",
    author="Peter Newell",
    description="Jupyter extension to enable user push notebooks to a git repo",
    packages=setuptools.find_packages(),
    install_requires=[
        'psutil',
        'notebook',
        'gitpython'
    ],
    package_data={'githubcommit': ['static/*']},
)
