from constants import Tile_Size, Tile_Color, Window_Size, button_width, slot_width, slot_length, Border_Width
from datetime import datetime
import pygame
import os
import csv


class Menu:
    def __init__(self, buttons, center=True, main_menu=False, text=None):
        # Creates Buttons
        self.buttons = []
        num_of_buttons = len(buttons)
        buttons_spacing = (button_width // 3) + button_width
        width = (buttons_spacing * num_of_buttons) // 2

        # Determines weather buttons are at the center of bottom of the window
        if center:
            button_location = Window_Size // 2
        else:
            button_location = (Window_Size // 3) * 2

        for i in range(num_of_buttons):
            pos = ((Window_Size // 2) - ((Tile_Size * 3) // 2), (button_location - width + (i * buttons_spacing)))
            self.buttons.append(Button(buttons[i], pos))

        # Creates the header image of the main menu
        if main_menu:
            Img = pygame.image.load('Chess_Pieces_Sprite.png')
            piece_size = Window_Size // 5
            Img = pygame.transform.scale(Img, (piece_size * 6, piece_size * 2))

            self.header = pygame.Surface((Window_Size, Window_Size // 5))
            self.header.fill((255, 255, 255))

            font = pygame.font.SysFont('arial', Window_Size // 5, bold=True)
            textsurface = font.render('CHESS', False, Tile_Color)

            width = textsurface.get_size()[0]

            side = (Window_Size // 2) - (width // 2)

            self.header.blit(textsurface, (side, 0))

            self.header.blit(Img, ((side // 2) - (piece_size // 2), 0), (0, 0, piece_size, piece_size))
            self.header.blit(Img, (Window_Size - (side // 2) - (piece_size // 2), 0),
                             (0, piece_size, piece_size, piece_size))

            self.title = 0

        # Creates header text
        elif text != None:
            self.header = pygame.Surface((Window_Size, (Window_Size // 16) * len(text)))
            self.header.fill((255, 255, 255))
            font = pygame.font.SysFont('arial', Window_Size // 20, bold=True)

            for i in range(len(text)):
                textsurface = font.render(text[i], False, Tile_Color)
                size = textsurface.get_size()
                self.header.blit(textsurface, ((Window_Size // 2) - (size[0] // 2), (Window_Size // 18) * i))

            self.title = 1

        else:
            self.title = 2

    def check_button_press(self, clicked):
        # Checks if the player clicked on of the buttons and if yes returns which one
        if clicked:
            for button in self.buttons:
                if button.mouse_on_button():
                    return button.text

    def draw(self, screen):
        screen.fill((255, 255, 255))
        for button in self.buttons:
            button.draw(screen)

        if self.title == 0:
            screen.blit(self.header, (0, (Window_Size // 4) - (Window_Size // 10)))

        elif self.title == 1:
            size = self.header.get_size()
            screen.blit(self.header, (0, (Window_Size // 3) - (size[1] // 2)))


class Button:
    def __init__(self, text, pos, length=3):
        # Creates the images of the button
        self.pos = pos
        self.text = text
        self.length = Tile_Size * length

        border_width = button_width // 10
        font = pygame.font.SysFont('arial', button_width - (border_width * 4), bold=False)

        self.mouse_not_over_button_image = pygame.Surface((self.length, button_width))
        self.mouse_not_over_button_image.fill((255, 150, 0))
        pygame.draw.rect(self.mouse_not_over_button_image, Tile_Color, (
            border_width, border_width, self.length - (border_width * 2), button_width - (border_width * 2)))
        textsurface = font.render(text, False, (255, 150, 0))
        size = textsurface.get_size()
        self.mouse_not_over_button_image.blit(textsurface, (
            (self.length // 2) - (size[0] // 2), (button_width // 2) - (size[1] // 2)))

        self.mouse_over_button_image = pygame.Surface((self.length, button_width))
        self.mouse_over_button_image.fill((255, 255, 0))
        pygame.draw.rect(self.mouse_over_button_image, Tile_Color, (
            border_width, border_width, self.length - (border_width * 2), button_width - (border_width * 2)))
        textsurface = font.render(text, False, (255, 255, 0))
        size = textsurface.get_size()
        self.mouse_over_button_image.blit(textsurface, (
            (self.length // 2) - (size[0] // 2), (button_width // 2) - (size[1] // 2)))

    def mouse_on_button(self):
        # Checks of the cursor is on the button
        cursor_pos = pygame.mouse.get_pos()

        if self.pos[0] < cursor_pos[0] < self.pos[0] + self.length and \
                self.pos[1] < cursor_pos[1] < self.pos[1] + button_width:
            return True
        else:
            return False

    def draw(self, screen):
        if self.mouse_on_button():
            screen.blit(self.mouse_over_button_image, self.pos)
        else:
            screen.blit(self.mouse_not_over_button_image, self.pos)


class File_Menu:
    def __init__(self):
        self.save_slots = []
        self.buttons_save = []
        self.buttons_load = []
        self.mode = None
        self.selected_slot = None

        self.button_bar_width = button_width + (button_width // 2)

        button_spacing = (Window_Size - (Tile_Size * 6)) // 4

        buttons_save = ('Save', 'Delete', 'Back')
        buttons_load = ('Load', 'Delete', 'Back')

        for i in range(3):
            self.buttons_save.append(Button(buttons_save[i], (
                button_spacing + i * (Tile_Size * 2 + button_spacing),
                Window_Size - button_width - (button_width // 4)),
                                       length=2))
            self.buttons_load.append(Button(buttons_load[i], (
                button_spacing + i * (Tile_Size * 2 + button_spacing),
                Window_Size - button_width - (button_width // 4)),
                                            length=2))

        slot_x_border = (Window_Size - (Tile_Size * 8)) // 3
        slot_y_border = ((Window_Size - self.button_bar_width) - (slot_width * 3)) // 3
        slot_spacing = slot_x_border + slot_width

        for i in range(3):
            self.save_slots.append(Save_Slot((slot_x_border, slot_y_border + i * slot_spacing)))
            self.save_slots.append(Save_Slot(((slot_x_border * 2) + (Tile_Size * 4), slot_y_border + i * slot_spacing)))

        self.update_slots()

    def file_path(self):
        if self.selected_slot is not None:
            return 'SaveFiles/SaveData' + str(self.save_slots.index(self.selected_slot)) + '.csv'

    def check_click(self, clicked):
        # Checks if the player clicked on of the buttons and if yes returns which one
        if clicked:
            if self.mode == 'Save':
                buttons = self.buttons_save
            else:
                buttons = self.buttons_load

            for button in buttons:
                if button.mouse_on_button():
                    return button.text

            for slot in self.save_slots:
                if slot.mouse_on_slot():
                    if self.selected_slot is not None:
                        self.selected_slot.selected = False

                    if self.selected_slot == slot:
                        self.selected_slot = None
                        slot.selected = False
                    else:
                        slot.selected = True
                        self.selected_slot = slot

                    return None

    def update_slots(self):
        files = os.listdir('SaveFiles')
        i = 0
        for slot in self.save_slots:
            file_names = ('SaveData' + str(i) + '.csv', 'SaveImage' + str(i) + '.jpg')

            if file_names[0] in files and file_names[1] in files:
                slot.empty = False
                with open('SaveFiles/' + file_names[0], 'r') as csvfile:
                    row = next(csv.reader(csvfile))

                font = pygame.font.SysFont('arial', slot_width // 6, bold=True)
                slot.date = font.render(row[2], True, Tile_Color)
                slot.time = font.render(row[3], True, Tile_Color)
                slot.load_image('SaveFiles/' + file_names[1])

            else:
                slot.empty = True

            i += 1

    def delete_file(self):
        if self.selected_slot is not None:
            i = self.save_slots.index(self.selected_slot)
            file_names = ('SaveFiles/SaveData' + str(i) + '.csv', 'SaveFiles/SaveImage' + str(i) + '.jpg')

            for name in file_names:
                if os.path.exists(name):
                    os.remove(name)

            self.selected_slot.empty = True
            self.selected_slot.selected = False
            self.selected_slot = None

    def save_game(self, game, overwrite=False):
        if self.selected_slot is not None:
            i = self.save_slots.index(self.selected_slot)
            files = os.listdir('SaveFiles')
            file_names = ('SaveData' + str(i) + '.csv', 'SaveImage' + str(i) + '.jpg')
            if file_names[0] in files and file_names[1] in files and not overwrite:
                return 'Already_Exists'

            with open('SaveFiles/' + file_names[0], 'w') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',')

                now = datetime.now()

                filewriter.writerow([game.turn, str(game.vs_computer), now.strftime("%d/%m/%Y"),
                                     now.strftime("%H:%M:%S")])

                for piece in game.tiles.values():
                    if piece is not None:
                        filewriter.writerow([piece.type, piece.tile[0], piece.tile[1], piece.color, str(piece.moved),
                                             str(piece.en_passant_target)])

            image = pygame.Surface((Window_Size, Window_Size))
            game.draw(image, True)
            sub = image.subsurface(pygame.Rect(Border_Width, Border_Width, Tile_Size * 8, Tile_Size * 8))
            pygame.image.save(sub, 'SaveFiles/' + file_names[1])

            self.selected_slot.selected = False
            self.selected_slot = None

            self.update_slots()

    def draw(self, screen):
        screen.fill((255, 255, 255))

        for slot in self.save_slots:
            slot.draw(screen)

        if self.mode == 'Save':
            buttons = self.buttons_save
        else:
            buttons = self.buttons_load

        for button in buttons:
            button.draw(screen)


class Save_Slot:
    def __init__(self, pos):
        self.selected = False
        self.empty = True
        self.pos = pos
        self.screenshot = None
        self.date = None
        self.time = None
        self.border_width = slot_width // 20

        font = pygame.font.SysFont('arial', slot_width // 6, bold=True)
        self.empty_text = font.render('EMPTY', True, Tile_Color)

        self.image_not_selected = pygame.Surface((slot_length, slot_width))
        self.image_not_selected.fill(Tile_Color)
        pygame.draw.rect(self.image_not_selected, (255, 255, 255), (
            self.border_width, self.border_width, slot_length - (self.border_width * 2),
            slot_width - (self.border_width * 2)))

        self.image_selected = pygame.Surface((slot_length, slot_width))
        self.image_selected.fill((255, 255, 0))
        pygame.draw.rect(self.image_selected, (255, 255, 255), (
            self.border_width, self.border_width, slot_length - (self.border_width * 2),
            slot_width - (self.border_width * 2)))

        self.image_mouse_over_slot = pygame.Surface((slot_length, slot_width))
        self.image_mouse_over_slot.fill((255, 150, 0))
        pygame.draw.rect(self.image_mouse_over_slot, (255, 255, 255), (
            self.border_width, self.border_width, slot_length - (self.border_width * 2),
            slot_width - (self.border_width * 2)))

    def mouse_on_slot(self):
        # Checks of the cursor is on the button
        cursor_pos = pygame.mouse.get_pos()

        if self.pos[0] < cursor_pos[0] < self.pos[0] + slot_length and \
                self.pos[1] < cursor_pos[1] < self.pos[1] + slot_width:
            return True
        else:
            return False

    def load_image(self, path):
        Img = pygame.image.load(path)
        self.screenshot = pygame.transform.scale(Img, (slot_width - (self.border_width * 2),
                                                       slot_width - (self.border_width * 2)))

    def draw(self, screen):
        if self.selected:
            screen.blit(self.image_selected, self.pos)

        elif self.mouse_on_slot():
            screen.blit(self.image_mouse_over_slot, self.pos)

        else:
            screen.blit(self.image_not_selected, self.pos)

        if self.empty:
            size = self.empty_text.get_size()
            screen.blit(self.empty_text, (self.pos[0] + (slot_length // 2) - (size[0] // 2),
                                          self.pos[1] + (slot_width // 2) - (size[1] // 2)))

        else:
            x = self.pos[0] + slot_width - self.border_width + ((slot_length - slot_width + self.border_width) // 2)

            size = self.date.get_size()
            screen.blit(self.date, (x - (size[0] // 2), self.pos[1] + (slot_width // 2) - size[1]))

            size = self.time.get_size()
            screen.blit(self.time, (x - (size[0] // 2), self.pos[1] + (slot_width // 2)))

            screen.blit(self.screenshot, (self.pos[0] + self.border_width, self.pos[1] + self.border_width))
