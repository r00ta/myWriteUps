import base64
import binascii
import re

def solve():
	ad = open('log_add.txt').read().split('\n')[:-1]
	ad = {key: re.findall('.'*32, ad[key]) for key in range(len(ad))}

	xo = open('log_xor.txt').read().split('\n')[:-1]

	xo = {key: re.findall('.'*32, xo[key]) for key in range(len(xo))}

	ad_all = reduce(lambda x, y: x + y, map(lambda x: ad[x], ad.keys()))


	xo_all = reduce(lambda x, y: x + y, map(lambda x: xo[x], xo.keys()))


	inter = set(ad_all).intersection(set(xo_all))

	inter_dict = {x : [] for x in inter}

	#inverse_dict = {}

	for x in inter:
		try:
			inter_dict[x].append( ( filter(lambda y: x in ad[y], ad.keys() )[0], 'add') ) 
		except:
			pass
		try:
			inter_dict[x].append( ( filter(lambda y: x in xo[y], xo.keys() )[0], 'xor') ) 
		except:
			pass
	conditions = []
	for x in inter_dict.keys():
		conditions.append('{} + x == {} ^ x'.format(inter_dict[x][0][0], inter_dict[x][1][0]))

	final = []
	for x in range(255):
		res = []
		for y in conditions:
			res.append(eval(y))
		if all(res):
			final.append(x)
	return final
#print inverse_dict
