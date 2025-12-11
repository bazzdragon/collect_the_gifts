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

class Gift:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 30
        self.color = RED
        self.vx = random.uniform(GIFT_VELOCITY_MIN, GIFT_VELOCITY_MAX)  # Slow horizontal velocity
        self.vy = random.uniform(GIFT_VELOCITY_MIN, GIFT_VELOCITY_MAX)  # Slow vertical velocity
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
        # Draw ribbon (cross)
        pygame.draw.line(screen, GOLD, 
                        (self.x - self.size//2, self.y), 
                        (self.x + self.size//2, self.y), 3)
        pygame.draw.line(screen, GOLD, 
                        (self.x, self.y - self.size//2), 
                        (self.x, self.y + self.size//2), 3)
    
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
        self.size = 60
        self.color = GREEN
    
    def draw(self, screen):
        # Draw Santa's bag
        pygame.draw.ellipse(screen, self.color, 
                           (self.x - self.size//2, self.y - self.size//2, 
                            self.size, self.size))
        # Draw opening (darker green)
        pygame.draw.ellipse(screen, (0, 150, 0), 
                           (self.x - self.size//3, self.y - self.size//2, 
                            self.size//1.5, self.size//3))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Collect the Gifts")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)
        
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mx, my = event.pos
                    # Check if clicked on a gift
                    for gift in self.gifts:
                        if gift.contains_point(mx, my):
                            self.dragging_gift = gift
                            gift.being_dragged = True
                            break
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.dragging_gift:
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
                if self.dragging_gift:
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
