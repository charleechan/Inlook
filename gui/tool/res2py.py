import subprocess, os, sys



images = os.listdir(sys.argv[1])
qss = os.listdir(sys.argv[2])
f = open(sys.argv[3], 'w+')
f.write(u'<RCC>\n\t<qresource prefix="/">\n')

for item in images:
    f.write(u'\t\t<file>img/'+ item +'</file>\n')
    
for item in qss:
    f.write(u'\t\t<file>qss/'+ item +'</file>\n')

f.write(u'\t</qresource>\n</RCC>')
f.close()

