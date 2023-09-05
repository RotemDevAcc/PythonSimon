import tkinter as tk
import random
import pygame.mixer

channel = None

class SimonGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Simon Game")

        self.sequence = []
        self.user_sequence = []
        self.round = 0
        self.step = 0
        self.game_started = False

        self.colors = ["red", "green", "blue", "yellow"]

        self.buttons = {}
        for i, color in enumerate(self.colors):
            self.buttons[color] = tk.Button(master, bg=color, height=5, width=10, command=lambda c=color: self.button_click(c))
            self.buttons[color].grid(row=i // 2, column=i % 2, padx=10, pady=10)

        self.start_button = tk.Button(master, text="Start", command=self.start_game)
        self.start_button.grid(row=len(self.colors) // 2, column=0, columnspan=2)

        self.round_label = tk.Label(master, text="Round: 0", font=("Arial", 20))
        self.round_label.grid(row=len(self.colors) // 2, column=2, columnspan=2)

    def start_game(self):
        if not self.game_started:
            global channel
            if(channel):
                channel.stop()
            channel = None
            self.game_started = True
            self.playing_sequence = False
            self.moving_round = False
            self.step = 0
            self.sequence = []
            self.user_sequence = []
            self.round = 0
            self.next_round()

    def next_round(self):
        self.round += 1
        self.sequence.append(random.choice(self.colors))
        self.round_label.config(text=f"Round: {self.round}")
        self.playing_sequence = True
        self.moving_round = False
        self.play_sequence(0)

    def play_sequence(self, index):
        if index < len(self.sequence):
            
            color = self.sequence[index]
            self.flash_button(color)
            self.master.after(1000, self.play_sequence, index + 1)
            
        else:
            self.user_sequence = []
            self.playing_sequence = False

    def flash_button(self, color):
        self.buttons[color].config(relief=tk.SUNKEN)
        self.master.update()
        self.playsoundbycolor(color)
        self.master.after(500, lambda: self.buttons[color].config(relief=tk.RAISED))
        self.master.update()

    def playsoundbycolor(self,color):
        sound = pygame.mixer.Sound(f"sounds/{color}.wav")
        sound.play()




    def button_click(self, color):
        if self.game_started:
            if(self.playing_sequence):
                return print("Cant Click in the middle of sequence")
            
            if(self.moving_round):
                return print("Moving Round, Please Wait.")
            
            self.user_sequence.append(color)
            self.flash_button(color)
            if color == self.sequence[self.step]:
                self.step += 1

                if self.step == len(self.sequence):
                    self.step = 0
                    self.moving_round = True
                    self.master.after(1000, self.next_round)
            else:
                self.end_game()

    def end_game(self):
        self.game_started = False
        self.round_label.config(text=f"Game Over! Your score: {self.round}")
        sound = pygame.mixer.Sound("sounds/gameover.wav")
        global channel
        channel = sound.play()
        self.start_button.config(text="Restart", command=self.start_game)

root = tk.Tk()
game = SimonGame(root)
pygame.mixer.init()
root.mainloop()
pygame.quit()
