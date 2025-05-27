#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" General functions to be used in DesingSPHysics."""

import re
import locale
import sys
from os import path

def make_float(num):
    """Operate the content before to cast it to float"""
    return float(operate_val(str(num)))

def make_int(num):
    """Operate the content before to cast it to int"""
    return int(operate_val(str(num)))

def operate_val(val):
    """Operate the result of giving a set of sums of subtractions recursively"""
    # TODO: Develop the multiplication and division.
    # Consider parentheses?
    # Consider other math functions: cos, sen, tan, pow, etc.?
    val_str = str(val)
    if len(val_str) > 0:  # Check if there is at least 1 character to process
        is_sub = True if len(val_str.split(
            '-')) > 1 else False  # is a subtraction?
        is_sum = True if len(val_str.split(
            '+')) > 1 else False  # is an addition?
        # In case of a subtraction
        if is_sub:
            val_tmp = 0
            for i in range(len(val_str.split('-'))):
                val_unsigned = operate_val(val_str.split('-')[i])
                val_tmp += val_unsigned*(-1) if i > 0 else val_unsigned
            val_str = str(val_tmp)
        # In case of an addition
        elif is_sum:
            val_tmp = 0
            for i in range(len(val_str.split('+'))):
                val_unsigned = operate_val(val_str.split('+')[i])
                val_tmp += val_unsigned if i > 0 else val_unsigned
            val_str = str(val_tmp)
        # Remember to cast the return value for recursive calls
    return (float(val_str) if val_str != '' else 0)

def has_special_char(text: str) -> bool:
    """Checks if a given text includes special characters and spaces"""
    regex = re.compile('[ @!#$%^&*()<>?`\'|}{~]')      
    if regex.search(text) is None: 
        return False
    return True

def parse_int(number_str):
    """Convert a str number to int using the default locale"""
    # Set the locale to the user default locale
    locale.setlocale(locale.LC_ALL, '')
    # Convert the string to an integer using locale
    return locale.atoi(number_str)

def parse_ds_int(number_str):
    """Replaces the thousands separator for DS compatibility"""
    return int(number_str.replace(',',''))

def get_designsphysics_path() -> str:
    """ Returns the module base path. """
    return "{}/../".format(path.dirname(path.abspath(__file__)))

def get_mod_path() -> str:
    """ Returns the module base path. """
    return format(path.dirname(path.abspath(__file__)))

def get_os():
    """Returns an string with the opertative system (OS)"""
    platforms = {
        'linux' : 'Linux',
        'linux1' : 'Linux',
        'linux2' : 'Linux',
        'darwin' : 'OS X',
        'win32' : 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform
    return platforms[sys.platform]

def migrate_state(rename_map,default_attrs,state):
    # Migrate old attribute names
    for old_name, new_name in rename_map.items():
        if old_name in state and new_name not in state:
            state[new_name] = state.pop(old_name)
    
    # Apply defaults for missing attributes
    for attr, default_value in default_attrs.items():
        if attr not in state:
            state[attr] = default_value
    
    return state


def is_key(obj,key):
    if obj and key in obj:
        return True
    return False
