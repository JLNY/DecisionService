# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 16:23:09 2016

@author: divakv
"""

import pandas as pd
import copy
import sys

class DecisionTree:
    
    def __init__(self, df):
        self.cols = list(df.columns)
        self.inputs = {x : list(df[x].unique()) for x in self.cols[:-1]}
        self.lendf = len(df)
        self.tree = {}
        self.buildTree(df)

    def buildTree(self, df):
        for i in range(len(df)):
            t = self.tree
            for j in range(len(self.cols) - 1) :
                try:
                    if j != len(self.cols) - 2:
                        t[df.iloc[i][self.cols[j]]][df.iloc[i][self.cols[j+1]]] = {}
                    else:
                        t[df.iloc[i][self.cols[j]]] = df.iloc[i][self.cols[j+1]]
                except KeyError:
                    if j != len(self.cols) - 2:
                        t[df.iloc[i][self.cols[j]]] = {df.iloc[i][self.cols[j+1]] : {}}
                    else:
                        t[df.iloc[i][self.cols[j]]] = df.iloc[i][self.cols[j+1]]
                t = t[df.iloc[i][self.cols[j]]]
            #print tree
        return self.tree
    
    
    def isBalanced(self):
        return reduce(lambda x, y: x*y, [len(x) for x in self.inputs.values()]) == self.lendf
    
    
    def validateInput(self, df):
        df1 = df.drop_duplicates()
        if len(df) != len(df1):
            i = raw_input('Duplicates found in Table, Fix? Y or N...')
            if str(i).lower() == 'y':
                df = df1
        return df
        
    def evalTree(self, inputs):
        t = copy.deepcopy(self.tree)
        for i in self.cols[:-1]:
            try:
                t = t[inputs[i]]
            except KeyError:
                print "Invalid Input"
                return None
        return t

if __name__ == "__main__":
    df = pd.read_excel('/home/vik1124/DecisionService/xor.xlsx',"Sheet1")
    #df = validateInput(df)
    #tree, ips = buildTree(df)
    tree = DecisionTree(df)
    
    print tree.tree, '\n', tree.inputs
    #print isBalanced(df)
    print tree.evalTree({'A' : 'Yes', 'B': 'No'})
