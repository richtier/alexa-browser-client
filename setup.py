from setuptools import setup, find_packages


setup(
    name='alexa_browser_client',
    version='2.1.0',
    url='https://github.com/richtier/alexa-browser-client',
    license='MIT',
    author='Richard Tier',
    description='Alexa client in your browser. Django app.',
    packages=find_packages(exclude=["tests.*", "tests"]),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=[
        'channels>=2.1.4,<3.0.0',
        'channels_redis>=2.1.1,<3.0.0',
        'Django>=2.1.0,<3.0.0',
        'avs-client>=0.7.1,<1.0.0',
        'command-lifecycle>=2.0.0,<3.0.0',
        'requests>=2.19.1,<3.0.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',
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
