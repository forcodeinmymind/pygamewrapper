from pygamegui.pygamewrapper.sprite import Sprite


class Widget(Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        
