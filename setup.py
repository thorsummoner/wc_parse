import os
import setuptools

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setuptools.setup(
    name = 'worldcraftcommand',
    version = '0.2.00',
    author = 'Dylan Grafmyre',
    author_email = 'thorsummoner@live.com',
    description = ('WorldCraft Command file parser/scripter'),
    license = 'CC0 1.0 Universal',
    keywords = 'sourcesdk wc hammer',
    url = 'http://packages.python.org/worldcraftcommand',
    packages=setuptools.find_packages(),
    package_data = {
        # # If any package contains *.txt or *.rst files, include them:
        # '': ['*.txt', '*.rst'],
        # And include any *.wc files found in the 'worldcraftcommand' package, too:
        'worldcraftcommand': ['*.wc'],
    },
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Environment :: X11 Applications :: Gnome',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Games/Entertainment :: First Person Shooters',
        'Topic :: Multimedia :: Graphics :: 3D Rendering',
        'Topic :: Multimedia :: Graphics :: Editors',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
            'runmap = worldcraftcommand.compiler:main',
            'wc-util = worldcraftcommand.util:main',
        ],
        'gui_scripts': [
            'Runmap = worldcraftcommand.gnome:main',
        ]
    }
)
