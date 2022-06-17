import os

# f = open("./docs", "w+")
files = []
for filename in os.listdir("./docs"):
    # print(filename)
    if os.path.isdir("./docs" + filename):
        print(filename)
#     content = """![](../imgs/{})
# """.format(filename)
#     f.write(content)
# f.close()

for parent, dirnames, filenames in os.walk("./docs"):
    for name in filenames:
        if name.endswith(".md"):
            cur = os.path.join(parent, name)
            files.append(cur)
            print(cur)
# opening the file in read mode
name = "./docs/计算机网络/一些关键笔记.md"
file = open(name, "r")
replacement = ""
# using the for loop
for line in file:
    line = line.strip()
    line = line.replace('<div align="center"> <img src="../imgs', '<div align="center"> <img src="https://raw.githubusercontent.com/wardseptember/notes/master/imgs')
    line = line.replace('<div align="center"> <img src="../../imgs', '<div align="center"> <img src="https://raw.githubusercontent.com/wardseptember/notes/master/imgs')
    print(line)
    replacement = replacement + line + "\n"


file.close()
# opening the file in write mode
fout = open("test.md", "w")
fout.write(replacement)
fout.close()