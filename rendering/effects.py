import pygame


def generate_shadow(image, shadow_offset=(10, 10), shadow_color=(0, 0, 0, 100)):
    # Create a shadow
    shadow = image.copy()
    shadow.fill(shadow_color, special_flags=pygame.BLEND_RGBA_MULT)

    # Returns shadow and its offset
    return shadow, shadow_offset

def draw_multiline_text(text, x, y, font,color, screen, padding):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        line_surface = font.render(line, True, color)
        screen.blit(line_surface, (x, y + padding*i))  # 40 is line height