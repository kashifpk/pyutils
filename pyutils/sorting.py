#!/usr/bin/env python

"""sorting.py
Module containing utility functions to sort various data structures.
"""
__author__ = "Kashif Iftikhar"
__version__ = "0.1"

def dict_sort_by_key(dict, sort_order="A"):
   """Given a dictionary object, returns sorted list with each element sorted by the dictionary key.
      Returned list contains a list object for each dictionary key-value pair.
      sort_order ("A" | "D") specifies the sorting order for the dictionary.
   """
   ret = []
   keys = dict.keys()
   keys.sort()
   if 'D' == sort_order:
      keys.reverse()

   for key in keys:
      l = [key, dict[key]]
      ret.append(l)

   return ret

def dict_sort_by_val(dict, sort_order="A"):
   """Given a dictionary object, returns sorted list with each element sorted by the dictionary value.
      Returned list contains a list object for each dictionary key-value pair.
      sort_order ("A" | "D") specifies the sorting order for the dictionary.
   """
   ret = []
   dict_items = dict.items()

   while len(dict_items)>0:
      max_val = dict_items[0][1]
      max_idx = 0
      for i in range(0,len(dict_items)):
         if max_val < dict_items[i][1]:
            max_val = dict_items[i][1]
            max_idx = i

      ret.append(dict_items[max_idx])
      del dict_items[max_idx]

   if 'A' == sort_order:
      ret.reverse()

   return ret

