import pygame


class InputBox:

    def __init__(self, x, y, w, h, puz, text=''):
        self.x, self.y = x, y
        self.cs = w  # cs: cell size
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (255, 255, 255)
        self.text = text
        self.txt_surface = pygame.font.Font(
            None, 32).render(text, True, self.color)
        self.active = False
        self.puz = puz

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = (30, 30, 255) if self.active else (255, 255, 255)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    if self.text != '':
                        self.puz[self.y // self.cs][self.x //
                                                    self.cs] = int(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) == 0:
                    if str(event.unicode).isdigit():
                        self.text += event.unicode
                elif len(self.text) == 1:
                    if str(event.unicode).isdigit():
                        self.text = ''
                        self.text += event.unicode
                # Re-render the text.
                self.txt_surface = pygame.font.Font(
                    None, 32).render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
