import random
import pygame

import config as co
import render as r

listLen=co.listLen

def swap(a,b):
	global ar
	temp=ar[a]
	ar[a]=ar[b]
	ar[b]=temp
	r.drawWrites(a,b)

def randInd():
	global listLen
	return random.randint(0,listLen-1)

def shuffle():
	global ar
	global listLen
	for c in range(listLen):
		i=randInd()
		if i!=c:
			swap(i,c)
		
def minishuffle(swaps):
	global ar
	global listLen
	for c in range(swaps):
		i=randInd()
		i2=randInd()
		if i!=i2:
			swap(i,i2)

def randSortSwaps(swaps):
	global ar
	global listLen
	for c in range(swaps):
		i=randInd()
		i2=randInd()
		if i<i2:
			r.drawComps(i,i2)
			if ar[i] > ar[i2]:
				swap(i,i2)
		elif i>i2:
			r.drawComps(i,i2)
			if ar[i] < ar[i2]:
				swap(i,i2)

def reverse():
	global ar
	global listLen
	for c in range(int(listLen/2)):
		swap(c,listLen-1-c)

def checkSorted():
	global ar
	global listLen
	for c in range(listLen-1):
		r.drawComps(c,c+1)
		if ar[c] > ar[c+1]:
			return False
	return True
	

	
def comb(gapFactor=1.3,stopGapFactor=5):
	global ar
	global listLen
	
	gapStart = listLen - 1
	gap = gapStart
	currentGapFactor = 1
	stopGap = max(1, gapStart / stopGapFactor)
	
	while gap >= stopGap:
		for c in range(listLen-gap):
			r.drawComps(c,c+gap)
			if ar[c] > ar[c+gap]:
				swap(c,c+gap)
		currentGapFactor *= gapFactor
		gap=round(gapStart/currentGapFactor)
	

