#coding: utf8
#author: alb

from ctypes import *
import time, sys, os
import numpy as np

Array6 = c_double*6

h = 0
h = windll.LoadLibrary('swedll32.dll')
for xpath in sys.path:
	dpath = xpath + '\swedll32.dll'
	if os.path.isfile(dpath):
		h = windll.LoadLibrary(dpath)
if not h: raise Exception('dll not found')

swe_calc = getattr(h, '_swe_calc@24')
swe_houses_ex = getattr(h, '_swe_houses_ex@40')

#swe_deltat = getattr(h, '_swe_deltat@8')

PL_NAMES = ['sun', 'moon', 'mercury','venus','mars', 'jupitor','saturn','uranus', 'neptune', 'pluto']
PL_CHAR = '日月水金火木土天海冥'.decode('utf8')
PL_HOUSE = ['Ari','Tau','Gem','Can','Leo','Vir','Lib','Sco','Sag','Cap','Aqu','Pis']

def ASTROLOG_DEG_REPR(x):
	ihouse = int(x/30)
	ideg = int(x-ihouse*30)
	quitint = lambda x: x-int(x)
	idegfin = int(quitint(x-ihouse*30)*60)
	ret = '%d%s%2d'%(ideg, PL_HOUSE[ihouse], idegfin)
	ret = ret.replace(' ', '0')
	return ret

def gen_degree(sdate = '19690505', dtt = 0):
	'''
		format:	'1969.05.05' or '19690505'
	'''
	if len(sdate) == 10:
		sdate = sdate.replace('.', '')
	year = int(sdate[:4])
	if year < 1971:
		f = 1971 - year
		dt = time.strptime('1971'+sdate[-4:], '%Y%m%d')
		tm = time.mktime(dt) - f*365.24*24*60*60
	else:
		dt = time.strptime(sdate, '%Y%m%d')
		tm = time.mktime(dt)
	return gen_degree_by_timestamp(tm+dtt)

def gen_degree_by_timestamp(timestamp, in_place = ''):
	bs = time.mktime(time.strptime('19970101', '%Y%m%d')) - 2450449.5*24*60*60
	timetemp = (timestamp - bs)/24/60/60
	Angles = []
	STARS = range(10) + []
	for id in STARS:
		i		= 	c_long(id)
		iflag 	= 	c_long(258)
		j 		= 	c_long(0)
		time_et = 	c_double(timetemp)
		x 		= 	Array6(0,0,0,0,0,0)
		serr 	=	c_char_p(' '*256)
		swe_calc(time_et, i, iflag, byref(x), serr)
		Angles.append(x[0])
	return Angles
	
def gen_aspect(deglist, sigstr = 'rysjhmtTHM'+'rysjhmtTHM', pansplitlen = 0):
	L = len(deglist)
	allowance = 5
	result = []
	half_a = allowance/2
	C = sigstr
	for i in range(L):
		for j in range(i+1, L):
			if pansplitlen != 0:
				if i>=pansplitlen or j<pansplitlen: continue
			deg1, deg2 = deglist[i], deglist[j]
			r = (deg1-deg2+half_a+720)%360-half_a
			if abs(r-120) < half_a or abs(r-240) < half_a:
				result.append(C[i]+C[j]+'v')
			elif abs(r-180) < half_a:
				result.append(C[i]+C[j]+'x')
			elif abs(r) < half_a:
				result.append(C[i]+C[j]+'o')
			elif abs(r-90) < half_a:
				result.append(C[i]+C[j]+'e')
	return result

if __name__ == '__main__':
	deglist = gen_degree('20141125')
	x = deglist
	print(x)
	