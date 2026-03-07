file = open("output2.txt")
lines = file.readlines()
width = len(lines[0]) - 1
height = len(lines) - 4
print(height)
print(width)
horizontal_lines = []
vertical_lines = []
pixel = format(int("3", 16), "04b")
bottom_line = []
for y, line in enumerate(lines[:-4]):
    x_line = []
    y_line = []
    right_line = []
    for x,c in enumerate(line[:-1]):
        pixel = format(int(c, 16), "04b")
        print(pixel)
        print(pixel[0])
        print(pixel[2])
        print(x)
        x_line.append(pixel[0]) #gora
        y_line.append(pixel[2]) #lewa
        if y == height - 1:
            bottom_line.append(pixel[3])
        if x == width - 1:
            y_line.append(pixel[1])
    horizontal_lines.append(x_line)
    vertical_lines.append(y_line)
horizontal_lines.append(bottom_line)

        #self.image_data[:4] = bytes([0,0,0,255]) 0011 west south east north
print(horizontal_lines)
print(vertical_lines)