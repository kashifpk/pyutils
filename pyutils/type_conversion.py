#!/usr/bin/env python

"""type_conversion.py
Module containing utility functions to convert between various data types.
"""
__author__ = "Kashif Iftikhar"
__version__ = "0.1"

def convert_type(source, target):
   """Converts the type of the target value/variable to the type of the source variable/value."""
   ret = target

   if type(1) == type(source): #int
      ret = int(target)
   elif type(1L) == type(source): #long
      ret = long(target)
   elif type(1.0) == type(source): #float
      ret = float(target)
   elif type('a') == type(source): #string
      ret = str(target)

   return(ret)