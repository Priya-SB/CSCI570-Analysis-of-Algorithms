# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 11:38:11 2021

@author: hp
"""

# -*- coding: utf-8 -*-
"""
Sequence Alignment Basic Version
"""

mn=[]
timebasic=[]
membasic=[]

from typing import List
import time
import tracemalloc

class InputOutputHandler:
    def __init__(self, inputFileName, outputFileName):
        self.inputFileName = inputFileName
        self.outputFileName = outputFileName
        
    def _readFile(self) -> List[str]:
        info = []
        with open(self.inputFileName, 'r') as file:
            for line in file.readlines():
                info.append(line.rstrip())
            file.close()
        return info
    
    def _stringGenerator(self, info: List[str]) -> str:

        str1 = ""
        str2 = ""
        lastStr = info[0]
        # print(lastStr)
        for line in info[1:]:
            if 48 <= ord(line[0]) <= 57:
                index = int(line)
                newStr = lastStr[:index+1] + lastStr + lastStr[index+1:]
                lastStr = newStr
                # print(lastStr)
            else:
                str1 = lastStr
                str2 = line
                lastStr = str2
                # print()
                # print(str2)
        str2 = lastStr
        return str1, str2
    
    def driver(self):
        info = self._readFile()
        return self._stringGenerator(info)
    
    def writeOutput(self, answer: List[str]):
        with open(self.outputFileName, 'w') as file:
            file.write(answer[0])
            for i in range(1, len(answer)):
                file.write("\n")
                file.write(answer[i])
        file.close()
        return
        
        
class SequenceAlignment_Basic:
    def __init__(self):
        self.hashMap = {'A' : 0, 'C': 1, 'G': 2, 'T': 3}
        self.alpha = [[0, 110, 48, 94],
                      [110, 0, 118, 48],
                      [48, 118, 0, 110],
                      [94, 48, 110, 0]]
        self.gapPenalty = 30
        
    def _getMismatchPenalty(self, str1: str, str2: str, i: int, j: int):
        return self.alpha[self.hashMap[str1[i]]][self.hashMap[str2[j]]]
    

    def _getAlignment(self, str1: str, str2: str) -> str:

        gapPenalty = self.gapPenalty
        
        m = len(str1)
        n = len(str2)
        arr = [[0 for j in range(n+1)] for i in range(m+1)]

        ## Initializing the table
        for i in range(m+1):
            arr[i][0] = i * gapPenalty
        for j in range(n+1):
            arr[0][j] = j * gapPenalty

        ## Finding the minimum penalty
        for i in range(1, m+1):
            for j in range(1, n+1):
                mismatchPenalty = self._getMismatchPenalty(str1, str2, i-1, j-1)
                arr[i][j] = min(arr[i-1][j-1] + mismatchPenalty, arr[i-1][j] + gapPenalty, arr[i][j-1] + gapPenalty)

        return arr
    
    def _tracePath(self, str1: str, str2: str, arr: List[int]) -> str:
        ## Backtracking to reconstruct the alignment
            m, n = len(str1), len(str2)
            gapPenalty = self.gapPenalty
            i, j = m, n
            x, y = "", ""

            while i > 0 and j > 0:
                mismatchPenalty = self._getMismatchPenalty(str1, str2, i-1, j-1)
                if arr[i - 1][j - 1] + mismatchPenalty == arr[i][j]:
                    x = str1[i-1] + x
                    y = str2[j-1] + y
                    i = i - 1
                    j = j - 1

                elif arr[i - 1][j] + gapPenalty == arr[i][j]:
                    x = str1[i-1] + x
                    y = '_' + y
                    i = i - 1

                elif arr[i][j - 1] + gapPenalty == arr[i][j]:
                    x = '_' + x
                    y = str2[j-1] + y
                    j = j - 1

            while i > 0:
                x = str1[i-1] + x
                y = '_' + y
                i = i - 1

            while j > 0:
                x = '_' + x
                y = str2[j-1] + y
                j = j - 1

            return x, y
        
    def driver(self, str1: str, str2: str):
    
        m, n = len(str1), len(str2)
        
        solution = []
        
        startTime = time.time()
        tracemalloc.start()
        
        arr = self._getAlignment(str1, str2)
        
        x_aligned, y_aligned = self._tracePath(str1, str2, arr)
        
        _, memoryUsage = tracemalloc.get_traced_memory()
        
        tracemalloc.stop()
        endTime = time.time()
        
        memoryUsage=memoryUsage / 10**3
        timeTaken = endTime - startTime
        
        line = x_aligned[:50] + " " + x_aligned[-50:]
        solution.append(line)
        line = y_aligned[:50] + " " + y_aligned[-50:]
        solution.append(line)
        line = str(round(arr[m][n], 1))
        solution.append(line)
        line = str(round(timeTaken, 3))
        solution.append(line)
        line = str(round(memoryUsage, 1))
        solution.append(line)
        
        mn.append(m+n)
        timebasic.append(timeTaken)
        membasic.append(memoryUsage)


        
        return solution

'''
iOHandler = InputOutputHandler("input35.txt", "output35.txt")
str1, str2 = iOHandler.driver()
seqAlignEff = SequenceAlignment_Basic()
answer = seqAlignEff.driver(str1, str2)
iOHandler.writeOutput(answer)
'''


for i in range(0,21):
  #print(i)
  iOHandler = InputOutputHandler("inputs/input"+str(i)+".txt", "outputs/output"+str(i)+".txt")
  str1, str2 = iOHandler.driver()
  seqAlignEff = SequenceAlignment_Basic()
  answer = seqAlignEff.driver(str1, str2)
  iOHandler.writeOutput(answer)
  
print("MN",mn)
print("Timebasic",timebasic)
print("Membasic",membasic)
