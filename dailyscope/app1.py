#coding:utf8

import swe, time, sys

mchr = u'日月水金火木土天海冥'

def findtext(key, cree, spec):
	keym = key+u'相位'
	for i in range(len(msfile)):
		if msfile[i].find(keym) != -1:
			if spec in [3,6]:
				return key+msfile[i+2]
			else:
				return key+msfile[i+1]
				
def gen_ps(i):
	datestr = time.strftime('%Y%m%d', time.gmtime(time.time()+24*60*60*i))
	ps2 = swe.gen_degree(datestr)
	if 'nature' in sys.argv:
		ps = ps2
	else:
		ps = swe.gen_degree(sys.argv[1])
	return ps, ps2, datestr

file1 = open('0data.txt', 'r')
msfile = file1.read().decode('utf8').split('\n')

for i in range(7):
	ps, ps2, datestr = gen_ps(i)
	print u'\n今日运势', datestr
	items = []
	for i in range(10):
		for j in range(10):
			if 'nature' in sys.argv and i>j:
				continue
			aa,bb = ps[i], ps2[j]
			ms = abs(aa-bb)
			cree = 0
			spec = int((ms+2)/30)
			if ((ms+32)%30)<4: cree = 1
			if ((ms+31)%30)<2: cree = 2
			if cree:
				if i>6 or j>6: cree+=10
				if spec not in [3,4,6]: cree+=100
				additem = [mchr[i]+mchr[j]+'%d'%spec, '%3d'%cree]
				items.append(additem)
				if cree==1:
					print '-------'
					print findtext(mchr[i]+mchr[j], cree, spec)
					print findtext(mchr[j]+mchr[i], cree, spec)

	print '-------'
	items.sort(key=lambda x:x[1])
	for i in items:
		print i[0], i[1]
			