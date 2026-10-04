

class Menu:

    def __init__(self, window, menu_img, images,
                 selected_images=None) -> None:
        self.window = window
        self.menu_img = menu_img
        self.images = images
        self.selected_images = selected_images

    def test(self):
        ...
