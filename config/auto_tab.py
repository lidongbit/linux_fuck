from sys import argv
import re,sys
argc = int(len(argv))
if argc<4:
	print('Usage: python 0-%s 1-file_name 2-tab_name 3-begin_num !'%argv[0])
	sys.exit()
	
f = open('%s'%argv[1], 'r')
f_new = open('%s.bak'%argv[1],'w')
txt = '[REMOTE_NET_12]'
if re.match(r'\[REMOTE\_NET\_\d{2}\]', txt):
    print('match')
else:
    print('not match')
