#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
""" General funtions to be used in DesingSPHysics."""


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
            '-')) > 1 else False  # is a substraction?
        is_sum = True if len(val_str.split(
            '+')) > 1 else False  # is an addition?
        # In case of a substraction
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
