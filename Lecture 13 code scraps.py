#!/usr/bin/env python
# encoding: utf-8
"""
lecture code scraps.py

Created by Scott Brenner on 2011-02-25.
Copyright (c) 2011 Scott Brenner. All rights reserved.
"""

import sys
import os
numCalls = 0
num2Calls = 0

current_combo = []
best_combo = []

def tryMaxVal():
    w = [1,5,3,2,4]
    v = [15,10,9,5,5]
    
    w = [1,2,3,4,1,2,3,4]
    v = [15,10,9,5,15,10,9,5]
    #w = [7,4,3,4,5,6,7,8,8,9,9,5,1,1,9,15,15,10,12,5,9,5,19,15,9,1,5,3,4,1,5,3,4,9,5,9,5,9,5,15,10,15,10,15,10,5,15,10]
    #v = [9,1,5,3,4,1,5,3,4,9,5,9,5,9,5,15,10,15,10,15,10,5,15,10,7,4,3,4,5,6,7,8,8,9,9,5,1,1,9,15,15,10,12,5,9,5,19,15]
    
    res = maxVal(w,v,len(v)-1,7)
    print 'max val =', res, 'number of calls = ',numCalls


def maxVal0(w, v, i, aW):
    """
    Returns a schedule optimized by value that is equal to less that the maxload (aW).  It takes two vectors describing a course schedule--one describes the work load, the other describes the value of each course.   i is the length of the course catalog/vectors.
    
    SCOTT: CONSIDER ADDING a procedure that reduces the length catalog by elmiinating class with workloads that exceed max work.  Also consider simplifying this function to just take the catalog and aW. That way the prep work can be 'hidden' from the user.
    """
    
    m = {}
    value, schedule = fastMaxVal(w, v, i, aW, m)
    return value, schedule

def fastMaxVal(w, v, i, aW, m):
    """
    Returns a schedule optimized by value that is equal to less that the maxload (aW).  It takes two vectors describing a course schedule--one describes the work load, the other describes the value of each course.   i is the index of the currect class being evaluated.
    The functions uses a decision tree to evaluate build every option and then the optimal option is chosen.
    
    w: a list of workloads for each available class.
    v: a list of values for each available class
    i: index; length of vectors
    
    *** This function returns the highes value but how do you find the i's that were choosen.  SUGGESTION:  as each itme is taken along the take branch add the i (index) to a dictionary called best choice. 
    
    """
    #   These are just here for counting the number of recursions.
    global num2Calls
    num2Calls += 1
    pd = False
    if pd: print "i,aW", i,aW, '\tvalue:',v[i]
    #   Check if this index, remaining workload pair has been evaluated.
    #   If it has, return the previously calculated result(~vi).
    try: return m[(i, aW)]    #   use the try: except scheme because attempting to access a key that doesn't exist returns an error
    except KeyError:
        
        ################ Base case.  
        if i == 0:
            #print "in base case"
            if w[i] <= aW:          # If there is a enough aW for the w[0] then
                #print "take base" 
                m[(i, aW)] = v[i], [0]   # create dictionary entry for 0th, aw with value of 0th itme
                return v[i], [0]         # return value of 0th item and i itself.
            else:
                #print "don't take base"
                m[(i, aW)] = 0,[]      # not enough room in aW for 0th item, return 0
                return 0, []        # return 0 and an empty string.
       
        ################ Recurse with the next item closer to 0th.
        ################ This is basically builing the results for all the don't-take branches.
        #print "not in base.  Now at i =", i
        without_i, i_list = fastMaxVal(w, v, i-1, aW, m)   #   Set without_i to the value returned by fastMaxVal for the next i.
        #print "back up from base."
        #print "without_i, i_list:\t", without_i, i_list
        if w[i] > aW:               # If there isnt a enough w[i] then
            #print "not enough room aW for w[i]", w[i] > aW
            m[(i, aW)] = without_i, i_list      # This is a dead end with this aW.  Make a dictionary entry.
            return without_i, i_list  # Return value of of path to this point and list of i's to this point.
            
        else:       # There is room in aW for w[i].
            #   Recursibely build the do-take branches
            #   Set with_i value to value of just selected item and add the value of the downstream branch/decisions.
            #print "enough room aW for w[i].  w[i], aW, i:\t", w[i], aW, i
            with_i, maybe_i = fastMaxVal(w, v, i-1, aW - w[i], m)
            with_i += v[i]
        #res = max(with_i, without_i)    # Decide whether choosing the item produces a higher value than not choosing the item.
        if with_i > without_i:
            res = with_i
            i_list = [i] + maybe_i
        else:
            res = without_i
        ########  Write some code here to select the best path based on highest value.
        m[(i, aW)] = res, i_list           # Add a dictionary key for the better decision.
        return res, i_list            # Return the higher value, and the selected i's.




def tryMaxVals(n):
    w = [ 1, 5,3,2,4]   #  with aW of 7 optimal is [0,3,4] with value of 29
    v = [15,10,9,5,5]
    w = [2,1,2,3,4,1,2,3,4]   #  with aW of 7 optimal is [] with value of 50
    v = [8,15,10,9,5,15,10,9,5]
    w = [7,4,3,4,5,6,7,8,8,9,9,5,1,1,9,15,15,10,12,5,9,5,19,15,9,1,5,3,4,1,5,3,4,9,5,9,5,9,5,15,10,15,10,15,10,5,15,10]
    v = [9,1,5,3,4,1,5,3,4,9,5,9,5,9,5,15,10,15,10,15,10,5,15,10,7,4,3,4,5,6,7,8,8,9,9,5,1,1,9,15,15,10,12,5,9,5,19,15]
    
    # res = maxVal(w,v,len(v)-1,n)
    # print 'max val =', res, 'number of calls = ',numCalls
    
    res, best_schedule = maxVal0(w,v,len(v)-1,n)
    best_schedule.sort()
    print best_schedule
    print 'max val =', res, 'number of calls = ',num2Calls

tryMaxVals(7)