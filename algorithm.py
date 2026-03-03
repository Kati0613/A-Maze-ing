file = open("output.txt")
lines = file.readlines()
width = len(lines[0])
height = len(lines) - 4
print(len(lines))
pixel = format(int("3", 16), "04b")
for line in lines[:-3]:
    for c in line[:-1]:
        pixel = format(int(c, 16), "04b")
        #self.image_data[:4] = bytes([0,0,0,255]) 0011 west south east north