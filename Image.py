from mlx import Mlx
from typing import Any


class Image():
    """Represents an image element displayed inside the MLX window.

    This class handles loading an image from file, storing its pixel data,
    and rendering or removing it from the window. It is mainly used as a
    UI element (e.g., buttons, icons).

    Attributes:
        ptr (Any): Pointer to the MLX instance.
        window (Any): Window where the image is displayed.
        mlx (Mlx): MLX wrapper instance.
        img (str): Path to the image file.
        x (int): X coordinate of the image position.
        y (int): Y coordinate of the image position.
        show (bool): Determines whether the image is visible.
        original_image: Pointer to the loaded image.
        color_data (bytes): Raw pixel data of the image.
        size_line (int): Number of bytes per row in the image.
    """

    def __init__(self, ptr: Any, window: Any, mlx: Mlx, x: int = 1600,
                 y: int = 800,
                 img: str = "images/image.png", show: bool = True) -> None:
        """Initialize an image object and load it into memory.

        Args:
            ptr (Any): Pointer returned by MLX initialization.
            window (Any): Window where the image will be displayed.
            mlx (Mlx): MLX wrapper instance.
            x (int, optional): X position of the image. Defaults to 1600.
            y (int, optional): Y position of the image. Defaults to 800.
            img (str, optional): Path to the image file. Defaults to
            "images/image.png".
            show (bool, optional): Whether the image should
            be visible initially.
                Defaults to True.

        Returns:
            None
        """
        self.img_ptr = mlx.mlx_new_image(ptr, 100, 100)
        self.mlx_img_data = mlx.mlx_get_data_addr(self.img_ptr)
        self.img_data = self.mlx_img_data[0]
        img_array = mlx.mlx_png_file_to_image(ptr, img)

        self.original_image = mlx.mlx_png_file_to_image(ptr, img)[0]

        self.ptr = ptr
        self.img = img
        self.mlx = mlx
        self.window = window

        self.img_data = mlx.mlx_get_data_addr(img_array[0])
        self.color_data = bytes(self.img_data[0])
        self.size_line = self.img_data[2]
        self.x = x
        self.y = y

        self.image_data_ptr = img_array[0]

        self.show = show

    def show_button(self) -> None:
        """Display the image in the window if visibility is enabled.

        If `self.show` is True, the image is drawn at its current position.
        Otherwise, the image is removed from the screen.

        Returns:
            None
        """
        if self.show is True:
            self.mlx.mlx_png_file_to_image(self.ptr, self.img)
            self.mlx.mlx_put_image_to_window(self.ptr, self.window,
                                             self.original_image,
                                             self.x, self.y)
        else:
            self.erase_button()

    def erase_button(self) -> None:
        """Remove the image from the window by overwriting it.

        This method fills the image buffer with a solid color (black)
        and redraws it, effectively erasing the previous image.

        Returns:
            None
        """
        buffer = self.img_data[0]
        buffer[:] = bytes([0, 0, 0, 255]) * (len(self.color_data) // 4)
        self.mlx.mlx_put_image_to_window(self.ptr, self.window,
                                         self.image_data_ptr, self.x, self.y)
