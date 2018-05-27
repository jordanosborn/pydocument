from subprocess import run
#run(["./pdftohtml", "2017-financial-statements-en.pdf", "output"])
text = '<html><head></head>\n<body></body></html>'
import glob
filelist = []
for filename in glob.iglob('./output/*.html'):
     filelist.append(filename)

def findcontent(tag, text, get_text = False):
	start = 0
	end = len(text)
	close_tag = tag.replace('<','</')
	for i in range(0,len(text)):
		if text[i:i+len(tag)] == tag:
			start = i +len(tag)
		elif text[i:i+len(close_tag)] == close_tag:
			end = i
			break
	if get_text:
		return text[start:end]
	else:
		return (start, end)

import re

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

filelist = natural_sort(filelist)

for f in filelist:
	a = open(f,'r')
	t = a.read()
	t_body = findcontent('<body>', t, True)
	t_head = findcontent('<head>', t, True)
	tag_head = findcontent('<head>', text)
	text = text[:tag_head[0]] + t_head + text[tag_head[0]:]
	tag_body = findcontent('<body>', text)
	text = text[:tag_body[1]] + t_body + text[tag_body[1]:]
	a.close()
	print(f)
b = open('file.html','w')
b.write(text)
b.close()