from setuptools import setup, find_packages


setup(
    name='alexa_browser_client',
    version='3.3.0',
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
        'avs-client>=1.2.0,<2.0.0',
        'command-lifecycle>=4.1.0,<5.0.0',
        'requests>=2.20.0,<3.0.0',
    ],
    extras_require={
        'test': [
            'pytest==3.2.3',
            'pytest-cov==2.5.1',
            'pytest-django==3.1.2',
            'pytest-sugar==0.9.0',
            'flake8==3.4.0',
            'codecov==2.0.9',
            'requests_mock==1.3.0',
            'django-environ==0.4.3',
            'pytest-asyncio==0.9.0',
            'twine>=1.11.0,<2.0.0',
            'wheel>=0.31.0,<1.0.0',
            'setuptools>=38.6.0,<39.0.0',
        ]
    },
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
