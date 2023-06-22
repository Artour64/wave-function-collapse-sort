import pygame

import config as co
import render as r
import sort as s

import vone

listLen=co.listLen
ar=list(range(listLen));

r.ar=ar
s.ar=ar
vone.ar=ar

r.drawAr()
pygame.time.wait(1000)

s.shuffle()

#pygame.time.wait(500)
#s.randSortSwaps(200)

#s.minishuffle(20)
#s.minishuffle(100)
#s.minishuffle(1000)
#s.reverse()

pygame.time.wait(1000)

#pygame.display.update()

#s.comb(1.3,5)

compPass = True
compPass = False

partSort = True
#partSort = False

vone.sort(compPass,partSort)


print("done")

if co.stay:
	import events as ev
	while ev.running:
		for event in pygame.event.get():
			ev.event(event)
