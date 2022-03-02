import pygame, constants


current_path = constants.current_path + "Music\\"

pygame.mixer.init()
pygame.mixer.music.load(current_path + "GameMusic.wav")
pygame.mixer.music.play(-1) 

""" ex:
sounds = {}
sound_list = ['boing', 'Can-you-repeat-that-one', 'Hahaha', 'Hahahahahaha', 'jump', 'land', 'light_turn_on', 'Maw-ha-ha-ha-ha-ha', 'pop1', 'pop2', "Sorry_-I-donot-know-that_1", 'Your-time-is-up_1', "ouch", "wrong"]
def init(current_path):
    for sound in sound_list:
        # sounds[sound] = pygame.mixer.Sound(os.path.join(current_path, "Data/Sounds/" + sound + '.wav'))
        sounds[sound] = pygame.mixer.Sound("Data/Sounds/" + sound + '.wav')

alexa_laughs = ['Maw-ha-ha-ha-ha-ha', 'Hahaha', 'Hahahahahaha']

def alexa_laugh():
    sounds[random.choice(alexa_laughs)].play()
"""
