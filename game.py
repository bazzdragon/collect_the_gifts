import pygame
import random
import math
from enum import Enum

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GAME_TIME = 30  # 30 seconds
GIFT_COUNT = 10
GIFT_VELOCITY_MIN = -1  # Minimum velocity for gift movement
GIFT_VELOCITY_MAX = 1   # Maximum velocity for gift movement

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
GOLD = (255, 215, 0)
BLUE = (0, 100, 255)
PURPLE = (150, 0, 200)
DARK_RED = (180, 0, 0)
LIGHT_RED = (255, 100, 100)
BUTTON_COLOR = (0, 150, 0)
BUTTON_HOVER = (0, 200, 0)
SKIN_COLOR = (255, 224, 189)
LIGHT_BLUE = (200, 230, 255) # Winter background
BROWN = (139, 69, 19)
DARK_BROWN = (101, 67, 33)

class GameState(Enum):
    START = 1
    PLAYING = 2
    GAME_OVER = 3

class Gift:
    def __init__(self, x, y, gift_type=None):
        self.x = x
        self.y = y
        self.size = 50  # Base size
        self.gift_type = gift_type if gift_type else random.randint(1, 3)
        self.shape_type = random.choice(['box', 'long', 'round'])
        
        # Different colors for different gift types
        if self.gift_type == 1:
            self.color = RED
        elif self.gift_type == 2:
            self.color = BLUE
        else:
            self.color = PURPLE
            
        self.vx = random.uniform(GIFT_VELOCITY_MIN, GIFT_VELOCITY_MAX)
        self.vy = random.uniform(GIFT_VELOCITY_MIN, GIFT_VELOCITY_MAX)
        self.being_dragged = False
        
        self.angle = 0
        self.rotation_speed = random.uniform(-2, 2)
        
        # Adjust dimensions based on shape
        if self.shape_type == 'long':
            self.width = 70
            self.height = 40
        else:
            self.width = 50
            self.height = 50
        
    def update(self):
        if not self.being_dragged:
            # Move the gift
            self.x += self.vx
            self.y += self.vy
            self.angle += self.rotation_speed
            
            # Bounce off walls
            if self.x <= self.width//2 or self.x >= SCREEN_WIDTH - self.width//2:
                self.vx *= -1
            if self.y <= self.height//2 or self.y >= SCREEN_HEIGHT - self.height//2:
                self.vy *= -1
                
            # Keep within bounds
            self.x = max(self.width//2, min(SCREEN_WIDTH - self.width//2, self.x))
            self.y = max(self.height//2, min(SCREEN_HEIGHT - self.height//2, self.y))
    
    def draw(self, screen):
        # Create a surface for the gift to handle rotation
        surface_size = int(max(self.width, self.height) * 1.5) # Make room for rotation
        gift_surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)
        
        # Center of the surface
        cx, cy = surface_size // 2, surface_size // 2
        
        if self.shape_type == 'round':
            # Draw round gift
            pygame.draw.circle(gift_surface, self.color, (cx, cy), self.width//2)
            # Ribbon
            pygame.draw.line(gift_surface, GOLD, (cx - self.width//2, cy), (cx + self.width//2, cy), 5)
            pygame.draw.line(gift_surface, GOLD, (cx, cy - self.width//2), (cx, cy + self.width//2), 5)
        else:
            # Draw rectangular/box gift
            rect = pygame.Rect(cx - self.width//2, cy - self.height//2, self.width, self.height)
            pygame.draw.rect(gift_surface, self.color, rect)
            # Ribbon
            pygame.draw.line(gift_surface, GOLD, (cx - self.width//2, cy), (cx + self.width//2, cy), 5)
            pygame.draw.line(gift_surface, GOLD, (cx, cy - self.height//2), (cx, cy + self.height//2), 5)
        
        # Draw bow
        bow_y = cy - (self.width//2 if self.shape_type == 'round' else self.height//2)
        pygame.draw.circle(gift_surface, GOLD, (cx - 10, bow_y), 8)
        pygame.draw.circle(gift_surface, GOLD, (cx + 10, bow_y), 8)
        pygame.draw.circle(gift_surface, GOLD, (cx, bow_y), 6)
        
        # Rotate the surface
        rotated_surface = pygame.transform.rotate(gift_surface, self.angle)
        new_rect = rotated_surface.get_rect(center=(self.x, self.y))
        
        screen.blit(rotated_surface, new_rect)
    
    def contains_point(self, px, py):
        return (abs(px - self.x) <= self.size//2 and 
                abs(py - self.y) <= self.size//2)
    
    def collides_with(self, other_x, other_y, other_size):
        dx = self.x - other_x
        dy = self.y - other_y
        distance = math.sqrt(dx*dx + dy*dy)
        return distance < (self.size//2 + other_size//2)

class Bag:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 100
        self.size = 120  # Increased from 80
        self.color = RED
    
    def draw(self, screen):
        # Draw Santa holding the bag (simple representation)
        # Santa's body behind the bag
        santa_x = self.x + 60
        santa_y = self.y
        
        # Santa's Legs
        pygame.draw.rect(screen, RED, (santa_x - 30, santa_y + 50, 25, 50)) # Left Leg
        pygame.draw.rect(screen, RED, (santa_x + 5, santa_y + 50, 25, 50))  # Right Leg
        # Boots
        pygame.draw.rect(screen, BLACK, (santa_x - 35, santa_y + 100, 35, 15))
        pygame.draw.rect(screen, BLACK, (santa_x + 5, santa_y + 100, 35, 15))

        # Santa's Body (Coat) - Widened to match new head size
        pygame.draw.rect(screen, RED, (santa_x - 40, santa_y - 30, 80, 80))
        # Belt
        pygame.draw.rect(screen, BLACK, (santa_x - 40, santa_y + 20, 80, 10))
        pygame.draw.rect(screen, GOLD, (santa_x - 10, santa_y + 20, 20, 10), 2) # Buckle
        
        # Santa's Head (Matched to Start Screen: Radius 40, centered higher)
        # In start screen, head center is at y-40. Here we lift it to y-60 to be above body/bag
        head_y_offset = 60
        pygame.draw.circle(screen, SKIN_COLOR, (santa_x, santa_y - head_y_offset), 40)
        
        # Santa's Beard (Matched to Start Screen)
        # Start screen beard offsets: (-15, -20, -20, 0, +15) relative to center y-40
        # We apply same offsets relative to our head center (santa_y - head_y_offset)
        # But we need to adjust slightly because our head center is y-60
        
        # Main beard mass
        pygame.draw.circle(screen, WHITE, (santa_x, santa_y - head_y_offset + 25), 25) # Center
        pygame.draw.circle(screen, WHITE, (santa_x - 18, santa_y - head_y_offset + 20), 18) # Left
        pygame.draw.circle(screen, WHITE, (santa_x + 18, santa_y - head_y_offset + 20), 18) # Right
        # Tapering bottom
        pygame.draw.circle(screen, WHITE, (santa_x, santa_y - head_y_offset + 40), 18)
        pygame.draw.circle(screen, WHITE, (santa_x, santa_y - head_y_offset + 55), 12)
        
        # Santa's Hat (Matched to Start Screen)
        # Start screen hat: polygon top y-120, base y-60. (Head center y-40).
        # So base is 20 above center. Top is 80 above center.
        # Our center is santa_y - 60.
        # Base: santa_y - 80. Top: santa_y - 140.
        pygame.draw.polygon(screen, RED, [
            (santa_x - 40, santa_y - head_y_offset - 20), 
            (santa_x + 40, santa_y - head_y_offset - 20), 
            (santa_x, santa_y - head_y_offset - 80)
        ])
        pygame.draw.circle(screen, WHITE, (santa_x, santa_y - head_y_offset - 80), 12) # Pom pom
        pygame.draw.rect(screen, WHITE, (santa_x - 45, santa_y - head_y_offset - 20, 90, 15)) # Hat trim
        
        # Santa's Eyes (Matched to Start Screen)
        # Start screen eyes: y-45 (5 pixels above center y-40).
        # Our center: santa_y - 60. So eyes at santa_y - 65.
        pygame.draw.circle(screen, BLACK, (santa_x - 12, santa_y - head_y_offset - 5), 4)
        pygame.draw.circle(screen, BLACK, (santa_x + 12, santa_y - head_y_offset - 5), 4)

        # Draw Santa's bag body (The "Best Sack")
        # Base/Bottom weight (Heavy look)
        pygame.draw.ellipse(screen, self.color, (self.x - self.size//1.6, self.y - self.size//4, self.size*1.25, self.size))
        
        # Mid-section connecting to neck
        pygame.draw.polygon(screen, self.color, [
            (self.x - self.size//2.5, self.y - self.size//1.5), # Neck Left
            (self.x + self.size//2.5, self.y - self.size//1.5), # Neck Right
            (self.x + self.size//1.8, self.y + self.size//4),   # Body Right
            (self.x - self.size//1.8, self.y + self.size//4)    # Body Left
        ])
        
        # Highlight/Shading (Lighter Red)
        highlight_rect = pygame.Rect(self.x - self.size//3, self.y, self.size//2, self.size//3)
        pygame.draw.ellipse(screen, LIGHT_RED, highlight_rect)
        
        # Wrinkles (Darker lines)
        pygame.draw.arc(screen, DARK_RED, (self.x - self.size//2, self.y, self.size, self.size//2), 0.5, 2.5, 3)
        pygame.draw.arc(screen, DARK_RED, (self.x - self.size//3, self.y - self.size//3, self.size//1.5, self.size//2), 0.2, 2.0, 2)

        # Inside of the sack (Darker) - Drawn BEFORE trim now
        inside_rect = pygame.Rect(self.x - self.size//3, self.y - self.size//1.55, 
                                  self.size * 0.66, self.size * 0.15)
        pygame.draw.ellipse(screen, DARK_RED, inside_rect)

        # Fluffy Trim at the top (Cloud-like) - Drawn AFTER inside
        trim_y = self.y - self.size//1.5
        trim_width = self.size * 0.9
        trim_start_x = self.x - trim_width//2
        
        # Draw multiple circles for fluff
        for i in range(5):
            cx = trim_start_x + (i * (trim_width/4))
            # Slightly lower y for the front circles to overlap the hole
            pygame.draw.circle(screen, WHITE, (int(cx), int(trim_y + 10)), 18) # +10 offset
            
        
        # Santa's Hand holding the bag
        pygame.draw.circle(screen, SKIN_COLOR, (self.x + self.size//3, self.y - self.size//4), 15)
        # Sleeve
        pygame.draw.rect(screen, RED, (self.x + self.size//3 + 10, self.y - self.size//4 - 10, 30, 20))
        pygame.draw.rect(screen, WHITE, (self.x + self.size//3 + 5, self.y - self.size//4 - 12, 10, 24)) # Cuff


class Button:
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.hovered = False
    
    def draw(self, screen):
        color = BUTTON_HOVER if self.hovered else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 3, border_radius=10)
        
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def is_hovered(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Collect the Gifts")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)
        self.title_font = pygame.font.Font(None, 90)
        self.subtitle_font = pygame.font.Font(None, 30)
        
        self.state = GameState.START
        
        self.reset_game()
        
        # Create buttons
        button_width = 200
        button_height = 60
        
        # Try Again Button
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        button_y = SCREEN_HEIGHT // 2 + 100
        self.try_again_button = Button(button_x, button_y, button_width, button_height, 
                                       "Try Again", self.font)
                                       
        # Play Button
        self.play_button = Button(button_x, SCREEN_HEIGHT // 2, button_width, button_height,
                                  "PLAY", self.large_font)
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.gifts = []
        self.bag = Bag()
        self.score = 0
        self.dragging_gift = None
        self.start_time = pygame.time.get_ticks()
        self.spawn_gifts()
        
        # Start screen flying gifts
        self.start_gifts = []
        # Sack position on start screen
        sack_x = SCREEN_WIDTH - 150
        sack_y = SCREEN_HEIGHT // 2 + 100
        
        for _ in range(5):
             self.start_gifts.append(Gift(
                 random.randint(sack_x - 40, sack_x + 40),
                 random.randint(sack_y - 130, sack_y - 100)
             ))
             # Make them fly up and out
             self.start_gifts[-1].vy = random.uniform(-5, -2)
             self.start_gifts[-1].vx = random.uniform(-3, 3)

    
    def spawn_gifts(self):
        """Spawn GIFT_COUNT new gifts at random positions"""
        for _ in range(GIFT_COUNT):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 150)
            self.gifts.append(Gift(x, y))
            
    def get_rank(self):
        if self.score == 0:
            return "Grinch"
        elif self.score < 5:
            return "Coal Collector"
        elif self.score < 10:
            return "Reindeer Walker"
        elif self.score < 15:
            return "Sleigh Polisher"
        elif self.score < 20:
            return "Gift Wrapper"
        elif self.score < 25:
            return "Toy Maker"
        elif self.score < 30:
            return "Head Elf"
        elif self.score < 35:
            return "Santa's Right Hand"
        elif self.score < 40:
            return "Santa's Apprentice"
        else:
            return "Santa's Best Elf"

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if self.state == GameState.START:
                        if self.play_button.is_clicked(mouse_pos):
                            self.state = GameState.PLAYING
                            self.reset_game()
                            self.start_time = pygame.time.get_ticks() # Reset timer on start
                    
                    elif self.state == GameState.GAME_OVER:
                        # Check if try again button clicked
                        if self.try_again_button.is_clicked(mouse_pos):
                            self.state = GameState.PLAYING
                            self.reset_game()
                            self.start_time = pygame.time.get_ticks()
                    
                    elif self.state == GameState.PLAYING:
                        # Check if clicked on a gift
                        mx, my = event.pos
                        for gift in self.gifts:
                            if gift.contains_point(mx, my):
                                self.dragging_gift = gift
                                gift.being_dragged = True
                                break
                                
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.dragging_gift and self.state == GameState.PLAYING:
                    # Check if gift is dropped in the bag
                    if self.dragging_gift.collides_with(self.bag.x, self.bag.y, self.bag.size):
                        self.score += 1
                        self.gifts.remove(self.dragging_gift)
                        
                        # Spawn new gifts if all are collected
                        if len(self.gifts) == 0:
                            self.spawn_gifts()
                    
                    self.dragging_gift.being_dragged = False
                    self.dragging_gift = None
                    
            elif event.type == pygame.MOUSEMOTION:
                if self.state == GameState.START:
                    self.play_button.is_hovered(mouse_pos)
                elif self.state == GameState.GAME_OVER:
                    self.try_again_button.is_hovered(mouse_pos)
                elif self.state == GameState.PLAYING and self.dragging_gift:
                    mx, my = event.pos
                    self.dragging_gift.x = mx
                    self.dragging_gift.y = my
    
    def update(self):
        if self.state == GameState.START:
            # Sack position on start screen
            sack_x = SCREEN_WIDTH - 150
            sack_y = SCREEN_HEIGHT // 2 + 100
            
            # Update background flying gifts for start screen
            for gift in self.start_gifts:
                gift.x += gift.vx
                gift.y += gift.vy
                # Respawn if off screen
                if gift.y < -50 or gift.x < 0 or gift.x > SCREEN_WIDTH:
                    # Respawn inside the sack
                    gift.x = random.randint(sack_x - 40, sack_x + 40)
                    gift.y = random.randint(sack_y - 130, sack_y - 100)
                    gift.vy = random.uniform(-5, -2)
                    gift.vx = random.uniform(-3, 3)
            return

        if self.state == GameState.GAME_OVER:
            return
        
        # Check time
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        if elapsed_time >= GAME_TIME:
            self.state = GameState.GAME_OVER
            # Release any dragged gift
            if self.dragging_gift:
                self.dragging_gift.being_dragged = False
                self.dragging_gift = None
            return
        
        # Update gifts
        for gift in self.gifts:
            gift.update()
    
    def draw_start_screen(self):
        self.screen.fill(LIGHT_BLUE)
        
        # Draw Title
        title_text = self.title_font.render("Collect the Gifts", True, RED)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Draw Subtitle
        subtitle_text = self.subtitle_font.render("Santa needs your help in saving the gifts!", True, GREEN)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 160))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Draw Play Button
        self.play_button.draw(self.screen)
        
        # Draw Santa (Left Side) - Full Body
        santa_x = 150
        santa_y = SCREEN_HEIGHT // 2
        
        # Body
        pygame.draw.rect(self.screen, RED, (santa_x - 40, santa_y - 20, 80, 100))
        # Belt
        pygame.draw.rect(self.screen, BLACK, (santa_x - 40, santa_y + 40, 80, 15))
        pygame.draw.rect(self.screen, GOLD, (santa_x - 10, santa_y + 40, 20, 15), 2)
        # Legs
        pygame.draw.rect(self.screen, RED, (santa_x - 40, santa_y + 80, 35, 60))
        pygame.draw.rect(self.screen, RED, (santa_x + 5, santa_y + 80, 35, 60))
        # Boots
        pygame.draw.rect(self.screen, BLACK, (santa_x - 45, santa_y + 140, 45, 20))
        pygame.draw.rect(self.screen, BLACK, (santa_x + 5, santa_y + 140, 45, 20))
        # Arms
        pygame.draw.rect(self.screen, RED, (santa_x - 70, santa_y - 10, 30, 70)) # Left Arm
        pygame.draw.rect(self.screen, RED, (santa_x + 40, santa_y - 10, 30, 70)) # Right Arm
        # Mittens
        pygame.draw.circle(self.screen, BLACK, (santa_x - 55, santa_y + 60), 15)
        pygame.draw.circle(self.screen, BLACK, (santa_x + 55, santa_y + 60), 15)
        # Cuffs
        pygame.draw.rect(self.screen, WHITE, (santa_x - 70, santa_y + 45, 30, 10))
        pygame.draw.rect(self.screen, WHITE, (santa_x + 40, santa_y + 45, 30, 10))
        
        # Head
        pygame.draw.circle(self.screen, SKIN_COLOR, (santa_x, santa_y - 40), 40)
        
        # Beard (Bigger and Lowered further)
        # Main beard mass
        pygame.draw.circle(self.screen, WHITE, (santa_x, santa_y - 15), 25)
        pygame.draw.circle(self.screen, WHITE, (santa_x - 18, santa_y - 20), 18)
        pygame.draw.circle(self.screen, WHITE, (santa_x + 18, santa_y - 20), 18)
        # Tapering bottom
        pygame.draw.circle(self.screen, WHITE, (santa_x, santa_y), 18)
        pygame.draw.circle(self.screen, WHITE, (santa_x, santa_y + 15), 12)
        
        # Hat
        pygame.draw.polygon(self.screen, RED, [(santa_x - 40, santa_y - 60), (santa_x + 40, santa_y - 60), (santa_x, santa_y - 120)])
        pygame.draw.circle(self.screen, WHITE, (santa_x, santa_y - 120), 12)
        pygame.draw.rect(self.screen, WHITE, (santa_x - 45, santa_y - 60, 90, 15))
        # Eyes (Lowered further)
        pygame.draw.circle(self.screen, BLACK, (santa_x - 12, santa_y - 40), 4)
        pygame.draw.circle(self.screen, BLACK, (santa_x + 12, santa_y - 40), 4)
        
        # Draw Sack with flying presents (Right Side)
        sack_x = SCREEN_WIDTH - 150
        sack_y = SCREEN_HEIGHT // 2 + 100
        size = 120
        
        # Draw the sack (The "Best Sack")
        # Base/Bottom weight (Heavy look)
        pygame.draw.ellipse(self.screen, RED, (sack_x - size//1.6, sack_y - size//4, size*1.25, size))
        
        # Mid-section connecting to neck
        pygame.draw.polygon(self.screen, RED, [
            (sack_x - size//2.5, sack_y - size//1.5), # Neck Left
            (sack_x + size//2.5, sack_y - size//1.5), # Neck Right
            (sack_x + size//1.8, sack_y + size//4),   # Body Right
            (sack_x - size//1.8, sack_y + size//4)    # Body Left
        ])
        
        # Highlight/Shading (Lighter Red)
        highlight_rect = pygame.Rect(sack_x - size//3, sack_y, size//2, size//3)
        pygame.draw.ellipse(self.screen, LIGHT_RED, highlight_rect)
        
        # Wrinkles (Darker lines)
        pygame.draw.arc(self.screen, DARK_RED, (sack_x - size//2, sack_y, size, size//2), 0.5, 2.5, 3)
        pygame.draw.arc(self.screen, DARK_RED, (sack_x - size//3, sack_y - size//3, size//1.5, size//2), 0.2, 2.0, 2)

        # Inside of the sack (Darker) - Drawn BEFORE trim
        inside_rect = pygame.Rect(sack_x - size//3, sack_y - size//1.55, 
                                  size * 0.66, size * 0.15)
        pygame.draw.ellipse(self.screen, DARK_RED, inside_rect)
        
        # Fluffy Trim at the top (Cloud-like) - Drawn AFTER inside
        trim_y = sack_y - size//1.5
        trim_width = size * 0.9
        trim_start_x = sack_x - trim_width//2
        
        # Draw multiple circles for fluff
        for i in range(5):
            cx = trim_start_x + (i * (trim_width/4))
            # Lifted y slightly (from +15 to +10)
            pygame.draw.circle(self.screen, WHITE, (int(cx), int(trim_y + 10)), 18)

        # Draw flying gifts
        for gift in self.start_gifts:
            gift.draw(self.screen)

    def draw(self):
        if self.state == GameState.START:
            self.draw_start_screen()
        else:
            self.screen.fill(LIGHT_BLUE)
            
            # Draw bag
            self.bag.draw(self.screen)
            
            # Draw gifts
            for gift in self.gifts:
                gift.draw(self.screen)
            
            # Draw score
            score_text = self.font.render(f"Score: {self.score}", True, BLACK)
            self.screen.blit(score_text, (10, 10))
            
            # Draw timer
            elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
            time_left = max(0, GAME_TIME - elapsed_time)
            time_text = self.font.render(f"Time: {time_left:.1f}s", True, BLACK)
            self.screen.blit(time_text, (SCREEN_WIDTH - 150, 10))
            
            # Draw game over screen
            if self.state == GameState.GAME_OVER:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.set_alpha(200)
                overlay.fill(BLACK)
                self.screen.blit(overlay, (0, 0))
                
                game_over_text = self.large_font.render("TIME'S UP!", True, WHITE)
                score_text = self.large_font.render(f"Score: {self.score}", True, GOLD)
                rank_text = self.font.render(f"Rank: {self.get_rank()}", True, GREEN)
                
                self.screen.blit(game_over_text, 
                               (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 
                                SCREEN_HEIGHT//2 - 120))
                self.screen.blit(score_text, 
                               (SCREEN_WIDTH//2 - score_text.get_width()//2, 
                                SCREEN_HEIGHT//2 - 40))
                self.screen.blit(rank_text,
                               (SCREEN_WIDTH//2 - rank_text.get_width()//2,
                                SCREEN_HEIGHT//2 + 20))
                
                # Draw try again button
                self.try_again_button.draw(self.screen)
        
        pygame.display.flip()

    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
