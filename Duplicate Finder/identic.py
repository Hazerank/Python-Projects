#!/usr/bin/python3
import argparse
import os
import hashlib

"""
This is the part when I arrange parser arguments

My program also handles the cases where -d and -f comes together.
It is implemented as mutually exclusive in -c -n -cn cases
because in the lecture Can Hoca explains in that way.
"""
parser = argparse.ArgumentParser()
parser.add_argument("-d",action="store_true",default=False)
parser.add_argument("-f",action="store_true",default=False)
parser.add_argument("-s",action="store_true",default=False)
parser.add_argument("dirs",nargs="*",default=".",type=str)
group = parser.add_mutually_exclusive_group()
group.add_argument("-c", action="store_true", default=True)
group.add_argument("-n", action="store_true", default=False)
group.add_argument("-cn",action="store_true",default=False)

args = parser.parse_args()
dirs = []


"""
Those are storage elements as dictionaries.
	
hfiles (int,list(str)): The map that maps file hashes to full paths of files that has same hash value.
hdirs (int,list(str)): The map that maps directory hashes to full paths of directories that has same hash value.
dirsizes (int,int): The map that maps directory hashes to sizes of directories.

At the beginning, the size of the empty directory is assigned as 0  bytes.
"""
hfiles,hdirs,dirsizes = {},{},{}
dirsizes[hashlib.sha256("".encode()).hexdigest()] = 0

def hasher(name):
	"""
	Calculates hash for a file and add it to corresponding storage element which is hfiles.

	Hashes according to the arguments "args"  using sha256().
	-n: hashes the name of the file
	-c: hashes the content of the file via reading file as rb
	-cn: hashes the concatenation of the name and the content.
	If "-n", size is assigned to 0.
	Adds [hash : [full_path]] pair to the hfiles dictionary if doesn't exist.
	If calculated hash exist in the dictionary, adds full_path to the list of that hash value.

	Parameters:
		name (str): Absolute or relative path of the file that will be hashed.
	
	Returns:
		list (hash,size): returns the corresponding hash value and the size of the file 
	"""
	size = 0
	BLOCK_SIZE = 65536  #Block size when reading file as parts 
	file_hash = hashlib.sha256()

	if(args.n):
		hash = hashlib.sha256(os.path.basename(name).encode()).hexdigest() # if name is important, It is added to the hash
	else:
		size = os.stat(name).st_size
		if(args.cn):
			file_hash.update(os.path.basename(name).encode())
		
		with open(name, 'rb') as f: 
			fb = f.read(BLOCK_SIZE) 
			while len(fb) > 0: 
				file_hash.update(fb)
				fb = f.read(BLOCK_SIZE)
		hash = file_hash.hexdigest()

	if hash in hfiles:
		hfiles[hash].append(os.path.abspath(name))
	else:
		hfiles[hash] = [os.path.abspath(name)]

	return [hash,size]

def traverse(dir):
	"""
	Traverses all subdirectories of given "dir" and fills the corresponding hash and size tables.

	It works in an iterative way. Traverses its subfiles and subdirectories and calculates hash values.
	When it has a file as child, calls hasher() function.
	When it has a directory, calls itself.
	Iteration stops when it has no children as directory.
	When it is an empty directory, hashes empty string in case of -c, hashes name of the dir otherwise.
	Finds hash of the directory by concatenating subfiles or directories hashes. In case of -n or -cn, adds name of the direction beginning.
	It also calculates size of the directory as sum of the sizes of its sub-elements and stores in the size map.

	Parameters:
		dir (str): Absolute or relative path of the direction that will be hashed.
	
	Returns:
		list (hash,size): returns the corresponding hash value and the size of the dir 

	"""
	arguments = []                 # The list that stores child hash values.
	children = os.listdir(dir)
	sizeTotal = 0                  # Sum of sizes of the children
	if len(children) == 0:         # When it has no element in it, the empty dir case.
		if args.n or args.cn:
			hash = hashlib.sha256(os.path.basename(dir).encode()).hexdigest() 
		else:
			hash = hashlib.sha256("".encode()).hexdigest()
		if hash in hdirs:
			hdirs[hash].append(os.path.abspath(dir))
		else:
			hdirs[hash] = [os.path.abspath(dir)]
		
		return [hash,sizeTotal]

	for item in children:                    # Traversing children
		newitem = os.path.join(dir,item)
		if os.path.isdir(newitem):           # Directory Case
			result = traverse(newitem)
			arguments.append(result[0])
			sizeTotal += result[1]
		else:                                # File Case
			result = hasher(newitem)
			arguments.append(result[0])
			sizeTotal += result[1]

	arguments.sort()                         # Hash values are sorted.

	if(args.n or args.cn):
		arguments.insert(0, hashlib.sha256(os.path.basename(dir).encode()).hexdigest())
	
	hash =  hashlib.sha256(listToStr(arguments).encode()).hexdigest()


	if hash in hdirs:
		hdirs[hash].append(os.path.abspath(dir))
	else:
		hdirs[hash] = [os.path.abspath(dir)]

	if hash not in dirsizes:
		dirsizes[hash] = sizeTotal
		
	return [hash,sizeTotal]

def listToStr(list):
	"""
	Takes a list of string and returns a string as concateanted.

	Parameters:
		list (str): A list of string
	
	Returns:
		str (str): Single string that concatenation of elements.
	
	"""

	str = ""
	for element in list:
		str += element
	return str


"""
In this part, nested paths are handled

Every path turned into absolute path and with string manipulation, checked if any nested paths exist.
If so, eliminated nested path.
"""
for i in range(len(args.dirs)):
	dirs.append(os.path.abspath(args.dirs[i]))

dirs = list(dict.fromkeys(dirs))     # List of paths

for dir in dirs:

	duplicated = False
	for other in dirs:
		if other == dir:
			continue 
		if dir.startswith(other):
			duplicated = True 
	if not duplicated:
		traverse(dir) 


"""
In this part, hash values are traversed as constrained by arguments.
They stored in printList dictionary.

Dictionary stores 2 types of maps in two different cases.

When -s case, printList maps size values to list of the full paths of that corresponding sized.

Otherwise, printList maps paths with same hashes, first path maps to rest of the paths list.

It is implemented in this way in order to sort paths easily with sort methods.
In this manner, Key values can be sorted easily both cases when it is size or the first element.

Every path list is also sorted in alphabetic order.

After all sorting process, we have lists sorted by both alphabetic and sized.
"""
printList = {}
if args.f or not (args.f or args.d) :
	for temp in hfiles:
		listTemp = sorted(hfiles[temp])
		if len(listTemp) > 1:
			if args.s and not args.n:
				size = os.stat(listTemp[0]).st_size
				if size in printList:
					printList[size].append(listTemp)
				else:
					printList[size] = [listTemp]
			else:
				printList[listTemp[0]] = listTemp[1:] 
			
if(args.d):
	for temp in hdirs:
		listTemp = sorted(hdirs[temp])
		if len(listTemp) > 1:
			if args.s and not args.n:
				size = dirsizes[temp]
				if size in printList:
					printList[size].append(listTemp)
				else:
					printList[size] = [listTemp]
			else:
				printList[listTemp[0]] = listTemp[1:] 

"""
This part is to print printlist in the form as description.
"""
keys = printList.keys()
keys = sorted(keys)
if args.s:
	keys = reversed(keys)
for key in keys:
	if(args.s and not args.n):
		for file in sorted(printList[key]):
			for one in file:
				print(one + "\t" + str(key))
			print()
	else:
		print (key)
		for file in printList[key]:
			print(file)	
		print()