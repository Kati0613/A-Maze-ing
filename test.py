from mlx import Mlx

def close(param):
    




def main():
    mlx = Mlx()
    ptr = mlx.mlx_init()

    window = mlx.mlx_new_window(ptr, 100, 100, "whoores")
    rzeczy = {
        "ptr": mlx,
        "window": window,
    }
    
    mlx.mlx_loop(ptr)

if __name__ == "__main__":
    main()
