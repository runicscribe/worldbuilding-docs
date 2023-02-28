import os
import subprocess

header = "layout: default\n"

def proc_file(f):
  # Is this a file?
  if f.endswith(".md"):
    permalink = f[1:]
	# Index permalinks to folder, others permalink to self
    if f.endswith("index.md"):
      permalink = permalink[:-8]
    else:
      permalink = permalink[:-3]
    
	# Apply subfolder styles
    if f.startswith("./dae-machina"):
      header="layout: dm_style\n"
    if f.startswith("./magepunk"):
      header="layout: mp_style\n"
    if f.startswith("./schizotech"):
      header="layout: st_style\n"

    sp = subprocess.Popen("git checkout master "+f, shell=True)
    sp.wait()
    fin = open(f, 'r', encoding='utf-8')
    data = fin.read()
    fin.close()
    fout = open(f, 'w', encoding='utf-8')
    fout.write("---\n"+header+"permalink: "+permalink+"\n"+"---\n"+"\n"+data)
    fout.close()
      
def find_files(folder):
  contents = os.listdir(folder)
  files = []
  for f in contents:
    filepath = folder + "/" + f
    if (f.startswith(".")):
      print("Skipping "+filepath)
    elif os.path.isfile(filepath):
      print("Processing file: "+filepath)
      files.append(filepath)
    elif os.path.isdir(filepath):
      print("Processing folder: "+filepath)
      files.extend(find_files(filepath))
    else:
      print("File: "+filepath+" does not exist")
  return files
  
print("Updating source files from master")
sp = subprocess.Popen("git stash", shell=True)
sp.wait()
sp = subprocess.Popen("git checkout master", shell=True)
sp.wait()
sp = subprocess.Popen("git pull origin master", shell=True)
sp.wait()

files = find_files('.')

sp = subprocess.Popen("git checkout gh-pages", shell=True)
sp.wait()
sp = subprocess.Popen("git stash apply", shell=True)
sp.wait()

for f in files:
  proc_file(f)
