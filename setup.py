import setuptools

with open('requirements.txt') as f:
    reqs = f.read()

setuptools.setup(name='restock',
                 version="0.1.1",
                 description="restock: Simple tool to quickly obtain stock information",
                 author="jrcast",
                 author_email="jrcast@users.noreply.github.com",
                 packages=setuptools.find_packages(),
                 include_package_data=True,
                 url="https://github.com/jrcast/restock",
                 install_requires = (reqs.strip().split("\n"),)
                 )
