#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 17:02:03 2019

@author: Luca Michael Reeb
"""

class _ParallelOp:
    
    ID = 0
    
    def getID():
        _ParallelOp.ID += 1
        return _ParallelOp.ID
    
    def __init__(self, split_op, pipes, merge_op):
        self.id = _ParallelOp.getID()
        self.split_op = split_op
        self.pipes = pipes
        self.merge_op = merge_op
        
        
    def __call__(self, x):
        splitted = self.split_op(x)
        res = [self.pipes[i](x) for i, x in enumerate(splitted)]
        return self.merge_op(*res)
        
    def __eq__(self, other):
        if type(other) == type(self):
            return self.id == other.id
        return False
    
    def __hash__(self):
        return hash(self.id)
    
    def __str__(self):
        return 'ParallelOp({})'.format(self.id)
    
    def __repr__(self):
        return str(self)

class Pipeline:
    
    def __init__(self):
        self.ops = []
        self.splits = {}
        
    def add(self, op, idx=-1):
        '''Add an operation to the pipeline.
        
        Args: 
            op: callable
                The operation to append to the pipline
            idx: int
                The position to insert the operation into.
                
        Returns:
            the index of the inserted operation
        '''
        if idx == -1:
            self.ops.append(op)
            return len(self.ops)
        else:
            self.ops.insert(idx, op)
            return idx
    
    def split(self, split_op, pipes, merge_op, idx=-1):
        '''Add (virtually) parrallel operations to the pipeline.
        
        Args:
            split_op: callable
                the operation splitting providing the data to be processed in parallel
                based on the incoming data.
            pipes: iterable of fwlib.Pipeline
                The pipelines which to apply to the outputs of the splitting operation.
                Must have the same length as the output of the splitting_op as elements.
                The order of `pipes` is assumed to be corresponding to splitting_op's output
                order.
            merge_op: callable
                Operation merging the results of parallel operations into a single
                output. Must have the same parameters as `len(pipes)`.
            idx: int
                the pipeline index to insert the parallel operations into.
        '''
        pop = _ParallelOp(split_op, pipes, merge_op)
        self.add(pop, idx)
            
    def __getitem__(self, key):
        return self.ops[key]
    
    def __setitem__(self, key, value):
        self.ops[key] = value
        
    def __delitem__(self, key):
        del self.ops[key]
        
    def __call__(self, input):
        for op in self.ops:
            input = op(input)
        return input
        
    