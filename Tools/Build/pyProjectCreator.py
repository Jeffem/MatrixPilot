'''
Created on 31 August 2014

@author: Robert Dickenson
'''

import os, fnmatch

rootdir = ""

# MPLAB8 project builder variables
file_subfolders = ""
other_files = ""
file_info = ""
file_cnt = 0

def mkdirnotex(filename):  
	folder = os.path.dirname(filename)  
	if not os.path.exists(folder):  
		os.makedirs(folder) 

def count_files(masks, dir):
	count = 0
	for entry in os.listdir(dir):
		if os.path.isfile(os.path.join(dir, entry)):
			for mask in masks:
				if fnmatch.fnmatch(entry, mask):
					count = count + 1
	return count

def find_files(masks, dir):
	str = ""
	for entry in os.listdir(dir):
		if os.path.isdir(os.path.join(dir, entry)):
			title = entry.replace(rootdir, "")
			count = count_files(masks, os.path.join(dir, title))
			if count != 0:
				str = str + "      <logicalFolder name=\"" + title + "\" displayName=\"" + title + "\" projectFiles=\"true\">\n"
				str = str + find_files(masks, os.path.join(dir, entry))
				str = str + "      </logicalFolder>\n"
		else:
			for mask in masks:
				if fnmatch.fnmatch(entry, mask):
					str = str + "        <itemPath>" + dir.replace("\\", "/") + "/" + entry + "</itemPath>\n"
	return str

def find(masks, startdir=os.curdir):
	fullpath = []
	for (thisDir, subsHere, filesHere) in os.walk(startdir):
		path = thisDir.replace(rootdir, "..")
		for name in subsHere + filesHere:
			if fnmatch.fnmatch(name, masks):
				fullpath = fullpath + [os.path.join(path, name)]
	return fullpath

def mplab8_scan_dirs(masks, directories):
	global file_subfolders
	global other_files
	global file_info
	global file_cnt
	for directory in directories:
		path = os.path.join(rootdir, directory)
		files = find(masks, path)
		for filename in files:
			file_subfolders = file_subfolders + "file_" + str.format('{:0>3}', file_cnt) + "=" + directory + '\n'
			other_files = other_files + "file_" + str.format('{:0>3}', file_cnt) + "=no\n"
			file_info = file_info + "file_" + str.format('{:0>3}', file_cnt) + "=" + filename + '\n'
			file_cnt = file_cnt + 1

def mplab8_project(mcu_type, target_board, config_dir, project_output_file):
	with open ("mplab8-template.txt", "r") as file:
		data = file.read()
		data = data.replace("%%DEVICE%%", mcu_type)
		data = data.replace("%%CONFIG%%", config_dir)
		data = data.replace("%%TARGET_BOARD%%", target_board)
		data = data.replace("%%FILE_SUBFOLDERS%%", file_subfolders)
		data = data.replace("%%GENERATED_FILES%%", other_files)
		data = data.replace("%%OTHER_FILES%%", other_files)
		data = data.replace("%%FILE_INFO%%", file_info)
	mkdirnotex(project_output_file)
	with open (project_output_file, "w") as file:
		file.write(data)

def vs2010_scan_dirs(masks, sources, directories):
	str = ""
	for dir in directories:
		path = os.path.join(rootdir, dir)
		for mask in masks:
			files = find(mask, path)
			for filename in files:
				if sources == 1:
					str = str + "    <ClCompile Include=\"" + filename.replace("/", "\\") + "\" />\n"
				else:
					str = str + "    <ClInclude Include=\"" + filename.replace("/", "\\") + "\" />\n"
	return str

def vs2010_scan_filter_dirs(masks, sources, prefix, directories):
	str = ""
	for dir in directories:
		path = os.path.join(rootdir, dir)
		for mask in masks:
			files = find(mask, path)
			for filename in files:
				fname = filename.replace("/", "\\")
				if sources == 1:
					str = str + "    <ClCompile Include=\"" + fname + "\">\n"
					str = str + "      <Filter>" + prefix + os.path.dirname(fname.replace("..\\", "")) + "</Filter>\n"
					str = str + "    </ClCompile>\n"
				else:
					str = str + "    <ClInclude Include=\"" + fname + "\">\n"
					str = str + "      <Filter>" + prefix + os.path.dirname(fname.replace("..\\", "")) + "</Filter>\n"
					str = str + "    </ClInclude>\n"
	return str

def vs2010_project(mcu_type, target_board, config_dir, header_files, source_files, project_output_file):
	with open ("template.vcxproj", "r") as file:
		data = file.read()
		data = data.replace("%%CONFIG%%", config_dir)
		data = data.replace("%%SOURCE_FILES%%", source_files)
		data = data.replace("%%HEADER_FILES%%", header_files)
	mkdirnotex(project_output_file)
	with open (project_output_file, "w") as file:
		file.write(data)

def vs2010_project_filters(mcu_type, target_board, config_dir, header_files, source_files, project_output_file):
	with open ("template.vcxproj.filters", "r") as file:
		data = file.read()
		data = data.replace("%%SOURCE_FILES%%", source_files)
		data = data.replace("%%HEADER_FILES%%", header_files)
	mkdirnotex(project_output_file)
	with open (project_output_file, "w") as file:
		file.write(data)

def mplabX_scan_dirs(masks, directories):
	str = ""
	for dir in directories:
		path = os.path.join(rootdir, dir)
		str = str + "      <logicalFolder name=\"" + dir + "\" displayName=\"" + dir + "\" projectFiles=\"true\">\n"
		str = str + find_files(masks, path)
		str = str + "      </logicalFolder>\n"
	return str

def mplabX_project(mcu_type, name, target_board, config_dir, header_files, source_files, project_path):
	mkdirnotex(os.path.join(project_path, "Makefile"))
	with open ("Makefile", "r") as file:
		data = file.read()
	with open (os.path.join(project_path, "Makefile"), "w") as file:
		file.write(data)
	project_path = os.path.join(project_path, "nbproject")
	mkdirnotex(os.path.join(project_path, "nbproject"))
	with open ("configurations.xml", "r") as file:
		data = file.read()
		data = data.replace("%%NAME%%", name)
		data = data.replace("%%DEVICE%%", mcu_type)
		data = data.replace("%%CONFIG%%", config_dir)
		data = data.replace("%%TARGET_BOARD%%", target_board)
		data = data.replace("%%HEADER_FILES%%", header_files)
		data = data.replace("%%SOURCE_FILES%%", source_files)
	with open (os.path.join(project_path, "configurations.xml"), "w") as file:
		file.write(data)
	with open ("project.xml", "r") as file:
		data = file.read()
		data = data.replace("%%NAME%%", name)
		data = data.replace("%%TARGET_BOARD%%", target_board)
	with open (os.path.join(project_path, "project.xml"), "w") as file:
		file.write(data)

if __name__ == '__main__':

	from optparse import OptionParser
	parser = OptionParser("pyProjectCreator.py [options]")
	parser.add_option("-n", "--name", dest="name", help="specify the project name", type="string", default="MatrixPilot", metavar="MatrixPilot")
	parser.add_option("-t", "--target", dest="target", help="specify the target board", type="string", default="UDB5", metavar="UDB5")
	parser.add_option("-d", "--dir", dest="directories", help="search directory for source files", action='append')
	parser.add_option("-i", "--inc", dest="includes", help="additional include files directory", default="")
	parser.add_option("-c", "--cfg", dest="config", help="specify configuration files directory", default="../Config")
	parser.add_option("-o", "--out", dest="out", help="project files output path", default="output")
#	parser.add_option("--defines", dest="defines", help="specify optional defines", action='append')
	(opts, args) = parser.parse_args()

	rootdir = os.path.join("..", "..")

	if opts.target == "UDB4":
		arch = "dsPIC33FJ256GP710A"
	elif opts.target == "UDB5":
		arch = "dsPIC33FJ256GP710A"
	elif opts.target == "AUAV3":
		arch = "dsPIC33EP512MU810"
	else:
		arch = ""

	if opts.target == "SIL":
		sources = vs2010_scan_dirs(["*.c"], 1, opts.directories)
		headers = vs2010_scan_dirs(["*.h"], 0, opts.directories)
		project_path = os.path.join(opts.out, opts.name + "-" + opts.target + ".vcxproj")
		print "writing: " + project_path
		vs2010_project(arch, opts.target, opts.config, headers, sources, project_path)
		source_filter = vs2010_scan_filter_dirs(["*.c"], 1, "Source Files\\", opts.directories)
		header_filter = vs2010_scan_filter_dirs(["*.h"], 0, "Header Files\\", opts.directories)
		project_path = os.path.join(opts.out, opts.name + "-" + opts.target + ".vcxproj.filters")
		vs2010_project_filters(arch, opts.target, opts.config, header_filter, source_filter, project_path)
	else:
		mplab8_scan_dirs("*.c", opts.directories)
		mplab8_scan_dirs("*.s", opts.directories)
		mplab8_scan_dirs("*.h", opts.directories)
		project_path = os.path.join(opts.out, opts.name + "-" + opts.target + ".mcp")
		print "writing: " + project_path
		mplab8_project(arch, opts.target, opts.config, project_path)

		headers = mplabX_scan_dirs(["*.h", "*.inc"], opts.directories)
		sources = mplabX_scan_dirs(["*.c", "*.s"], opts.directories)
		project_path = os.path.join(opts.out, opts.name + "-" + opts.target + ".X")
		print "writing: " + project_path
		mplabX_project(arch, opts.name, opts.target, "../" + opts.config, headers, sources, project_path)
