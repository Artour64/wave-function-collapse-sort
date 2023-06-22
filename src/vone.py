import random
import pygame

import config as co
import render as r

import sort as s

listLen=co.listLen

dataInd = list(range(listLen))

data=list(range(listLen))


def sort(compPass = False, partSort = False):
	global data, dataInd, ar, listLen
	init_data()
	isSorted = False
	passes = 0
	while not isSorted:
		passes += 1
		
		best_comp(partSort)
		if compPass:
			comp_pass(partSort)
		
		propagate()
		
		do_swaps()
		
		checkDone()
		isSorted = True
		for c in data:
			if not c.done:
				isSorted = False
				break
		
	print("passes: "+str(passes))

class Data :
	def __init__(self, val ):
		global listLen
		self.val = val
		self.iMin = 0
		self.iMax = listLen - 1
		self.above = set()
		self.below = set()
		self.equal = set()#not fully implemented
		self.done = False
	
	def range(self):
		return self.iMax - self.iMin
	
	def related(self,i):
		if i in self.above:
			return True
		if i in self.below:
			return True
		if i in self.equal:
			return True
		return False
	
	def relatives(self):
		return len(self.above) + len(self.below)
	
	def addAbove(self,i):
		global data
		if i not in self.above:
			self.above.add(i)
			if self.iMax >= data[i].iMax:
				self.iMax = data[i].iMax - 1
			if self.iMin >= data[i].iMin:
				data[i].iMin = self.iMin + 1
	
	def addBelow(self,i):
		global data
		if i not in self.below:
			self.below.add(i)
			if self.iMin <= data[i].iMin:
				self.iMin = data[i].iMin + 1
			if self.iMax <= data[i].iMax:
				data[i].iMax = self.iMax - 1
	
	def calc(self):
		self.calcAbove()
		self.calcBelow()
	
	#has no base condition that always works, don't use until fixed
	def recursiveCalc(self):
		global data
		if not self.done:
			self.calc()
			for c in self.above:
				data[c].recursiveCalc()
			
			for c in self.below:
				data[c].recursiveCalc()
	
	def calcAbove(self):
		global data
		if self.iMax >= listLen - len(self.above):
			self.iMax = listLen - len(self.above) - 1
		changed = True
		while changed:
			changed = False
			for c in self.above:
				if self.iMax >= data[c].iMax:
					self.iMax = data[c].iMax - 1
				size = len(self.above)
				self.above.update(data[c].above)
				if size < len(self.above):
					changed = True
					break
	
	def calcBelow(self):
		global data, listLen
		if self.iMin <= len(self.below):
			self.iMin = len(self.below)
		changed = True
		while changed:
			changed = False
			for c in self.below:
				if self.iMin <= data[c].iMin:
					self.iMin = data[c].iMin + 1
				size = len(self.below)
				self.below.update(data[c].below)
				if size < len(self.below):
					changed = True
					break
	


def get_data(i):
	global data, dataInd
	return data[dataInd[i]]

def init_data():
	global data, dataInd, ar
	for c in range(listLen):
		data[c] = Data(ar[c]);

def comp(a,b,partSort = False):
	global data, dataInd, ar
	r.drawComps(a,b)
	if ar[a] == ar[b]:
		print("eq")#probably a bug
		get_data(a).equal.add(dataInd[b])
		get_data(a).equal.add(dataInd[a])
		return
	elif ar[a] > ar[b]:
		a,b = b,a
	#a < b
	get_data(a).addAbove(dataInd[b])
	get_data(b).addBelow(dataInd[a])
	
	if partSort:
		if a > b:
			if not get_data(a).done:
				if not get_data(b).done:
					swap(a,b)

def comp_pass(partSort):
	global data, dataInd, ar, listLen
	for c in range(listLen):
		i = s.randInd()
		tries = 0
		triesMax = listLen
		d = get_data(c)
		while (i == c or get_data(i).range() == 0 or d.related(dataInd[i])) and tries < triesMax:
			i = s.randInd()
			tries += 1
		if tries >= triesMax:
			l = []
			for i in range(listLen):
				if i != c and get_data(i).range() != 0 and not d.related(dataInd[i]):
					l.append(i)
			if len(l) > 0:
				i = random.choice(l)
			else:
				i = -1
		if i != -1:
			comp(c,i,partSort)
				

def best_comp(partSort = False):
	global data, dataInd, ar, listLen
	l = []
	r0 = listLen
	for c in range(listLen):
		r2 = get_data(c).range()
		if r0 == r2:
			l.append(c)
		elif r0 > r2 and r2 > 0:
			l = [c]
			r0 = r2
	
	if len(l) > 0:
		i1 = random.randint(0,len(l) - 1)
		i1 = l[i1]
		if len(l) > 1:
			i2 = random.randint(0,len(l) - 1)
			i2 = l[i2]
			while i1 == i2:
				i2 = random.randint(0,len(l) - 1)
				i2 = l[i2]
		else:
			r3 = r0
			l = []
			r0 = listLen
			for c in range(listLen):
				r2 = get_data(c).range()
				if r0 == r2:
					l.append(c)
				elif r0 > r2 and r2 > r3:
					l = [c]
					r0 = r2
			i2 = random.randint(0,len(l) - 1)
			i2 = l[i2]
	else:
		#is bug probably
		print("bug")
		i1 = 0
		i2 = 1
		
	
	while get_data(i1).related(dataInd[i2]):
		i1 = s.randInd()
		while get_data(i1).range == 0:
			i1 = s.randInd()
		i2 = s.randInd()
		while get_data(i2).range == 0 or i1 == i2:
			i2 = s.randInd()
	
	comp(i1,i2,partSort)

def checkDone():
	global data, dataInd, ar, listLen
	for c in range(listLen):
		d = get_data(c)
		if d.range() == 0:
			if c == d.iMin:
				d.done = True
				r.drawDone(c)
	pygame.display.update()

def totalSize(maxSize = -1):
	global data
	size = 0
	
	if maxSize == -1:
		for c in data:
			size += len(c.above)
			size += len(c.below)
	else:
		for c in data:
			size += len(c.above)
			size += len(c.below)
			if size > maxSize:
				return size
	return size
		
def propagate():
	did = True
	while did:
		did = False
		for c in data:
			if did:
				c.calc()
			else:
				rel = c.relatives()
				c.calc()
				did = rel < c.relatives()		


def do_swaps():
	did = True
	didAny = False
	while did:
		did = False
		for c in range(listLen):
			d = get_data(c)
			if d.range() == 0:
				if c != d.iMin:
					didAny = True
					d.done = True
					swap(c,d.iMin)
					r.drawDone(d.iMin)
					if d.iMin < c:
						did = True
						break
	return didAny

def swap(a,b):
	global ar, dataInd
	s.swap(a,b)
	
	temp=dataInd[a]
	dataInd[a]=dataInd[b]
	dataInd[b]=temp


