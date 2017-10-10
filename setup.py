import pip.download
from pip.req import parse_requirements
from setuptools import setup, find_packages

try:
    long_description = open('README.rst').read()
except FileNotFoundError:
    long_description = open('README.md').read()


def get_requirements():
    requirements = parse_requirements(
        'requirements.txt',
        session=pip.download.PipSession()
    )
    return [str(r.req) for r in list(requirements)]


setup(
    name='alexa_browser_client',
    version='0.8.0',
    url='https://github.com/richtier/alexa-browser-client',
    license='MIT',
    author='Richard Tier',
    description='Alexa client in your browser. Django app.',
    packages=find_packages(exclude=["tests.*", "tests"]),
    long_description=long_description,
    include_package_data=True,
    install_requires=get_requirements(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
