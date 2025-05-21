import pygame

def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft = top_left).center)
    win.blit(rotated_image, new_rect.topleft)

def blit_text_center(win, font, text):
    render = font.render(text, 1, (0, 0, 0))
    win.blit(render, (win.get_width() / 2 - render.get_width() / 2, win.get_height() / 2 - render.get_height() / 2))



[(226, 72), (520, 94), (655, 175), (586, 204), (440, 325), (299, 315), (177, 320), (160, 457), (643, 647), (485, 675), (199, 648), (40, 415)]