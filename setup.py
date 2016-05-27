from pip.req import parse_requirements
from setuptools import find_packages
from setuptools import setup
from setuptools.command.install import install as _install


install_requirements = parse_requirements('requirements.txt', session=False)
requirements = [str(ir.req) for ir in install_requirements]


class install(_install):

    def run(self):
        _install.run(self)


setup(
    name='notify',
    version='0.0.0',
    author=u'Alexander Brandstedt',
    author_email='alexbrsub@gmail.com',
    description='Some description',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    cmdclass={'install': install},
    )
