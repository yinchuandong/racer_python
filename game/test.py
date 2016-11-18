import pyglet


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2

game_window = pyglet.window.Window(640, 480)

pyglet.resource.path = ['images/sprites']
pyglet.resource.reindex()

palm_tree_img = pyglet.resource.image('palm_tree.png')
palm_tree = pyglet.sprite.Sprite(img=palm_tree_img)
palm_tree.scale = 0.4

@game_window.event
def on_draw():
    game_window.clear()
    palm_tree.draw()

if __name__ == '__main__':
    pyglet.app.run()
