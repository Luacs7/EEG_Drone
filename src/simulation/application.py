import pygame
import sys

from src.map.map import Map

# Image PATH
PATH_CRAZY_DRONE = "D:/NTNU/drone_eeg/src/simulation/crazy_drone.jpg"

class Application:
    def __init__(self, m: object = Map()):
       
        pygame.init()
        
        #Initialisation of the screen
        self.screen_width = 1600
        self.screen_height = 800
        self.background_color = (255, 255, 255)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        #Load of important image
        self.crazy_drone_image = pygame.image.load(PATH_CRAZY_DRONE)
        
        #Main variable
        self.mode = "Simulation"
        self.map = m

        
    def set_mode(self, mode):
        if mode in ["Simulation", "Real"]:
            self.mode = mode
        else:
            raise ValueError("Mode must be 'Simulation' or 'Real'")
    
    def get_mode(self):
        return self.mode    
    
    def draw_background_menu(self):
        self.screen.fill(self.background_color)
        self.screen.blit(self.crazy_drone_image, (self.screen_width / 3,0))
    
    def show_menu(self):

        menu_font = pygame.font.SysFont(None, 36)
        title_font = pygame.font.SysFont(None, 54)
        title = title_font.render('EEG Drone', True, (0, 0, 0))
        start_text = menu_font.render('Start Game', True, (0, 0, 0))
        quit_text = menu_font.render('Quit', True, (0, 0, 0))
        
        title_rect = title.get_rect(center=(self.screen_width / 2, (self.screen_height / 2)+100))
        start_rect = start_text.get_rect(center=(self.screen_width / 2, self.screen_height / 2 + 175))
        quit_rect = quit_text.get_rect(center=(self.screen_width / 2, self.screen_height / 2 + 225))

        mode_font = pygame.font.SysFont(None, 24)
        mode_0 = mode_font.render('Simulation', True, (0,0,0))
        mode_1 = mode_font.render('Real', True, (0,0,0))
        mode_0_rect = mode_0.get_rect(center=((self.screen_width/2)+50,self.screen_height-125))
        mode_1_rect = mode_1.get_rect(center=((self.screen_width/2)-50,self.screen_height-125))

        while True:
            self.draw_background_menu()

            self.screen.blit(title, title_rect)
            self.screen.blit(start_text, start_rect)
            self.screen.blit(quit_text, quit_rect)

            self.screen.blit(mode_0, mode_0_rect)
            self.screen.blit(mode_1, mode_1_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_rect.collidepoint(mouse_pos):
                        return 'start'
                    elif quit_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
                    if mode_0_rect.collidepoint(mouse_pos):
                        self.set_mode("Simulation")
                        mode_0 = mode_font.render('Simulation', True, (255,0,0))
                        mode_1 = mode_font.render('Real', True, (0,0,0))
                    if mode_1_rect.collidepoint(mouse_pos):
                        self.set_mode("Real")
                        mode_0 = mode_font.render('Simulation', True, (0,0,0))
                        mode_1 = mode_font.render('Real', True, (255,0,0))

            pygame.display.flip()

def run(self):


    pass

# Exemple d'utilisation
if __name__ == "__main__":
    app = Application()
    app.show_menu()