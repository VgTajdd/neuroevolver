import os
import sys

walk_dir = sys.argv[1]

def put_header(filename, header):
	content = header + '\n'

	file = open(filename)
	for line in file:
		line = line.rstrip() # This deletes break line.
		#print(line)
		content += ('\n'+ line)

	open(filename, "w").close() # Overwrite

	with open(filename, 'a') as out:
	    out.write(content)

headerBase = '\
## ========================================================================= ##\n\
## Copyright (c) 2019 Agustin Durand Diaz.                                   ##\n\
## This code is licensed under the MIT license.                              ##\n\
## XXX                                                                       ##\n\
## ========================================================================= ##'

indexForFilename = headerBase.find( 'XXX' )

print('walk_dir = ' + walk_dir)

# If your current working directory may change during script execution, it's recommended to
# immediately convert program arguments to an absolute path. Then the variable root below will
# be an absolute path as well. Example:
# walk_dir = os.path.abspath(walk_dir)
print('walk_dir (absolute) = ' + os.path.abspath(walk_dir))

for root, subdirs, files in os.walk(walk_dir):

    for filename in files:
        filePath = os.path.join(root, filename)

        if filename == '__init__.py':
        	print("SKIPPED: " + filePath)
        	continue

        if not filename.lower().endswith(('.py')):
        	print("SKIPPED: " + filePath)
        	continue

        newHeader = headerBase[:indexForFilename] + filename + headerBase[(indexForFilename+len(filename)):]

        print("DONE: " + filePath)
        put_header(filePath, newHeader)