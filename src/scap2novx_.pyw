"""Scapple to noveltree converter 

Version @release
Requires Python 3.6+
Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/noveltree_scapple
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import argparse
from pathlib import Path
from novxlib.ui.ui import Ui
from novxlib.ui.ui_tk import UiTk
from novxlib.config.configuration import Configuration
from scap2novxlib.scap_converter import ScapConverter

SUFFIX = ''
APPNAME = 'scap2novx'
GREEN = '0.0 0.5 0.0'
BLUE = '0.0 0.0 1.0'
RED = '1.0 0.0 0.0'
PURPLE = '0.5 0.0 0.5'
SETTINGS = dict(
    location_color=BLUE,
    item_color=GREEN,
    major_chara_color=RED,
    minor_chara_color=PURPLE,
)
OPTIONS = dict(
    export_sections=True,
    export_characters=True,
    export_locations=True,
    export_items=True,
)


def run(sourcePath, silentMode=True, installDir='.'):
    if silentMode:
        ui = Ui('')
    else:
        ui = UiTk('Scapple to noveltree converter @release')

    #--- Try to get persistent configuration data
    sourceDir = os.path.dirname(sourcePath)
    if not sourceDir:
        sourceDir = '.'
    iniFileName = f'{APPNAME}.ini'
    iniFiles = [f'{installDir}/{iniFileName}', f'{sourceDir}/{iniFileName}']
    configuration = Configuration(SETTINGS, OPTIONS)
    for iniFile in iniFiles:
        configuration.read(iniFile)
    kwargs = {'suffix': SUFFIX}
    kwargs.update(configuration.settings)
    kwargs.update(configuration.options)
    converter = ScapConverter()
    converter.ui = ui
    converter.run(sourcePath, **kwargs)
    ui.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Scapple to noveltree converter',
        epilog='')
    parser.add_argument('sourcePath',
                        metavar='Sourcefile',
                        help='The path of the Scapple file.')
    parser.add_argument('--silent',
                        action="store_true",
                        help='suppress error messages and the request to confirm overwriting')
    args = parser.parse_args()
    try:
        homeDir = str(Path.home()).replace('\\', '/')
        installDir = f'{homeDir}/.noveltree/{APPNAME}/config'
    except:
        installDir = '.'
    run(args.sourcePath, args.silent, installDir)
