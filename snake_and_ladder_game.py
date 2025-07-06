#!/usr/bin/env python3
"""
🐍🪜 ULTIMATE SNAKES & LADDERS Game 🪜🐍
Enhanced with Pygame, Colorama, and spectacular visuals!
"""

import pygame
import random
import time
import math
import os
import sys
import threading
from colorama import init, Fore, Back, Style
import tkinter as tk
from tkinter import messagebox, simpledialog

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class GameColors:
    """Enhanced color system using colorama"""
    RED = Fore.RED + Style.BRIGHT
    BLUE = Fore.BLUE + Style.BRIGHT
    GREEN = Fore.GREEN + Style.BRIGHT
    YELLOW = Fore.YELLOW + Style.BRIGHT
    PURPLE = Fore.MAGENTA + Style.BRIGHT
    CYAN = Fore.CYAN + Style.BRIGHT
    WHITE = Fore.WHITE + Style.BRIGHT
    
    BG_RED = Back.RED + Fore.WHITE + Style.BRIGHT
    BG_BLUE = Back.BLUE + Fore.WHITE + Style.BRIGHT
    BG_GREEN = Back.GREEN + Fore.WHITE + Style.BRIGHT
    BG_YELLOW = Back.YELLOW + Fore.BLACK + Style.BRIGHT
    BG_PURPLE = Back.MAGENTA + Fore.WHITE + Style.BRIGHT
    BG_CYAN = Back.CYAN + Fore.BLACK + Style.BRIGHT

class UltimateSnakeLadderGame:
    def __init__(self):
        """Initialize the Ultimate SNAKES & LADDERS game with pygame"""
        # Initialize pygame
        pygame.init()
        
        # Game settings - Keep original square size but larger window
        self.WINDOW_WIDTH = 1400
        self.WINDOW_HEIGHT = 1000
        self.BOARD_SIZE = 600
        self.SQUARE_SIZE = 60  # Back to original size
        
        # Create snake and ladder images
        self.create_game_images()
    def create_game_images(self):
        """Create realistic snake and ladder images like traditional board game"""
        
        # Create realistic ladder image
        self.ladder_image = pygame.Surface((50, 100), pygame.SRCALPHA)
        ladder_brown = (139, 90, 43)
        ladder_light = (205, 133, 63)
        
        # Draw ladder sides (rails)
        pygame.draw.rect(self.ladder_image, ladder_brown, (8, 0, 8, 100))
        pygame.draw.rect(self.ladder_image, ladder_brown, (34, 0, 8, 100))
        
        # Add wood grain effect to rails
        pygame.draw.rect(self.ladder_image, ladder_light, (10, 0, 4, 100))
        pygame.draw.rect(self.ladder_image, ladder_light, (36, 0, 4, 100))
        
        # Draw ladder rungs (steps)
        for i in range(0, 100, 15):
            # Main rung
            pygame.draw.rect(self.ladder_image, ladder_brown, (8, i, 34, 6))
            # Highlight on rung
            pygame.draw.rect(self.ladder_image, ladder_light, (8, i, 34, 2))
        
        # Create realistic snake image
        self.snake_image = pygame.Surface((80, 80), pygame.SRCALPHA)
        
        # Snake colors - green with patterns
        snake_dark = (34, 139, 34)
        snake_light = (50, 205, 50)
        snake_pattern = (0, 100, 0)
        
        # Draw snake body segments in S-curve
        segments = [
            # (x, y, width, height) for each body segment
            (10, 60, 25, 15),  # Tail
            (20, 45, 30, 18),  # Body 1
            (35, 30, 32, 20),  # Body 2
            (25, 15, 30, 18),  # Body 3
            (15, 5, 25, 15),   # Head
        ]
        
        # Draw snake body
        for i, (x, y, w, h) in enumerate(segments):
            # Main body color
            pygame.draw.ellipse(self.snake_image, snake_dark, (x, y, w, h))
            # Lighter belly
            pygame.draw.ellipse(self.snake_image, snake_light, (x+2, y+2, w-4, h-4))
            # Pattern spots
            if i % 2 == 0:
                pygame.draw.ellipse(self.snake_image, snake_pattern, (x+w//3, y+h//3, w//3, h//3))
        
        # Draw snake head details (on the head segment)
        head_x, head_y = 15, 5
        # Eyes
        pygame.draw.circle(self.snake_image, (255, 255, 255), (head_x + 8, head_y + 5), 4)
        pygame.draw.circle(self.snake_image, (255, 255, 255), (head_x + 18, head_y + 5), 4)
        pygame.draw.circle(self.snake_image, (0, 0, 0), (head_x + 8, head_y + 5), 2)
        pygame.draw.circle(self.snake_image, (0, 0, 0), (head_x + 18, head_y + 5), 2)
        
        # Forked tongue
        pygame.draw.line(self.snake_image, (255, 0, 0), (head_x + 13, head_y + 12), (head_x + 13, head_y + 18), 2)
        pygame.draw.line(self.snake_image, (255, 0, 0), (head_x + 11, head_y + 18), (head_x + 15, head_y + 18), 2)
        
        # Create game window
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("SNAKES & LADDERS")
        
        # Game state
        self.players = {}
        self.current_player = 1
        self.game_over = False
        self.winner = None
        self.dice_value = 1
        self.dice_rolling = False
        self.timer_active = False
        self.time_left = 45
        
        # Colors for pygame - Fall Season Theme
        self.COLORS = {
            'WHITE': (255, 255, 255),
            'BLACK': (50, 50, 50),
            'SOFT_RED': (180, 80, 70),
            'MUTED_BLUE': (70, 100, 130),
            'FOREST_GREEN': (85, 107, 47),
            'WARM_YELLOW': (218, 165, 32),
            'LAVENDER': (147, 112, 147),
            'SOFT_CYAN': (95, 158, 160),
            'BURNT_ORANGE': (204, 85, 0),
            'DUSTY_ROSE': (188, 143, 143),
            'CREAM': (245, 245, 220),
            'SAGE_GREEN': (154, 205, 50),
            'GOLDEN_BROWN': (184, 134, 11),
            'RUSTIC_BROWN': (139, 90, 43),
            'DEEP_RED': (139, 69, 19),
            'AUTUMN_ORANGE': (255, 140, 0),
            'FALL_GRADIENT': (205, 133, 63)
        }
        
        # Game elements
        self.ladders = {
            1: 38,   # Ladder from 1 to 38
            21: 42,  # Ladder from 21 to 42
            4: 14,   # Ladder from 4 to 14
            9: 31,   # Ladder from 9 to 31
            28: 84,  # Ladder from 28 to 84
            51: 67,  # Ladder from 51 to 67
            71: 91,  # Ladder from 71 to 91
            80: 100  # Ladder from 80 to 100
        }
        
        self.snakes = {
            17: 7,   # Snake from 17 to 7
            62: 19,  # Snake from 62 to 19
            64: 60,  # Snake from 64 to 60
            87: 24,  # Snake from 87 to 24
            93: 73,  # Snake from 93 to 73
            98: 79,  # Snake from 98 to 79
            54: 34,  # Snake from 54 to 34
            95: 75   # Snake from 95 to 75
        }
        
        # Player info with fall colors - no emojis
        self.player_info = {
            1: {'color': self.COLORS['SOFT_RED'], 'name': 'Player 1', 'symbol': 'P1'},
            2: {'color': self.COLORS['MUTED_BLUE'], 'name': 'Player 2', 'symbol': 'P2'},
            3: {'color': self.COLORS['FOREST_GREEN'], 'name': 'Player 3', 'symbol': 'P3'},
            4: {'color': self.COLORS['BURNT_ORANGE'], 'name': 'Player 4', 'symbol': 'P4'}
        }
        
        # Fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Clock for FPS
        self.clock = pygame.time.Clock()
    def run_game(self):
        """Simple game runner - basic version"""
        # Initialize pygame
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Snake and Ladder Game")
        clock = pygame.time.Clock()
        
        # Simple setup
        self.players = {1: 0, 2: 0}  # Two players starting at position 0
        self.current_player = 1
        
        print("🎮 Snake and Ladder Game Started!")
        print("Players: Player 1, Player 2")
        print("Click the window and press SPACE to roll dice, ESC to quit")
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Roll dice
                        dice_roll = random.randint(1, 6)
                        old_pos = self.players[self.current_player]
                        new_pos = min(100, old_pos + dice_roll)
                        self.players[self.current_player] = new_pos
                        
                        print(f"Player {self.current_player} rolled {dice_roll}")
                        print(f"Moved from {old_pos} to {new_pos}")
                        
                        # Check for ladders
                        if new_pos in self.ladders:
                            ladder_top = self.ladders[new_pos]
                            self.players[self.current_player] = ladder_top
                            print(f"🪜 LADDER! Climbed to {ladder_top}")
                        
                        # Check for snakes
                        elif new_pos in self.snakes:
                            snake_tail = self.snakes[new_pos]
                            self.players[self.current_player] = snake_tail
                            print(f"🐍 SNAKE! Slid down to {snake_tail}")
                        
                        # Check for win
                        if self.players[self.current_player] >= 100:
                            print(f"🎉 Player {self.current_player} WINS!")
                            running = False
                        else:
                            # Switch players
                            self.current_player = 2 if self.current_player == 1 else 1
                            print(f"Current player: {self.current_player}")
                            print("---")
                    
                    elif event.key == pygame.K_ESCAPE:
                        running = False
            
            # Simple display
            screen.fill((245, 245, 220))  # Cream background
            
            # Draw simple board representation
            font = pygame.font.Font(None, 36)
            
            # Show player positions
            for i, (player, pos) in enumerate(self.players.items()):
                text = font.render(f"Player {player}: Position {pos}", True, (0, 0, 0))
                screen.blit(text, (50, 50 + i * 40))
            
            # Show current player
            current_text = font.render(f"Current Player: {self.current_player}", True, (255, 0, 0))
            screen.blit(current_text, (50, 150))
            
            # Instructions
            inst_font = pygame.font.Font(None, 24)
            instructions = [
                "Press SPACE to roll dice",
                "Press ESC to quit",
                "First to reach 100 wins!"
            ]
            for i, inst in enumerate(instructions):
                inst_text = inst_font.render(inst, True, (100, 100, 100))
                screen.blit(inst_text, (50, 250 + i * 25))
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        print("Thanks for playing!")

def main():
    """Main function"""
    try:
        print("🚀 Starting Snake and Ladder Game...")
        game = UltimateSnakeLadderGame()
        game.run_game()
    except ImportError as e:
        print(f"❌ Missing required library: {e}")
        print("Please install: pip install pygame colorama")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
