import json
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk
from typing import Any

from tile_map import TileMap
from dijkstra import dijkstra, get_dijkstra_route, get_dijkstra_distance, M


def node_to_corner(node: int):
    return node % 6, node // 6


def corner_to_node(x: int, y: int):
    return y * 6 + x


def full_corner_to_node(x: int, y: int):
    return corner_to_node(x - 10, y - 50)


def node_to_full_corner(node: int):
    x, y = node_to_corner(node)
    return x + 10, y + 50


def build_matrix():
    matrix = [[M for x in range(6 * 6)] for y in range(6 * 6)]
    for node in range(6 * 6):
        x, y = node_to_corner(node)
        full_x, full_y = node_to_full_corner(node)
        x_distance = 8 if full_y == 51 else 4
        y_distance = 6 if 12 <= full_x <= 14 else 4
        matrix[node][node] = 0
        if x > 0:
            matrix[node][corner_to_node(x - 1, y)] = x_distance
        if x < 5:
            matrix[node][corner_to_node(x + 1, y)] = x_distance
        if y > 0:
            matrix[node][corner_to_node(x, y - 1)] = y_distance
        if y < 5:
            matrix[node][corner_to_node(x, y + 1)] = y_distance
    return matrix


def draw_map(canvas: tk.Canvas,
             tile_width: int,
             tile_height: int,
             vertical_offset: int,
             horizontal_offset: int,
             map_data: list[list[Any]],
             tile_map: TileMap
             ):
    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            image = tile_map.get_tile(tile)
            canvas.create_image(
                horizontal_offset + x * tile_width,
                vertical_offset + y * tile_height,
                image=image,
                anchor="nw")


def draw_axes(canvas: tk.Canvas,
              tile_width: int,
              tile_height: int,
              x_axis_start: int,
              x_axis_end: int,
              y_axis_start: int,
              y_axis_end: int,
              vertical_offset: int,
              horizontal_offset: int,
              ):
    x_offset = horizontal_offset + 0.5 * tile_width
    y_offset = vertical_offset + 0.5 * tile_height
    for x in range(x_axis_start, x_axis_end - 1, 1 if x_axis_end > x_axis_start else -1):
        canvas.create_text(
            x_offset,
            0.5 * vertical_offset,
            text=f"{x}",
            font=("Arial", 16),
            fill="white",
            anchor="center")
        x_offset += tile_width
    for y in range(y_axis_start, y_axis_end - 1, 1 if y_axis_end > y_axis_start else -1):
        canvas.create_text(
            0.5 * horizontal_offset,
            y_offset,
            text=f"{y}",
            font=("Arial", 16),
            fill="white",
            anchor="center")
        y_offset += tile_height


def draw_path(
    canvas: tk.Canvas,
    route: list[tuple[int, int]],
    tile_width: int,
    tile_height: int,
    vertical_offset: int,
    horizontal_offset: int,
    fill: str = "white"
):
    if len(route) > 1:
        canvas.create_line(
            *[
                (
                    horizontal_offset + (5 - x + 0.5) * tile_width,
                    vertical_offset + (5 - y + 0.5) * tile_height
                )
                for x, y in route
            ],
            fill=fill,
            arrow="last",
            joinstyle="round",
            width=4,
        )
    else:
        x, y = route[0]
        canvas.create_oval(
            horizontal_offset + (5 - x + 0.45) * tile_width,
            vertical_offset + (5 - y + 0.45) * tile_height,
            horizontal_offset + (5 - x + 0.55) * tile_width,
            vertical_offset + (5 - y + 0.55) * tile_height,
            fill=fill,
            outline=""
        )


def draw_sprite(
    canvas: tk.Canvas,
    image: ImageTk.PhotoImage,
    position: tuple[int, int],
    tile_width: int,
    tile_height: int,
    vertical_offset: int,
    horizontal_offset: int,
    fill: str = "white"
):
    canvas.create_image(
        horizontal_offset + (5 - position[0]) * tile_width,
        vertical_offset + (5 - position[1]) * tile_height,
        image=image,
        anchor="nw")


def simular(matrix: list[list[int]],
            destination: int,
            javiers_house: int,
            andreinas_house: int,
            root: tk.Tk,
            tile_width: int,
            tile_height: int,
            vertical_offset: int,
            horizontal_offset: int,
            map_data: list[list[Any]],
            tile_map: TileMap,
            sprite_map: TileMap
            ):
    javiers_table = dijkstra(javiers_house, matrix, handicap=0)
    javiers_route = [node_to_corner(node)
                     for node in get_dijkstra_route(javiers_table, destination)]
    javiers_time = get_dijkstra_distance(javiers_table, destination)

    andreinas_table = dijkstra(andreinas_house, matrix, handicap=2)
    andreinas_route = [node_to_corner(node)
                       for node in get_dijkstra_route(andreinas_table, destination)]
    andreinas_time = get_dijkstra_distance(andreinas_table, destination)

    canvas = tk.Canvas(
        root,
        width=horizontal_offset + tile_width * len(map_data[0]),
        height=vertical_offset + tile_height * len(map_data)
    )
    draw_map(
        canvas=canvas,
        tile_width=tile_width,
        tile_height=tile_height,
        horizontal_offset=horizontal_offset,
        vertical_offset=vertical_offset,
        map_data=map_data,
        tile_map=tile_map
    )
    draw_axes(
        canvas=canvas,
        tile_width=tile_width,
        tile_height=tile_height,
        x_axis_start=15,
        x_axis_end=10,
        y_axis_start=55,
        y_axis_end=50,
        horizontal_offset=horizontal_offset,
        vertical_offset=vertical_offset,
    )
    canvas.pack()

    draw_path(
        canvas=canvas,
        route=javiers_route,
        tile_width=tile_width,
        tile_height=tile_height,
        horizontal_offset=horizontal_offset - 4,
        vertical_offset=vertical_offset - 4,
        fill="skyblue"
    )

    draw_path(
        canvas=canvas,
        route=andreinas_route,
        tile_width=tile_width,
        tile_height=tile_height,
        horizontal_offset=horizontal_offset + 8,
        vertical_offset=vertical_offset + 8,
        fill="pink"
    )

    draw_sprite(canvas=canvas,
                image=sprite_map.get_tile("male_south1"),
                position=node_to_corner(javiers_house),
                tile_width=tile_width,
                tile_height=tile_height,
                horizontal_offset=horizontal_offset,
                vertical_offset=vertical_offset,)

    draw_sprite(canvas=canvas,
                image=sprite_map.get_tile("female_south1"),
                position=node_to_corner(andreinas_house),
                tile_width=tile_width,
                tile_height=tile_height,
                horizontal_offset=horizontal_offset,
                vertical_offset=vertical_offset,)

    messagebox.showinfo("Resultado", f"Javier debe salir de su casa {andreinas_time - javiers_time} minutos después que Andreina"
                        if javiers_time < andreinas_time else
                        f"Andreina debe salir de su casa {
                            javiers_time - andreinas_time} minutos después que Javier"
                        )


def main():

    # Calculate routes

    javiers_house = full_corner_to_node(14, 54)
    andreinas_house = full_corner_to_node(13, 52)

    the_darkness_club = full_corner_to_node(14, 50)
    la_pasion_bar = full_corner_to_node(11, 54)
    rolita_beerhouse = full_corner_to_node(12, 50)

    matrix = build_matrix()

    # Create the main window
    root = tk.Tk()
    root.title("Bogota Trouble")

    # Create a frame to hold the buttons
    title_frame = tk.Frame(root)
    title_frame.pack(pady=10)

    title_text = tk.Label(title_frame, text="Seleccione un local de destino:")
    title_text.pack()

    button_frame = tk.Frame(title_frame)
    button1 = tk.Button(button_frame, text="Discoteca The Darkness",
                        command=lambda: simulate(the_darkness_club))
    button1.pack(side=tk.LEFT, padx=5)
    button2 = tk.Button(button_frame, text="Bar La Pasión",
                        command=lambda: simulate(la_pasion_bar))
    button2.pack(side=tk.LEFT, padx=5)
    button3 = tk.Button(button_frame, text="Cervecería Rolita",
                        command=lambda: simulate(rolita_beerhouse))
    button3.pack(side=tk.LEFT, padx=5)
    button_frame.pack(anchor=tk.CENTER)

    # Load resources

    map_data_path = "./assets/map.json"
    map_image_path = "./assets/map.png"
    sprite_data_path = "./assets/sprite.json"
    sprite_image_path = "./assets/sprite.png"

    with open(map_data_path) as file:
        data = json.load(file)

    tile_width: int = data["tileSize"]["width"]
    tile_height: int = data["tileSize"]["height"]
    vertical_offset = 32
    horizontal_offset = 32

    tile_data: dict[Any, tuple[int, int]] = data["tiles"]
    map_data: list[list[Any]] = data["map"]

    tile_map = TileMap(
        image_path=map_image_path,
        tile_width=tile_width,
        tile_height=tile_height,
        tile_data=tile_data
    )

    with open(sprite_data_path) as file:
        data = json.load(file)

    sprite_width: int = data["spriteSize"]["width"]
    sprite_height: int = data["spriteSize"]["height"]
    sprite_data: dict[Any, tuple[int, int]] = data["sprites"]

    sprite_map = TileMap(
        image_path=sprite_image_path,
        tile_width=sprite_width,
        tile_height=sprite_height,
        tile_data=sprite_data
    )

    canvas = tk.Canvas(
        root,
        width=horizontal_offset + tile_width * len(map_data[0]),
        height=vertical_offset + tile_height * len(map_data)
    )

    draw_map(
        canvas=canvas,
        tile_width=tile_width,
        tile_height=tile_height,
        horizontal_offset=horizontal_offset,
        vertical_offset=vertical_offset,
        map_data=map_data,
        tile_map=tile_map
    )
    draw_axes(
        canvas=canvas,
        tile_width=tile_width,
        tile_height=tile_height,
        x_axis_start=15,
        x_axis_end=10,
        y_axis_start=55,
        y_axis_end=50,
        horizontal_offset=horizontal_offset,
        vertical_offset=vertical_offset,
    )

    canvas.pack()

    def simulate(destination: int):
        javiers_table = dijkstra(javiers_house, matrix, handicap=0)
        javiers_route = [node_to_corner(node)
                         for node in get_dijkstra_route(javiers_table, destination)]
        javiers_time = get_dijkstra_distance(javiers_table, destination)

        andreinas_table = dijkstra(andreinas_house, matrix, handicap=2)
        andreinas_route = [node_to_corner(node)
                           for node in get_dijkstra_route(andreinas_table, destination)]
        andreinas_time = get_dijkstra_distance(andreinas_table, destination)

        canvas.delete("all")

        draw_map(
            canvas=canvas,
            tile_width=tile_width,
            tile_height=tile_height,
            horizontal_offset=horizontal_offset,
            vertical_offset=vertical_offset,
            map_data=map_data,
            tile_map=tile_map
        )
        draw_axes(
            canvas=canvas,
            tile_width=tile_width,
            tile_height=tile_height,
            x_axis_start=15,
            x_axis_end=10,
            y_axis_start=55,
            y_axis_end=50,
            horizontal_offset=horizontal_offset,
            vertical_offset=vertical_offset,
        )

        draw_path(
            canvas=canvas,
            route=javiers_route,
            tile_width=tile_width,
            tile_height=tile_height,
            horizontal_offset=horizontal_offset - 4,
            vertical_offset=vertical_offset - 4,
            fill="skyblue"
        )

        draw_path(
            canvas=canvas,
            route=andreinas_route,
            tile_width=tile_width,
            tile_height=tile_height,
            horizontal_offset=horizontal_offset + 8,
            vertical_offset=vertical_offset + 8,
            fill="pink"
        )

        draw_sprite(canvas=canvas,
                    image=sprite_map.get_tile("male_south1"),
                    position=node_to_corner(javiers_house),
                    tile_width=tile_width,
                    tile_height=tile_height,
                    horizontal_offset=horizontal_offset,
                    vertical_offset=vertical_offset,)

        draw_sprite(canvas=canvas,
                    image=sprite_map.get_tile("female_south1"),
                    position=node_to_corner(andreinas_house),
                    tile_width=tile_width,
                    tile_height=tile_height,
                    horizontal_offset=horizontal_offset,
                    vertical_offset=vertical_offset,)

        canvas.update()

        messagebox.showinfo("Resultado", (f"Javier debe salir de su casa {andreinas_time - javiers_time} minutos después que Andreina."
                            if javiers_time < andreinas_time else
                            f"Andreina debe salir de su casa \
                                {javiers_time - andreinas_time} minutos después que Javier")
                            + f"\nJavier demora {javiers_time} minutos y Andreina demora {andreinas_time} minutos."
                            )

    root.attributes("-topmost", True)
    root.lift()
    root.attributes("-topmost", False)

    root.mainloop()


if __name__ == "__main__":
    main()
