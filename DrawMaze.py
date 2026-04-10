from mlx import Mlx

class Maze():

    def __init__(self, mlx, ptr, window, output, width, height):
        self.mlx = mlx
        self.window = window
        self.ptr = ptr
        self.fourtytwo = []
        self.fourtytwo_color = bytes([0, 0, 0, 255])
 
        self.x = 0
        self.y = 0
        self.i = 0
        self.z = 0

        self.color = bytes([255, 255, 255, 255])

        self.output = output
        self.size = 36
    
    def draw_maze(self, color=bytes([255, 255, 255, 255]), width=21, height=21):
        self.width = width
        self.height = height
        print(f"\n MAZE WIDTH: {self.width} \n MAZE HEIGHT: {self.height}")
        print(f"LENGTH OF OUTPUT {len(self.output)}")
        print(f"MAZE: {self.output}")
        #self.output = "1111111111111111111111111111111111111111111111111111111111111111"
        self.fourtytwo = []

       
        
        cell = self.size - 1
        img_w = self.width * cell + 1
        img_h = self.height * cell + 1

        self.img_ptr = self.mlx.mlx_new_image(self.ptr, img_w, img_h)
        self.mlx_img_data = self.mlx.mlx_get_data_addr(self.img_ptr)
        self.image_data = self.mlx_img_data[0]
        self.line_length = self.mlx_img_data[2]

        #print(self.line_length)
        
        # Szybkie czyszczenie - używamy bytes o tej samej długości
        self.image_data[:] = len(self.image_data) // 4 * bytes([0,0,0,255])
        
        x, y, j = 0, 0, 0

        while y < self.height:
            print(f"\n X: {x} Y: {y}")
            pixel = self.output[j:j+4]
            print(f"PIXEL: {pixel}")
            if pixel[3] == "1": # gorna
                start = y * cell * self.line_length + 4 * x * cell
                end = y * cell * self.line_length + (cell * x + cell + 1) * 4
                self.image_data[
                    start: end
                     ] = self.size * color
            if pixel[1] == "1":
                start = (y + 1) * cell * self.line_length + x * cell * 4
                end = (y + 1) * cell * self.line_length + (cell * x + cell + 1) * 4
                self.image_data[
                    start: end
                     ] = self.size * color
            if pixel[0] == "1":
                for i in range(0, cell):
                    start = (y * cell + i) * self.line_length + x * cell * 4
                    #print(f"START lewa sciana {start}")
                    end = (y * cell + i) * self.line_length + x*cell * 4 + 4
                    self.image_data[
                            start: end
                            ] = color
            if pixel[2] == "1":
                for i in range(0, cell):
                    start = (y * cell + i) * self.line_length + (x + 1) * 4 * cell
                    end = (y * cell + i) * self.line_length + (x + 1) * 4 * cell + 4
                    self.image_data[
                            start: end
                            ] = color
            if x == self.width - 1:
                x = -1
                y += 1
            j += 4
            x += 1
            #print(f"\n X: {x} Y: {y}")

        self.mlx.mlx_put_image_to_window(self.ptr, self.window, self.img_ptr, 560, 140)
    
    def draw_fourtytwo(self, color=bytes([255, 255, 255, 255])):
        cell = self.size - 1

        for coor in self.fourtytwo:
            x, y = coor

            base_y = y * cell * self.line_length
            base_x = x * cell * 4

            for i in range(2, cell - 2):
                row = base_y + i * self.line_length

                start = row + base_x + 2 * 4
                end = row + base_x + (cell - 2) * 4

                self.image_data[start:end] = (cell - 4) * color

        self.mlx.mlx_put_image_to_window(self.ptr, self.window,
                                         self.img_ptr, 560, 140)

    def draw_path(self, color = bytes([0, 255, 255, 255])):
        y = self.starty * (self.size - 1)
        x = self.startx * (self.size - 1)

        coords = {"N": (0, -1), "S": (0, 1), "W": (-1, 0), "E": (1, 0)}
        for path in self.lines[-1].strip():
            y += coords[path][1] * (self.size - 1)
            x += coords[path][0] * (self.size - 1)
            for i in range(3, self.size - 2):
                self.image_data[
                    (y + i) * self.line_length
                    + 4 * (x + 2):
                    (y + i) * self.line_length
                    + 4 * (x + self.size - 3)
                    ] = (self.size - 5) * color
            self.mlx.mlx_put_image_to_window(
            self.ptr, self.window, self.img_ptr, 560, 140)
