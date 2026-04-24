from typing import Any
from mlx import Mlx


class Button():
    """Represents a simple clickable UI button with text inside.

    This class creates a rectangular button rendered as an image in the MLX
    window. It supports displaying text, updating numeric values, and
    refreshing
    its appearance.

    Attributes:
        ptr (Any): Pointer returned by MLX initialization.
        mlx (Mlx): MLX wrapper used for rendering.
        window (Any): Window where the button is displayed.
        x (int): X coordinate of the button position.
        y (int): Y coordinate of the button position.
        width (int): Width of the button in pixels.
        height (int): Height of the button in pixels.
        word (str): Text currently displayed on the button.
        btn_ptr: Pointer to the button image.
        image_data (bytes): Raw pixel buffer of the button.
    """

    def __init__(self, ptr: Any, window: Any, mlx: Mlx, x: int = 1600,
                 y: int = 800,
                 width: int = 300, height: int = 300,
                 word: int | None = None) -> None:
        """Initialize a button with position, size, and optional text.

        The button is drawn immediately after creation with a default
        background color and optional centered text.

        Args:
            ptr (Any): Pointer returned by MLX initialization.
            window (Any): Window where the button will be displayed.
            mlx (Mlx): MLX wrapper instance.
            x (int, optional): X position of the button. Defaults to 1600.
            y (int, optional): Y position of the button. Defaults to 800.
            width (int, optional): Button width in pixels. Defaults to 300.
            height (int, optional): Button height in pixels. Defaults to 300.
            word (int | None, optional): Initial numeric value displayed
                on the button. Defaults to None.

        Returns:
            None
        """
        self.ptr = ptr
        self.mlx = mlx
        self.window = window

        self.x = x
        self.y = y

        self.word = str(word)

        self.btn_ptr = self.mlx.mlx_new_image(self.ptr, width, height)
        self.image_data = self.mlx.mlx_get_data_addr(self.btn_ptr)[0]
        self.width = width
        self.height = height
        self.image_data[:] = (
            len(self.image_data) // 4 * bytes([153, 204, 255, 255])
        )

        self.mlx.mlx_put_image_to_window(self.ptr, self.window,
                                         self.btn_ptr, x, y)
        if str is not None:
            self.put_str()

    def put_str(self) -> None:
        """Render the button text centered inside the button.

        The method clears the button background and redraws the current
        text (`self.word`) in the center.

        Returns:
            None
        """
        self.image_data[:] = (
            len(self.image_data) // 4 * bytes([153, 204, 255, 255])
        )
        self.mlx.mlx_put_image_to_window(self.ptr, self.window,
                                         self.btn_ptr, self.x, self.y)
        self.mlx.mlx_string_put(self.ptr, self.window,
                                self.x + self.width // 2 - 5 * len(self.word),
                                self.y + self.height // 2 - 10,
                                0x000000, self.word)

    def update_int(self, sub: int,
                   maximum: int = 103, minimum: int = 2) -> int:
        """Update the numeric value displayed on the button.

        The value is incremented or decremented by `sub`, but always stays
        within the given `[minimum, maximum]` range. The updated value is
        immediately rendered.

        Args:
            sub (int): Value to add (or subtract if negative).
            maximum (int, optional): Maximum allowed value. Defaults to 103.
            minimum (int, optional): Minimum allowed value. Defaults to 2.

        Returns:
            int: The updated numeric value after applying constraints.
        """
        counter = min(max(int(self.word) + sub, minimum), maximum)
        self.word = str(counter)
        self.mlx.mlx_put_image_to_window(self.ptr, self.window,
                                         self.btn_ptr, self.x, self.y)
        self.mlx.mlx_string_put(self.ptr, self.window,
                                self.x + self.width // 2 - 5 * len(self.word),
                                self.y + self.height // 2 - 10, 0x000000,
                                self.word)
        return counter

    def refresh(self) -> None:
        """Redraw the button and its current text.

        This method is useful when the button needs to be re-rendered without
        changing its value.

        Returns:
            None
        """
        self.mlx.mlx_put_image_to_window(self.ptr, self.window, self.btn_ptr,
                                         self.x, self.y)
        if str is not None:
            self.put_str()
