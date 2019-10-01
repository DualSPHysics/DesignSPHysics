#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

''' Standard output and error related tools. '''

from os import path

from mod.constants import VERBOSE, APP_NAME, DEBUGGING, DISK_DUMP_FILE_NAME


def log(message):
    ''' Prints a log in the default output.'''
    if VERBOSE:
        print("[" + APP_NAME + "]" + message)


def warning(message):
    ''' Prints a warning in the default output. '''
    if VERBOSE:
        print("[" + APP_NAME + "] " + "[WARNING]" + ": " + str(message))


def error(message):
    ''' Prints an error in the default output.'''
    if VERBOSE:
        print("[" + APP_NAME + "] " + "[ERROR]" + ": " + str(message))


def debug(message):
    ''' Prints a debug message in the default output'''
    if DEBUGGING and VERBOSE:
        print("[" + APP_NAME + "] " + "[<<<<DEBUG>>>>]" + ": " + str(message))


def dump_to_disk(text):
    ''' Dumps text content into a file on disk '''
    with open('/tmp/{}'.format(DISK_DUMP_FILE_NAME), 'w') as error_dump:
        error_dump.write(text)


def print_license():
    ''' Prints this software license. '''
    licpath = "{}{}".format(path.abspath(__file__).split("mod")[0], "LICENSE")
    if path.isfile(licpath) and VERBOSE:
        with open(licpath) as licfile:
            print(licfile.read())
    else:
        raise EnvironmentError("LICENSE file could not be found.")
