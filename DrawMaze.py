from mlx import Mlx

class Maze():

#output na pliki
    def __init__(self, mlx, ptr, window):
        self.mlx = mlx
        self.window = window
        self.ptr = ptr
        self.fourtytwo = []
        self.fourtytwo_color = bytes([0, 255, 255, 255])

        self.x = 0
        self.y = 0
        self.i = 0
        self.z = 0

        self.color = bytes([0, 255, 255, 255])

        file = open("output.txt")
        self.lines = file.readlines()
        self.width_img = len(self.lines[0]) - 1
        self.height_img = len(self.lines) - 4
        self.size = 32
        self.img_ptr = self.mlx.mlx_new_image(
            self.ptr, self.width_img * self.size,
            (self.height_img + 1) * (self.size - 1)
            )# 800 to piksele czyli jeden piksel to 4 bity czyli jeden bajt
        self.mlx_img_data = self.mlx.mlx_get_data_addr(self.img_ptr)
        self.image_data = self.mlx_img_data[0]
        self.line_length = self.mlx_img_data[2]
        self.mlx.mlx_put_image_to_window(
            self.ptr, self.window, self.img_ptr, 560, 140)
    
    def draw_maze(self, color=bytes([255, 255, 255, 255]), pixel=None):
        color = bytes(color)
        print(len(self.image_data))
        start_parameters = self.lines[-3]
        end_parameters = self.lines[-2]
        self.startx = int(start_parameters[:start_parameters.find(",")])
        self.starty = int(start_parameters[start_parameters.find(",") + 1:])
        self.endx = int(end_parameters[:end_parameters.find(",")])
        self.endy = int(end_parameters[end_parameters.find(",") + 1:])
        self.y = 0
        self.image_data[:] = len(self.image_data) // 4 * bytes([0,0,0,255])
        for idxy, line in enumerate(self.lines[:-4]):
            self.x = 0
            for idxx, px in enumerate(line[:-1]):
                pixel = format(int(px, 16), "04b")
                if pixel[0] == "1":
                    self.image_data[self.y*self.line_length + 4 * self.x:
                                    self.y*self.line_length
                                    + 4*(self.x + self.size)
                                    ] = self.size * color#gorna sciana
                for i in range(0, self.size - 1):
                    if pixel[3] == "1":
                        self.image_data[
                            (self.y + i) * self.line_length + 4 * self.x:
                            (self.y + i) * self.line_length + 4 * (self.x + 1)
                            ] = color#lewa sciana
                    if pixel[1] == "1":
                        self.image_data[
                            (self.y + i) * self.line_length
                            + 4 * (self.x + self.size - 1):
                            (self.y + i) * self.line_length
                            + 4 * (self.x + self.size)
                            ] = color#prawa sciana
                if pixel[2] == "1":
                    self.image_data[
                        (self.y+self.size - 1)*self.line_length + 4 * self.x:
                        (self.y + self.size - 1)*self.line_length
                        + 4*(self.x + self.size)
                        ] = self.size * color#dolna sciana
                    #print(f"Dolna scianka : {self.y+self.size - 1}")
                if pixel == "1111":
                    self.fourtytwo.append([self.x, self.y])
                    for i in range(2, self.size - 2):
                        self.image_data[
                            (self.y + i) * self.line_length
                            + 4 * (self.x + 2):
                            (self.y + i) * self.line_length
                            + 4 * (self.x + self.size - 2)
                            ] = (self.size - 4) * self.fourtytwo_color
                if idxx == self.startx and idxy == self.starty:
                    for i in range(2, self.size - 2):
                        self.image_data[
                            (self.y + i) * self.line_length
                            + 4 * (self.x + 2):
                            (self.y + i) * self.line_length
                            + 4 *(self.x + self.size - 2)
                            ] = (self.size - 4) * bytes([255, 255, 0, 255])
                if idxx == self.endx and idxy == self.endy:
                    for i in range(2, self.size - 2):
                        self.image_data[
                            (self.y + i) * self.line_length
                            + 4 * (self.x + 2):
                            (self.y + i) * self.line_length
                            + 4 * (self.x + self.size - 2)
                            ] = (self.size - 4) * bytes([255, 0, 255, 255])
                self.x += self.size - 1 #to not have double walls -1
            #break
            self.y += self.size - 1 #to not have double walls -1 
        print(self.x)
        print(f"Y equals: {self.y}")
        self.mlx.mlx_clear_window(self.ptr, self.window)
        self.mlx.mlx_put_image_to_window(self.ptr, self.window,
                                         self.img_ptr, 560, 140)

    def draw_borders(self, color=bytes([255, 255, 255, 255])):
        color = bytes(color)
        if color != self.color:
            self.i = 0
            self.z = 0
            self.color = color
        if self.i < self.x:
            self.image_data[
                4*self.i: 4 * (self.i + 1)
                ] = self.color
            self.image_data[
                (self.y) * self.line_length + 4*self.i:
                (self.y) * self.line_length + 4 * (self.i + 1)
                ] = self.color
        if self.z < self.y:
            self.image_data[
                self.z*self.line_length + 4*0:
                self.z*self.line_length + 4 * (0 + 1)
                ] = self.color
            self.image_data[
                self.z*self.line_length + 4*self.x:
                self.z*self.line_length + 4 * (self.x + 1)
                ] = self.color
        self.mlx.mlx_put_image_to_window(
            self.ptr, self.window, self.img_ptr, 560, 140)
        self.i += 1 #temporary x
        self.z += 1 #temporary
    
    def draw_fourtytwo(self, color=bytes([255, 255, 255, 255])):
        for coor in self.fourtytwo:
            self.fourtytwo_color = color
            y = coor[1]
            x = coor[0]
            for i in range(2, self.size - 2):
                        self.image_data[
                            (y + i) * self.line_length
                            + 4 * (x + 2):
                            (y + i) * self.line_length
                            + 4 * (x + self.size - 2)
                            ] = (self.size - 4) * color
        self.mlx.mlx_put_image_to_window(self.ptr, self.window,
                                         self.img_ptr, 560, 140)
        


    
    def draw_path(self, color = bytes([0, 255, 255, 255])):
        y = self.starty * (self.size - 1)
        x = self.startx * (self.size - 1)

        coords = {"N": (0, -1), "S": (0, 1), "W": (-1, 0), "E": (1, 0)}
        for path in self.lines[-1].strip():
            print(f"y = {y} x = {x}")
            y += coords[path][1] * (self.size - 1)
            x += coords[path][0] * (self.size - 1)
            print(f"y = {y} x = {x}")
            for i in range(3, self.size - 2):
                self.image_data[
                    (y + i) * self.line_length
                    + 4 * (x + 2):
                    (y + i) * self.line_length
                    + 4 * (x + self.size - 3)
                    ] = (self.size - 5) * color
            self.mlx.mlx_put_image_to_window(
            self.ptr, self.window, self.img_ptr, 560, 140)
