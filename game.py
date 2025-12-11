import pygame
import random
import math

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

class Gift:
    def __init__(self, x, y, gift_type=None):
        self.x = x
        self.y = y
        self.size = 50  # Increased from 30
        self.gift_type = gift_type if gift_type else random.randint(1, 3)
        
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
        
    def update(self):
        if not self.being_dragged:
            # Move the gift
            self.x += self.vx
            self.y += self.vy
            
            # Bounce off walls
            if self.x <= self.size or self.x >= SCREEN_WIDTH - self.size:
                self.vx *= -1
            if self.y <= self.size or self.y >= SCREEN_HEIGHT - self.size:
                self.vy *= -1
                
            # Keep within bounds
            self.x = max(self.size, min(SCREEN_WIDTH - self.size, self.x))
            self.y = max(self.size, min(SCREEN_HEIGHT - self.size, self.y))
    
    def draw(self, screen):
        # Draw a simple gift box
        pygame.draw.rect(screen, self.color, 
                        (self.x - self.size//2, self.y - self.size//2, 
                         self.size, self.size))
        
        # Draw ribbon (vertical and horizontal)
        pygame.draw.line(screen, GOLD, 
                        (self.x - self.size//2, self.y), 
                        (self.x + self.size//2, self.y), 5)
        pygame.draw.line(screen, GOLD, 
                        (self.x, self.y - self.size//2), 
                        (self.x, self.y + self.size//2), 5)
        
        # Draw bow on top - centered at top of gift
        bow_x = int(self.x)
        bow_y = int(self.y - self.size//2)
        
        # Bow loops (two circles on sides)
        pygame.draw.circle(screen, GOLD, (bow_x - 10, bow_y), 8)
        pygame.draw.circle(screen, GOLD, (bow_x + 10, bow_y), 8)
        
        # Bow center knot
        pygame.draw.circle(screen, GOLD, (bow_x, bow_y), 6)
        
        # Bow ribbons hanging down
        pygame.draw.line(screen, GOLD, (bow_x - 5, bow_y + 6), (bow_x - 8, bow_y + 15), 3)
        pygame.draw.line(screen, GOLD, (bow_x + 5, bow_y + 6), (bow_x + 8, bow_y + 15), 3)
    
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
        self.y = SCREEN_HEIGHT - 80
        self.size = 80  # Increased from 60
        self.color = RED
    
    def draw(self, screen):
        # Draw Santa's bag body (main sack)
        bag_rect = pygame.Rect(self.x - self.size//2, self.y - self.size//3, 
                               self.size, self.size * 0.8)
        pygame.draw.ellipse(screen, self.color, bag_rect)
        
        # Draw bag opening/top (darker red oval)
        opening_rect = pygame.Rect(self.x - self.size//2.5, self.y - self.size//2.5, 
                                   self.size * 0.8, self.size * 0.35)
        pygame.draw.ellipse(screen, DARK_RED, opening_rect)
        
        # Draw rope/drawstring at the top
        pygame.draw.arc(screen, GOLD, 
                       (self.x - self.size//3, self.y - self.size//2, 
                        self.size * 0.6, self.size * 0.3), 
                       0, 3.14, 4)
        
        # Draw some wrinkles/folds for texture
        pygame.draw.line(screen, DARK_RED, 
                        (self.x - self.size//4, self.y), 
                        (self.x - self.size//4, self.y + self.size//3), 2)
        pygame.draw.line(screen, DARK_RED, 
                        (self.x + self.size//4, self.y), 
                        (self.x + self.size//4, self.y + self.size//3), 2)

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
        
        self.reset_game()
        
        # Create try again button
        button_width = 200
        button_height = 60
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        button_y = SCREEN_HEIGHT // 2 + 100
        self.try_again_button = Button(button_x, button_y, button_width, button_height, 
                                       "Try Again", self.font)
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.gifts = []
        self.bag = Bag()
        self.score = 0
        self.dragging_gift = None
        self.start_time = pygame.time.get_ticks()
        self.game_over = False
        self.spawn_gifts()
    
    def spawn_gifts(self):
        """Spawn GIFT_COUNT new gifts at random positions"""
        for _ in range(GIFT_COUNT):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 150)
            self.gifts.append(Gift(x, y))
    
    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if self.game_over:
                        # Check if try again button clicked
                        if self.try_again_button.is_clicked(mouse_pos):
                            self.reset_game()
                    else:
                        # Check if clicked on a gift
                        mx, my = event.pos
                        for gift in self.gifts:
                            if gift.contains_point(mx, my):
                                self.dragging_gift = gift
                                gift.being_dragged = True
                                break
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.dragging_gift and not self.game_over:
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
                if self.game_over:
                    self.try_again_button.is_hovered(mouse_pos)
                elif self.dragging_gift:
                    mx, my = event.pos
                    self.dragging_gift.x = mx
                    self.dragging_gift.y = my
    
    def update(self):
        if self.game_over:
            return
        
        # Check time
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        if elapsed_time >= GAME_TIME:
            self.game_over = True
            # Release any dragged gift
            if self.dragging_gift:
                self.dragging_gift.being_dragged = False
                self.dragging_gift = None
            return
        
        # Update gifts
        for gift in self.gifts:
            gift.update()
    
    def draw(self):
        self.screen.fill(WHITE)
        
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
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.large_font.render("TIME'S UP!", True, WHITE)
            score_text = self.large_font.render(f"Score: {self.score}", True, GOLD)
            
            self.screen.blit(game_over_text, 
                           (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 
                            SCREEN_HEIGHT//2 - 80))
            self.screen.blit(score_text, 
                           (SCREEN_WIDTH//2 - score_text.get_width()//2, 
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
