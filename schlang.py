
def draw_schlang(mlx, window, ptr):
	for i in range(1, 51):
        mlx.mlx_pixel_put(ptr, window, 374 + i, 200, 0xFFFFFF11)  #bialy
        mlx.mlx_pixel_put(ptr, window, 375, 200 + i, 0xFFFFFF11)  #bialy
        mlx.mlx_pixel_put(ptr, window, 425, 200 + i, 0xFFFFFF11)
        mlx.mlx_pixel_put(ptr, window, 400, 200 + i, 0xFFFFFF11)
        mlx.mlx_pixel_put(ptr, window, 374 + i, 250, 0xFFFFFF11)
        

    for i in range(1, 200):
        mlx.mlx_pixel_put(ptr, window, 375, 250 + i, 0xFFFFFF11)  #bialy
        mlx.mlx_pixel_put(ptr, window, 425, 250 + i, 0xFFFFFF11)
        
    for i in range(1, 101):
        mlx.mlx_pixel_put(ptr, window, 375 - i, 450, 0xFFFFFF11)
        mlx.mlx_pixel_put(ptr, window, 425 + i, 450, 0xFFFFFF11)
        
    for i in range(1, 101):
        mlx.mlx_pixel_put(ptr, window, 275, 450 + i, 0xFFFFFF11)
        mlx.mlx_pixel_put(ptr, window, 525, 450 + i, 0xFFFFFF11)
        
    for i in range(1, 101):
        mlx.mlx_pixel_put(ptr, window, 275 + i, 550, 0xFFFFFF11)
        mlx.mlx_pixel_put(ptr, window, 525 - i, 550, 0xFFFFFF11)
        
    for i in range(1, 101):
        mlx.mlx_pixel_put(ptr, window, 375, 550 - i, 0xFFFFFF11)
        mlx.mlx_pixel_put(ptr, window, 425, 550 - i, 0xFFFFFF11)
  
            
