import os

files = []
for parent, dirnames, filenames in os.walk("./docs"):
    for name in filenames:
        if name.endswith(".md"):
            cur = os.path.join(parent, name)
            files.append(cur)

for name in files:
    file = open(name, "r")
    replacement = ""
    need_replace = False
    for line in file:
        line = line.strip()
        if '<div align="center"> <img src="../imgs' in line or '<div align="center"> <img src="../../imgs' in line  or "wardseptember.top" in line:
            need_replace = True
        line = line.replace('<div align="center"> <img src="../imgs', '<div align="center"> <img src="https://raw.githubusercontent.com/wardseptember/notes/master/imgs')
        line = line.replace('<div align="center"> <img src="../../imgs', '<div align="center"> <img src="https://raw.githubusercontent.com/wardseptember/notes/master/imgs')
        line = line.replace('http://wardseptember.top', '<div align="center"> <img src="https://raw.githubusercontent.com/wardseptember/notes/master/imgs')
        replacement = replacement + line + "\n"
    file.close()
    if need_replace:
        fout = open(name, "w")
        fout.write(replacement)
        fout.close()