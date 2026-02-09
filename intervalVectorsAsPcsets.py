#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Create a dictionary of pcsets from interval vectors.

@author: Øyvind Brandtsegg
@contact: obrandts@gmail.com
@requires: The file 'VectPcs_3to9.txt' containing interval vector pc sets
@license: GPL
"""

# file read operations
import re


class PcsetFromIntervalVector:
    """
    This module create a dictionary of pcsets from interval vectors.

    It reads a file of interval vectors and their pcsets, and put the contents into a dictionary,
    using the interval vector as key, and a list of pcsets as value.
    """

    def __init__(self):
        """
        Class constructor.

        @param self: The object pointer.
        """
        # input textfile
        self.vectorfile = open('VectPcs_3to9.txt', 'r')
        # pattern for finding all integers in string
        self.getint = re.compile(r'(?P<int>\d*)')
        # dictionary for storing interval vectors as keys, pcsets as values
        self.vectordict = {}

        # find the interval vectors and pc sets stored for each line in the file
        for line in self.vectorfile:
            vectors = line[0:20]    # split the line into vector
            pcsets = line[21:-1]    # and pcsets
            pcset_temp = self.getint.findall(pcsets)
            vector_temp = self.getint.findall(vectors)

            # string formatting operation to clean up vector (only include numbers)
            intervalvector = []
            for item in vector_temp:
                try:
                    num = int(item)
                    intervalvector.append(num)
                except:
                    pass
            # string formatting operation to clean up pcset (only include numbers)
            pcset = []
            for num in pcset_temp:
                try:
                    num = int(num)
                    pcset.append(num)
                except:
                    pass

            # store vectors and pcsets in dicts, using vector as key
            self.vectordict.setdefault(tuple(intervalvector), []).append(pcset)

    def getVectors(self):
        """
        Get a list of all valid interval vectors.

        @param self: The object pointer.
        @return: The list of all valid interval vectors.
        """
        return self.vectordict.keys()

    def getPcsets(self, vector):
        """
        Get Pcsets.

        @param self: The object pointer.
        @param vector: The vector must be specified as a tuple, for example (1,0,0,1,1,0)
        @return: The pcsets corresponding to the interval vector.
        """
        try:
            return self.vectordict[vector]
        except:
            return None




def test():
    '''
    a basic test:
    >>> pcsetFromIntervalVector = PcsetFromIntervalVector()
    >>> pcsetFromIntervalVector.getPcsets((1,0,0,1,1,0))
    >>> [[0, 1, 5], [0, 1, 8], [0, 4, 5], [0, 4, 11], [0, 7, 8], [0, 7, 11]]
    '''
    pcsetFromIntervalVector = PcsetFromIntervalVector()
    print(pcsetFromIntervalVector.getPcsets((1,0,0,1,1,0)))

if __name__ == '__main__':
    test()
    '''
    pc = PcsetFromIntervalVector()
    f = open('vector_pc_items.txt', 'w')
    for vector in pc.vectordict.keys():
        f.write(str(vector) + '\t' + str(pc.vectordict[vector]) + '\n')
    f.close()
    '''
