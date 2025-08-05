import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions (portrait)
WIDTH, HEIGHT = 720, 960
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Falling Block Game")

# Colors
BG_COLOR = (20, 20, 30)
PLAYER_COLOR = (255, 220, 40)
WALL_COLOR = (100, 100, 120)

# Well wall properties
WALL_WIDTH = 30

BRICK_COLOR = (120, 110, 140)
MORTAR_COLOR = (60, 60, 80)
BRICK_WIDTH = WALL_WIDTH
BRICK_HEIGHT = 40

# Player properties
PLAYER_SIZE = 60
PLAYER_GROWTH = 32  # How much the player grows per hit
# Update player_x to start inside the well
player_x = WALL_WIDTH + (WIDTH - 2 * WALL_WIDTH) // 2 - PLAYER_SIZE // 2
# Add target_x for smooth movement
player_target_x = player_x
# Start player at the original Y position
player_y = 180  # Slightly lower
player_speed = 14
# Animation speed (pixels per frame)
PLAYER_ANIMATION_SPEED = 24
# Player fall speed
PLAYER_FALL_SPEED = 7

# Track current player size
player_size = PLAYER_SIZE

# Brick wall animation offset
brick_wall_offset = 0

# Clock for FPS
clock = pygame.time.Clock()
FPS = 60

# Obstacle properties
OBSTACLE_MIN_WIDTH = 80
OBSTACLE_MAX_WIDTH = 200
OBSTACLE_HEIGHT = 40
OBSTACLE_MIN_SPEED = 10
OBSTACLE_MAX_SPEED = 18
OBSTACLE_SPAWN_INTERVAL_MIN = 700  # ms
OBSTACLE_SPAWN_INTERVAL_MAX = 1300  # ms

obstacles = []
last_obstacle_time = pygame.time.get_ticks()
next_obstacle_interval = random.randint(OBSTACLE_SPAWN_INTERVAL_MIN, OBSTACLE_SPAWN_INTERVAL_MAX)

# Scoring
score = 0
font = pygame.font.SysFont(None, 60)

# Game state
game_over = False
fall_speed = 5  # Initial background/score speed
fall_acceleration = 0.002  # Speed up per frame

# Hit counter for collisions
player_hits = 0
MAX_HITS = 10

# Main game loop
running = True
SHRINKBLOCK_SIZE = 40
SHRINKBLOCK_COLOR = (60, 220, 220)  # Cyan
SHRINKBLOCK_FLASH_COLOR = (220, 60, 220)  # Magenta (not used elsewhere)
SHRINKBLOCK_SPAWN_INTERVAL_MIN = 4080  # ms (15% faster)
SHRINKBLOCK_SPAWN_INTERVAL_MAX = 8160   # ms (15% faster)
shrinkblocks = []
last_shrinkblock_time = pygame.time.get_ticks()
next_shrinkblock_interval = random.randint(SHRINKBLOCK_SPAWN_INTERVAL_MIN, SHRINKBLOCK_SPAWN_INTERVAL_MAX)

# Flash/invincible state
invincible = False
invincible_timer = 0
INVINCIBLE_FLASH_INTERVAL = 200  # ms
last_flash_time = 0
flash_toggle = False

# Invincibility speed/score multiplier
INVINCIBLE_SPEED_MULT = 4.0
INVINCIBLE_SCORE_MULT = 4.0
normal_fall_speed = None

REVERSEBLOCK_SIZE = 40
REVERSEBLOCK_COLOR = (120, 0, 0)  # Dark red
REVERSEBLOCK_PLAYER_COLOR = (200, 0, 80)  # Magenta-red for player during effect
REVERSEBLOCK_SPAWN_INTERVAL_MIN = 10800  # ms (40% faster)
REVERSEBLOCK_SPAWN_INTERVAL_MAX = 19200  # ms (40% faster)
reverseblocks = []
last_reverseblock_time = pygame.time.get_ticks()
next_reverseblock_interval = random.randint(REVERSEBLOCK_SPAWN_INTERVAL_MIN, REVERSEBLOCK_SPAWN_INTERVAL_MAX)

# Reverse control state
reverse_controls = False
reverse_timer = 0
REVERSE_DURATION = 7000  # ms
reverse_angle = 0
REVERSE_SPIN_SPEED = 12  # degrees per frame

# Explosion effect for player block
exploding = False
explosion_fragments = []
EXPLOSION_DURATION = 900  # ms
explosion_timer = 0
FRAGMENTS_PER_ROW = 4
FRAGMENTS_PER_COL = 4

BRICKBREAKER_SIZE = 40
BRICKBREAKER_COLOR = (60, 220, 60)  # Bright green
BRICKBREAKER_SPAWN_INTERVAL_MIN = 4080  # ms (same as shrinkBlock, 15% faster)
BRICKBREAKER_SPAWN_INTERVAL_MAX = 8160  # ms (same as shrinkBlock, 15% faster)
BRICK_BREAKER_SCORE_BONUS_DISPLAY = 500  # How much the displayed score should increase
BRICK_BREAKER_SCORE_BONUS = BRICK_BREAKER_SCORE_BONUS_DISPLAY * 100  # Internal score units
brickbreakers = []
last_brickbreaker_time = pygame.time.get_ticks()
next_brickbreaker_interval = random.randint(BRICKBREAKER_SPAWN_INTERVAL_MIN, BRICKBREAKER_SPAWN_INTERVAL_MAX)

# Brick breaker state
brick_breaker = False
brick_breaker_timer = 0
BRICK_BREAKER_DURATION = 10000  # ms

# Obstacle explosion effect for brick breaker
obstacle_explosions = []
OBSTACLE_EXPLOSION_DURATION = 350  # ms (faster than game over)
OBSTACLE_FRAGMENTS = 6

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Restart game
                player_x = WALL_WIDTH + (WIDTH - 2 * WALL_WIDTH) // 2 - PLAYER_SIZE // 2
                player_target_x = player_x
                player_y = 180
                brick_wall_offset = 0
                obstacles.clear()
                shrinkblocks.clear()
                reverseblocks.clear()
                brickbreakers.clear()
                score = 0
                fall_speed = 5
                last_obstacle_time = pygame.time.get_ticks()
                next_obstacle_interval = random.randint(OBSTACLE_SPAWN_INTERVAL_MIN, OBSTACLE_SPAWN_INTERVAL_MAX)
                last_shrinkblock_time = pygame.time.get_ticks()
                next_shrinkblock_interval = random.randint(SHRINKBLOCK_SPAWN_INTERVAL_MIN, SHRINKBLOCK_SPAWN_INTERVAL_MAX)
                last_reverseblock_time = pygame.time.get_ticks()
                next_reverseblock_interval = random.randint(REVERSEBLOCK_SPAWN_INTERVAL_MIN, REVERSEBLOCK_SPAWN_INTERVAL_MAX)
                last_brickbreaker_time = pygame.time.get_ticks()
                next_brickbreaker_interval = random.randint(BRICKBREAKER_SPAWN_INTERVAL_MIN, BRICKBREAKER_SPAWN_INTERVAL_MAX)
                game_over = False
                player_size = PLAYER_SIZE
                player_hits = 0
                invincible = False
                invincible_timer = 0
                last_flash_time = 0
                flash_toggle = False
                reverse_controls = False
                reverse_timer = 0
                reverse_angle = 0
                exploding = False
                explosion_fragments = []
                explosion_timer = 0
                brick_breaker = False
                brick_breaker_timer = 0
                obstacle_explosions = []

    if not game_over:
        # Key states for smooth movement
        keys = pygame.key.get_pressed()
        if not reverse_controls:
            if keys[pygame.K_LEFT]:
                # Move target left by one step
                new_target = player_target_x - player_speed
                player_target_x = max(WALL_WIDTH, min(WIDTH - WALL_WIDTH - player_size, new_target))
            if keys[pygame.K_RIGHT]:
                # Move target right by one step
                new_target = player_target_x + player_speed
                player_target_x = max(WALL_WIDTH, min(WIDTH - WALL_WIDTH - player_size, new_target))
        else:
            if keys[pygame.K_LEFT]:
                # Reversed: left key moves right
                new_target = player_target_x + player_speed
                player_target_x = max(WALL_WIDTH, min(WIDTH - WALL_WIDTH - player_size, new_target))
            if keys[pygame.K_RIGHT]:
                # Reversed: right key moves left
                new_target = player_target_x - player_speed
                player_target_x = max(WALL_WIDTH, min(WIDTH - WALL_WIDTH - player_size, new_target))
        # Animate player_x towards player_target_x
        if player_x < player_target_x:
            player_x = min(player_x + PLAYER_ANIMATION_SPEED, player_target_x)
        elif player_x > player_target_x:
            player_x = max(player_x - PLAYER_ANIMATION_SPEED, player_target_x)

        # Move the brick wall offset upward to maintain the falling illusion
        if invincible and invincible_timer > 500:
            brick_wall_offset = (brick_wall_offset + int(PLAYER_FALL_SPEED * INVINCIBLE_SPEED_MULT)) % BRICK_HEIGHT
        else:
            brick_wall_offset = (brick_wall_offset + PLAYER_FALL_SPEED) % BRICK_HEIGHT

        # Restore obstacle spawning (obstacles move upward)
        now = pygame.time.get_ticks()
        if now - last_obstacle_time > next_obstacle_interval:
            obs_width = random.randint(OBSTACLE_MIN_WIDTH, OBSTACLE_MAX_WIDTH)
            obs_x = random.randint(WALL_WIDTH, WIDTH - WALL_WIDTH - obs_width)
            obs_speed = random.randint(OBSTACLE_MIN_SPEED, OBSTACLE_MAX_SPEED) + int(fall_speed)
            # Spawn at the bottom
            obstacles.append({
                'rect': pygame.Rect(obs_x, HEIGHT, obs_width, OBSTACLE_HEIGHT),
                'speed': obs_speed
            })
            last_obstacle_time = now
            next_obstacle_interval = random.randint(OBSTACLE_SPAWN_INTERVAL_MIN, OBSTACLE_SPAWN_INTERVAL_MAX)

        # Spawn shrinkBlocks much less frequently
        if now - last_shrinkblock_time > next_shrinkblock_interval:
            shrink_x = random.randint(WALL_WIDTH, WIDTH - WALL_WIDTH - SHRINKBLOCK_SIZE)
            shrink_speed = random.randint(OBSTACLE_MIN_SPEED, OBSTACLE_MAX_SPEED) + int(fall_speed)
            shrinkblocks.append({
                'rect': pygame.Rect(shrink_x, HEIGHT, SHRINKBLOCK_SIZE, SHRINKBLOCK_SIZE),
                'speed': shrink_speed
            })
            last_shrinkblock_time = now
            next_shrinkblock_interval = random.randint(SHRINKBLOCK_SPAWN_INTERVAL_MIN, SHRINKBLOCK_SPAWN_INTERVAL_MAX)

        # Spawn reverseBlocks much less frequently
        if now - last_reverseblock_time > next_reverseblock_interval:
            rev_x = random.randint(WALL_WIDTH, WIDTH - WALL_WIDTH - REVERSEBLOCK_SIZE)
            rev_speed = random.randint(OBSTACLE_MIN_SPEED, OBSTACLE_MAX_SPEED) + int(fall_speed)
            reverseblocks.append({
                'rect': pygame.Rect(rev_x, HEIGHT, REVERSEBLOCK_SIZE, REVERSEBLOCK_SIZE),
                'speed': rev_speed
            })
            last_reverseblock_time = now
            next_reverseblock_interval = random.randint(REVERSEBLOCK_SPAWN_INTERVAL_MIN, REVERSEBLOCK_SPAWN_INTERVAL_MAX)

        # Spawn brickBreakers at a similar rate to shrinkBlocks
        if now - last_brickbreaker_time > next_brickbreaker_interval:
            bb_x = random.randint(WALL_WIDTH, WIDTH - WALL_WIDTH - BRICKBREAKER_SIZE)
            bb_speed = random.randint(OBSTACLE_MIN_SPEED, OBSTACLE_MAX_SPEED) + int(fall_speed)
            brickbreakers.append({
                'rect': pygame.Rect(bb_x, HEIGHT, BRICKBREAKER_SIZE, BRICKBREAKER_SIZE),
                'speed': bb_speed
            })
            last_brickbreaker_time = now
            next_brickbreaker_interval = random.randint(BRICKBREAKER_SPAWN_INTERVAL_MIN, BRICKBREAKER_SPAWN_INTERVAL_MAX)

        # Move brickBreakers upward
        for bb in brickbreakers:
            bb['rect'].y -= bb['speed']
        brickbreakers = [bb for bb in brickbreakers if bb['rect'].y + BRICKBREAKER_SIZE > 0]

        # Move obstacles upward
        for obs in obstacles:
            obs['rect'].y -= obs['speed']
        obstacles = [obs for obs in obstacles if obs['rect'].y + OBSTACLE_HEIGHT > 0]

        # Move shrinkBlocks upward
        for sb in shrinkblocks:
            sb['rect'].y -= sb['speed']
        shrinkblocks = [sb for sb in shrinkblocks if sb['rect'].y + SHRINKBLOCK_SIZE > 0]

        # Move reverseBlocks upward
        for rb in reverseblocks:
            rb['rect'].y -= rb['speed']
        reverseblocks = [rb for rb in reverseblocks if rb['rect'].y + REVERSEBLOCK_SIZE > 0]

        # Collision detection
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        # --- shrinkBlock collision ---
        for sb in shrinkblocks:
            if player_rect.colliderect(sb['rect']):
                if player_size > PLAYER_SIZE:
                    player_size -= PLAYER_GROWTH
                    player_x += PLAYER_GROWTH // 2
                    player_y += PLAYER_GROWTH // 2
                else:
                    # Already at minimum size: trigger/extend invincible state
                    invincible = True
                    invincible_timer = 10000 if invincible_timer == 0 else invincible_timer + 10000
                    last_flash_time = now
                shrinkblocks.remove(sb)
                break
        # --- obstacle collision ---
        if not invincible and not brick_breaker:
            for obs in obstacles:
                if player_rect.colliderect(obs['rect']):
                    player_size += PLAYER_GROWTH
                    player_x -= PLAYER_GROWTH // 2
                    player_y -= PLAYER_GROWTH // 2
                    player_hits += 1
                    if player_hits >= MAX_HITS:
                        game_over = True
                        # Trigger explosion effect
                        exploding = True
                        explosion_fragments = []
                        explosion_timer = EXPLOSION_DURATION
                        frag_size = player_size // FRAGMENTS_PER_ROW
                        for i in range(FRAGMENTS_PER_ROW):
                            for j in range(FRAGMENTS_PER_COL):
                                frag_x = player_x + i * frag_size
                                frag_y = player_y + j * frag_size
                                angle = random.uniform(0, 2 * 3.14159)
                                speed = random.uniform(7, 15)
                                dx = speed * math.cos(angle)
                                dy = speed * math.sin(angle)
                                explosion_fragments.append({
                                    'rect': pygame.Rect(frag_x, frag_y, frag_size, frag_size),
                                    'dx': dx,
                                    'dy': dy,
                                    'color': PLAYER_COLOR,
                                    'alpha': 255
                                })
                    obstacles.remove(obs)
                    break
        elif brick_breaker:
            for obs in obstacles:
                if player_rect.colliderect(obs['rect']):
                    # Trigger fast obstacle explosion
                    frag_size = max(8, obs['rect'].width // 3)
                    for _ in range(OBSTACLE_FRAGMENTS):
                        angle = random.uniform(0, 2 * 3.14159)
                        speed = random.uniform(15, 28)
                        dx = speed * math.cos(angle)
                        dy = speed * math.sin(angle)
                        frag_rect = pygame.Rect(obs['rect'].centerx, obs['rect'].centery, frag_size, frag_size)
                        obstacle_explosions.append({
                            'rect': frag_rect,
                            'dx': dx,
                            'dy': dy,
                            'color': (200, 60, 60),
                            'alpha': 255,
                            'timer': OBSTACLE_EXPLOSION_DURATION
                        })
                    obstacles.remove(obs)
                    score += BRICK_BREAKER_SCORE_BONUS
                    break

        # --- brickBreaker collision ---
        for bb in brickbreakers:
            if player_rect.colliderect(bb['rect']):
                brick_breaker = True
                brick_breaker_timer = BRICK_BREAKER_DURATION if brick_breaker_timer == 0 else brick_breaker_timer + BRICK_BREAKER_DURATION
                invincible = True
                invincible_timer = 0
                brickbreakers.remove(bb)
                break

        # --- brick breaker timer logic ---
        if brick_breaker:
            brick_breaker_timer -= clock.get_time()
            if brick_breaker_timer <= 0:
                brick_breaker = False
                brick_breaker_timer = 0
                invincible = False

        # --- obstacle explosion animation update ---
        for frag in obstacle_explosions:
            frag['rect'].x += int(frag['dx'])
            frag['rect'].y += int(frag['dy'])
            frag['alpha'] = max(0, frag['alpha'] - int(255 * (clock.get_time() / OBSTACLE_EXPLOSION_DURATION)))
            frag['timer'] -= clock.get_time()
        obstacle_explosions = [frag for frag in obstacle_explosions if frag['timer'] > 0]

        # --- invincible timer/flash logic ---
        if invincible:
            # Speed up game and score during invincibility, but return to normal speed for last 0.5s
            if normal_fall_speed is None:
                normal_fall_speed = fall_speed
            if invincible_timer > 500:
                fall_speed = normal_fall_speed * INVINCIBLE_SPEED_MULT
            else:
                fall_speed = normal_fall_speed
            invincible_timer -= clock.get_time()
            if invincible_timer <= 0:
                invincible = False
                invincible_timer = 0
                flash_toggle = False
                # Restore normal speed
                fall_speed = normal_fall_speed
                normal_fall_speed = None
            else:
                if now - last_flash_time > INVINCIBLE_FLASH_INTERVAL:
                    flash_toggle = not flash_toggle
                    last_flash_time = now

        # During brick breaker, player is invulnerable
        if brick_breaker:
            invincible = True
            invincible_timer = 0

        # --- reverseBlock collision ---
        for rb in reverseblocks:
            if player_rect.colliderect(rb['rect']):
                reverse_controls = True
                reverse_timer = REVERSE_DURATION if reverse_timer == 0 else reverse_timer + REVERSE_DURATION
                reverseblocks.remove(rb)
                break

        # --- reverse timer logic ---
        if reverse_controls:
            reverse_timer -= clock.get_time()
            reverse_angle = (reverse_angle + REVERSE_SPIN_SPEED) % 360
            if reverse_timer <= 0:
                reverse_controls = False
                reverse_timer = 0
                reverse_angle = 0

        # Update score and speed
        if invincible and invincible_timer > 500:
            score += int(fall_speed * INVINCIBLE_SCORE_MULT)
        else:
            score += int(fall_speed)
        if not invincible or (invincible and invincible_timer <= 500):
            fall_speed += fall_acceleration

    # Draw background
    screen.fill(BG_COLOR)

    # Draw well sides (walls)
    for i in range(0, HEIGHT // BRICK_HEIGHT + 2):
        y = i * BRICK_HEIGHT - brick_wall_offset
        # Offset every other row for a brick pattern
        offset = 0 if (i % 2 == 0) else BRICK_WIDTH // 4
        # Left wall brick
        pygame.draw.rect(screen, BRICK_COLOR, (0, y, BRICK_WIDTH, BRICK_HEIGHT))
        # Mortar lines (horizontal)
        pygame.draw.line(screen, MORTAR_COLOR, (0, y), (BRICK_WIDTH, y), 2)
        # Mortar lines (vertical, only if offset)
        if offset:
            pygame.draw.line(screen, MORTAR_COLOR, (offset, y), (offset, y + BRICK_HEIGHT), 2)
        # Right wall brick
        pygame.draw.rect(screen, BRICK_COLOR, (WIDTH - BRICK_WIDTH, y, BRICK_WIDTH, BRICK_HEIGHT))
        pygame.draw.line(screen, MORTAR_COLOR, (WIDTH - BRICK_WIDTH, y), (WIDTH, y), 2)
        if offset:
            pygame.draw.line(screen, MORTAR_COLOR, (WIDTH - BRICK_WIDTH + offset, y), (WIDTH - BRICK_WIDTH + offset, y + BRICK_HEIGHT), 2)

    # Draw obstacles
    for obs in obstacles:
        pygame.draw.rect(screen, (200, 60, 60), obs['rect'])

    # Draw shrinkBlocks
    for sb in shrinkblocks:
        pygame.draw.rect(screen, SHRINKBLOCK_COLOR, sb['rect'])

    # Draw reverseBlocks
    for rb in reverseblocks:
        pygame.draw.rect(screen, REVERSEBLOCK_COLOR, rb['rect'])

    # Draw brickBreakers
    for bb in brickbreakers:
        pygame.draw.rect(screen, BRICKBREAKER_COLOR, bb['rect'])

    # Draw obstacle explosions
    for frag in obstacle_explosions:
        surf = pygame.Surface((frag['rect'].width, frag['rect'].height), pygame.SRCALPHA)
        surf.fill(frag['color'] + (frag['alpha'],))
        screen.blit(surf, frag['rect'].topleft)

    # Draw player
    if exploding and explosion_timer > 0:
        # Animate explosion fragments
        for frag in explosion_fragments:
            frag['rect'].x += int(frag['dx'])
            frag['rect'].y += int(frag['dy'])
            frag['alpha'] = max(0, frag['alpha'] - int(255 * (clock.get_time() / EXPLOSION_DURATION)))
            surf = pygame.Surface((frag['rect'].width, frag['rect'].height), pygame.SRCALPHA)
            surf.fill(frag['color'] + (frag['alpha'],))
            screen.blit(surf, frag['rect'].topleft)
        explosion_timer -= clock.get_time()
    elif brick_breaker:
        # Draw spikey ball (circle with spikes)
        center = (player_x + player_size // 2, player_y + player_size // 2)
        radius = player_size // 2
        spike_len = player_size // 3
        spike_count = 12
        # Draw main ball
        pygame.draw.circle(screen, BRICKBREAKER_COLOR, center, radius)
        # Draw spikes
        for i in range(spike_count):
            angle = 2 * math.pi * i / spike_count
            x1 = int(center[0] + radius * math.cos(angle))
            y1 = int(center[1] + radius * math.sin(angle))
            x2 = int(center[0] + (radius + spike_len) * math.cos(angle))
            y2 = int(center[1] + (radius + spike_len) * math.sin(angle))
            pygame.draw.line(screen, (255,255,255), (x1, y1), (x2, y2), 3)
    elif reverse_controls:
        # Draw spinning, colored player block
        surf = pygame.Surface((player_size, player_size), pygame.SRCALPHA)
        surf.fill(REVERSEBLOCK_PLAYER_COLOR)
        rotated = pygame.transform.rotate(surf, reverse_angle)
        rect = rotated.get_rect(center=(player_x + player_size // 2, player_y + player_size // 2))
        screen.blit(rotated, rect.topleft)
    elif invincible and flash_toggle:
        pygame.draw.rect(screen, SHRINKBLOCK_FLASH_COLOR, (player_x, player_y, player_size, player_size))
    elif not exploding:
        pygame.draw.rect(screen, PLAYER_COLOR, (player_x, player_y, player_size, player_size))

    # Draw score
    score_text = font.render(f"Score: {score // 100}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

    # Game Over screen
    if game_over:
        over_text = font.render("GAME OVER", True, (255, 80, 80))
        restart_text = font.render("Press R to Restart", True, (255, 255, 255))
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 80))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit() 