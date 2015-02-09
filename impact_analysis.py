# -*- coding: utf-8 -*-
'''
Created on 30/08/2012
@author: Valtoni Boaventura (valtoni@gmail.com)
'''
import sys
import re
import os
import datetime
import project
from subprocess import call

''' Declarations '''

# Find svn
def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

# URL root
url_root = 'http://svnserver/project/trunk/'

# Analysing files
defaultdir = os.path.dirname(os.path.realpath(__file__))
file_impacts = os.path.join(defaultdir, 'impacts.txt')
file_result = os.path.join(defaultdir, 'impact_result.log')
file_projects = os.path.join(defaultdir, 'impact_projects.txt')

# Default searches
dir_proj = os.path.join(defaultdir, 'analysed')
search_exts = (["java", "py", "txt"])
format_date = "%d/%m/%Y %H:%M:%S"

svn_exe = which("svn")

if svn_exe is None:
  svn_exe = which("svn.exe")
  if svn_exe is None:
    print "svn executable was not found in path"
    sys.exit(1)
  
# functions
def readfile(filename):
    return open(filename).read().splitlines()

def formatintocomma(list_comma):
    return ",".join(list_comma)
    
def filesintarget(projectsdir, filters = search_exts):
    foundfiles = []
    for dirname, dirnames, filenames in os.walk(projectsdir):
        for subdirname in dirnames:
            os.path.join(dirname, subdirname)
        for filename in filenames:
            for search_ext in search_exts: 
                if re.match(".*\." + search_ext + "$", filename, re.IGNORECASE):
                    foundfiles.append(os.path.join(dirname, filename))
    return foundfiles

def log(logtext):
    logfile = open(file_result, "a")
    logfile.write(logtext + "\n")
    logfile.close()

def chekout_svn_project(project, dir_proj):
    tmp_dir = os.path.join(dir_proj, project.rawdir)
    if not os.path.exists(tmp_dir):
        call([svn_exe, "co", project.url, tmp_dir])
    else:
        call([svn_exe, "up", tmp_dir])

''' Implementations '''

# Building lists
list_projects = readfile(file_projects)
list_impacts = readfile(file_impacts)

# Build files and projectsto be scanned


for project_url in list_projects:
    project_instance = project.Project(url_root, project_url)
    chekout_svn_project(project_instance, dir_proj) 

list_target_files = filesintarget(dir_proj)


# initializing analysis...
initialized_time = datetime.datetime.now()
log("*** Impact analisys initialized in " + initialized_time.strftime(format_date))
log("Analysed: " + formatintocomma(list_impacts))

# Find impacts
for file_impacted in list_target_files:
    displayed = False
    for impact in list_impacts:
        line = 0;
        for readed_line in readfile(file_impacted):
            line += 1
            if re.match(".*" + impact + ".*", readed_line, re.IGNORECASE):
                if not displayed:
                    log('File: ' + file_impacted)
                    displayed = True
                log(str(line) + ": " + readed_line)

delta_time = datetime.datetime.now() - initialized_time
log("*** Finalyzed {0} ({1}min)".format(datetime.datetime.now().strftime(format_date), "x"))