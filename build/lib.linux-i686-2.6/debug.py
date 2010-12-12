#!/usr/bin/env python

"""debug.py
Module containing utility functions to work with date and times in python. Allows manipulating and converting
between mysql date and time values and other operations.
"""
__author__ = "Kashif Iftikhar"
__version__ = "0.1"

DEBUG = False

def print_debug(msg=""):
   if DEBUG:
      print msg