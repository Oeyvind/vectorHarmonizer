#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Various list operations.

@author: Øyvind Brandtsegg
@contact: obrandts@gmail.com
@license: GPL
"""

import copy
import re
getNum = re.compile('([1234567890.]+)')

def makeListFromString(aString):
    """
    Convert a string into a list of floats.

    @param aString: The input string.
    @param return: The string as a list of floats.
    """
    alist = getNum.findall(aString)
    index = 0
    for num in alist:
        try:
            alist[index] = float(num)
            if alist[index]  == int(alist[index]):
                alist[index] = int(num)
        except:
            print("makeListFromString can't make float from", num)
        index += 1
    return alist

def allPermutations(alist):
    """
    Return a list of lists, containing all possible reorderings of alist.

    Copied from http://snippets.dzone.com/posts/show/3556

    @param alist: The input list.
    @return: A list of lists with all permutations of the input list.
    """
    sz = len(alist)
    if sz <= 1:
        return [alist]
    return [p[:i]+[alist[0]]+p[i:] for i in list(range(sz)) for p in allPermutations(alist[1:])]

def eachToAllSecond(alist):
    """
    Combine the each element in a list with each of the other elements, returning a list of lists.

    Example:
    >>> eachToAllSecond([1,2,3,4])
    [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [2, 1],
    [3, 4], [3, 1], [3, 2], [4, 1], [4, 2], [4, 3]]

    @param alist: The input list.
    @return: A list of lists.
    """
    out = []
    for i in range(0, len(alist)):
        alistCopy = copy.copy(alist)
        new = firstToAllSecond(alistCopy)
        for member in new:
            out.append(member)
        #rotate
        first = alist.pop(0)
        alist.append(first)
    return out

def firstToAllSecond(alist):
    """
    Combine the first element in a list with each of the other elements, returning a list of lists.

    Example:
    >>> firstToAllSecond([1,2,3,4])
    [[1, 2], [1, 3], [1, 4]]

    @param alist: The input list.
    @return: A list of lists.
    """
    out = []
    clist = copy.copy(alist)
    first = clist.pop(0)
    while clist:
        second = clist.pop(0)
        out.append([first,second])
    return out

def appendToEach(item, alist):
    """
    Append item to each member of alist.

    Item may be a list and alist may be a list of lists

    Examples:
    >>> appendToEach(5, [1,2])
    [[1, 5], [2, 5]]
    >>> appendToEach([5,6], [[1,2],[3,4]])
    [[1, 2, 5, 6], [3, 4, 5, 6]]

    @param alist: The input list.
    @return: The list with item appended to each.
    """
    if type(item) is not list:
        item = [item]
    for member in alist:
        index = alist.index(member)
        if type(member) is not list:
            member = [member]
        member.extend(item)
        alist[index] = member
    return alist

def findAllCombinationsListOfLists(alist):
    """
    Returns a list of lists with all combinations possible by combining one member from each of two list.

    Lists may have different lengths.
    If there are more than two lists in alist, they are combined pairwise,
    then there must be an even number of sublists (e.g. 4 or 6 sublists.
    If there is only one list, the returned list will consist of each member of the input list each inside it's own list (e.g. in=[[1,2]], out=[[1],[2]]]

    Example:
    [[1,2], [3,4]] -> [[1,3], [1,4], [2,3], [2,4]]
    [[1,2], [3,4,5] -> [[1,3], [1,4], [1,5], [2,3], [2,4], [2,5]]
    >>>alist = [[1,2],[3,4],[5,6],[7,8]]
    >>> findAllCombinationsListOfLists(alist)
    [[1, 3], [1, 4], [2, 3], [2, 4], [5, 7], [5, 8], [6, 7], [6, 8]]

    @param alist: The input list.
    @return: The list of lists with all combinations of alist.
    """
    if len(alist) <=1:
        out = []
        try:
            for item in alist[0]:
                out.append([item])
        except:
            pass
        return out
    combo = []
    while len(alist) >= 2:
        sub1 = alist.pop(0)
        sub2 = alist.pop(0)
        for item in sub1:
            for item2 in sub2:
                combo.append([item, item2])
    return combo

def factorial(n, result=1):
    """
    Returns the factorial of n.

    @param n: The number to find factorial for.
    @return: The factorial of n.
    """
    while n > 1:
        result=n*result
        n = n - 1
    return result

def listRotate(alist, amount):
    """
    Rotates the members of a list, amount might be larger than the actual length of the list.

    @param alist: The list to rotate.
    @param amount: The rotation amount.
    @return: The rotated list.
    """
    if amount > 0:
        for i in range(0,amount):
            temp = alist.pop(0)
            alist.append(temp)
    if amount < 0:
        for i in range(0,abs(amount)):
            temp = alist.pop(-1)
            alist.insert(0, temp)
    return alist

def findAllMinimum(alist):
    """
    Return a list of indices to all values equal to the minimum value in a list.

    If only one value is the minimum of alist, this function would equal alist.index(min(alist)).

    @param alist: The list find minimums for.
    @return: The indices to the minimum values of the input list.
    """
    minimum = min(alist)
    minList = []
    index = 0
    for item in alist:
        if item == minimum:
            minList.append(index)
        index += 1
    return minList

def findAllMaximum(alist):
    """
    Return a list of indices to all values equal to the minimum value in a list.

    If only one value is the minimum of alist, this function would equal alist.index(min(alist))

    @param alist: The list find maximums for.
    @return: The indices to the maximum values of the input list.
    """
    maximum = max(alist)
    maxList = []
    index = 0
    for item in alist:
        if item == maximum:
            maxList.append(index)
        index += 1
    return maxList

def interpolate27List(alist, index):
    """
    List lookup with interpolation for floating point index.

    Interpolates into a list of [index,value] lists. The value returned is a linear interpolation between adjacent indices when index is fractional.
    The input list format is a list of lists with  [index, value], sort of like GEN27 in Csound.
    The input list is expected to be sorted in ascending index order, e.g. [[0,20], [1,10], [2,50]].
    An index of 0.5 will return a value of 15 using the list used as an example here,
    likewise, an index of 1.5 will return a value of 30.

    @param alist: The list to lookup values in.
    @param index: The index into the list, may be floating point.
    @return: The value at the interpolated index.
    """
    firstLower = None
    firstHigher = None
    for item in alist:
        if index >= item[0]:
            lowIndex,firstLower = item
        highIndex,firstHigher = item
        if index <= item[0]:
            break
    if (firstLower == None) or (firstHigher == None):
        print('interpolateList: bad index for list, check index and list')
        return
    difference = firstHigher - firstLower
    numIndices = (highIndex - lowIndex) + 1
    diffPerIndex = difference / numIndices
    indicesFromLowIndex = index - lowIndex
    return firstLower + (diffPerIndex*indicesFromLowIndex)
