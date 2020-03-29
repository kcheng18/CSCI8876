def readFileb(name):
    with open(name, 'rb') as f:
        data = f.read()
        f.close()
        return data

def createfileb(filename, text):
    with open(filename, 'wb') as f:
        f.write(text)
        f.close()

def readFile(name):
    with open(name, 'r') as f:
        data = f.read()
        f.close()
        return data

def createfile(filename, text):
    with open(filename, 'w') as f:
        f.write(text)
        f.close()