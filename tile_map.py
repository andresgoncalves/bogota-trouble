from PIL import Image, ImageTk
from typing import Any


class TileMap:
    def __init__(
        self,
        image_path: str,
        tile_width: int,
        tile_height: int,
        tile_data: dict[Any, tuple[int, int]]
    ):
        image = Image.open(image_path)

        self.tile_width: int = tile_width
        self.tile_height: int = tile_height

        self.tiles: dict[Any, ImageTk.PhotoImage] = dict()

        for name, (x, y) in tile_data.items():
            tk_tile = ImageTk.PhotoImage(self._load_tile(image, x, y))
            self.tiles[name] = tk_tile

        image.close()

    def get_tile(self, name: Any):
        return self.tiles.get(name)

    def _load_tile(self, image: Image.Image, x: int, y: int):
        tile = image.crop((
            x * self.tile_width,
            y * self.tile_height,
            (x + 1) * self.tile_width,
            (y + 1) * self.tile_height
        )).resize((96, 96))
        return tile
