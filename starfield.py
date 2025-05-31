import pygame
import random
import math
import sys

# --- Initialize Pygame ---
pygame.init()

# --- Screen Dimensions ---
SCREEN_WIDTH = 1280  # Increased default width
SCREEN_HEIGHT = 800  # Increased default height
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dynamic Tech Display")

# --- Colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
TRANSPARENT_BLACK = (0, 0, 0, 10) # For binary trail

# --- Global Settings ---
global_speed_multiplier = 1.0 # Affects all modes
FPS = 60 # Frames per second

# --- Modes ---
MODE_STARS = 0
MODE_PIPES = 1
MODE_BINARY = 2

current_mode = MODE_STARS
transitioning = False
transition_alpha = 0 # For fade effect (0 to 255)
transition_speed = 5 # How fast the fade happens

# --- Mode Customization Variables ---

# --- Stars Mode ---
NUM_STARS = 600 # Increased default number of stars
STARS_LIST = []
STAR_DENSITY = 1.0 # Controls how many stars are generated (1.0 is default)

TECH_STAR_COLORS = [
    (150, 200, 255), # Light Blue
    (100, 255, 150), # Light Green
    (255, 180, 100), # Light Orange
    (200, 200, 255), # Lavender
    (255, 255, 255)  # White
]

STAR_VIEW_DISTANCE = 1200 # How far the stars initially are in Z
STAR_FOCAL_LENGTH = 350   # Controls the perspective effect (higher = stronger perspective)
STAR_Z_RESET = STAR_VIEW_DISTANCE + 200 # Z value when a star resets to the back

NEBULA_ELEMENTS = []
NUM_NEBULAE = 10 # More nebulae
NEBULA_PALETTES = [
    [(30, 30, 60, 40), (60, 60, 100, 60)],  # Dark Blue/Purple
    [(30, 60, 30, 40), (60, 100, 60, 60)],  # Dark Green
    [(60, 30, 30, 40), (100, 60, 60, 60)],  # Dark Red
    [(50, 50, 50, 40), (80, 80, 80, 60)],   # Grayscale
    [(0, 40, 40, 40), (0, 80, 80, 60)]      # Dark Cyan
]
nebula_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
current_nebula_palette = random.choice(NEBULA_PALETTES)

def init_stars_mode():
    global STARS_LIST, current_nebula_palette, NEBULA_ELEMENTS
    STARS_LIST = []
    for _ in range(NUM_STARS):
        star = create_star_data()
        if star:
            STARS_LIST.append(star)
    current_nebula_palette = random.choice(NEBULA_PALETTES)
    NEBULA_ELEMENTS = []
    for _ in range(NUM_NEBULAE):
        nebula_color = random.choice(current_nebula_palette)
        nebula_radius = random.randint(150, 400)
        nebula_x = random.randint(0, SCREEN_WIDTH)
        nebula_y = random.randint(0, SCREEN_HEIGHT)
        NEBULA_ELEMENTS.append({'pos': (nebula_x, nebula_y), 'radius': nebula_radius, 'color': nebula_color})

def create_star_data():
    if random.random() > STAR_DENSITY:
        return None
    x = random.uniform(-SCREEN_WIDTH / 2, SCREEN_WIDTH / 2)
    y = random.uniform(-SCREEN_HEIGHT / 2, SCREEN_HEIGHT / 2)
    z = random.uniform(50, STAR_VIEW_DISTANCE)
    base_speed = random.uniform(0.5, 3.0)
    shape_type = random.choice(['circle', 'square'])
    size_factor = random.uniform(0.8, 2.5)
    color = random.choice(TECH_STAR_COLORS)
    return {'x': x, 'y': y, 'z': z, 'base_speed': base_speed,
            'shape': shape_type, 'size_factor': size_factor, 'color': color}

def get_flicker_brightness(base_brightness):
    return base_brightness * random.uniform(0.8, 1.2)

def update_stars_mode():
    stars_to_remove = [] # List to hold stars to remove
    for i, star in enumerate(STARS_LIST):
        star['z'] -= star['base_speed'] * global_speed_multiplier
        if star['z'] <= 1:
            new_star = create_star_data()
            if new_star:
                STARS_LIST[i] = new_star
            else: # If new star creation was skipped due to density
                stars_to_remove.append(i) # Mark for removal
            
    # Remove stars in reverse order to avoid index issues
    for i in reversed(stars_to_remove):
        del STARS_LIST[i]
    
    # Add new stars to maintain density if some were removed
    while len(STARS_LIST) < NUM_STARS * STAR_DENSITY: # Aim for NUM_STARS * DENSITY
        star = create_star_data()
        if star:
            STARS_LIST.append(star)


def draw_stars_mode(screen):
    # Draw nebulas (draw on a separate surface for transparency)
    nebula_surface.fill((0,0,0,0)) # Clear previous nebula drawings
    for nebula in NEBULA_ELEMENTS:
        # Ensure nebula color is RGBA for pygame.SRCALPHA surface
        if len(nebula['color']) == 3: # If RGB, add a default alpha
            nebula_draw_color = nebula['color'] + (255,)
        else:
            nebula_draw_color = nebula['color']
        pygame.draw.circle(nebula_surface, nebula_draw_color, nebula['pos'], nebula['radius'])
    screen.blit(nebula_surface, (0,0))

    # Update and Draw Stars
    for star in STARS_LIST:
        screen_x = int((star['x'] / star['z']) * STAR_FOCAL_LENGTH + SCREEN_WIDTH / 2)
        screen_y = int((star['y'] / star['z']) * STAR_FOCAL_LENGTH + SCREEN_HEIGHT / 2)
        projected_size = max(1, int(star['size_factor'] * STAR_FOCAL_LENGTH / star['z']))
        base_brightness_factor = max(0.1, min(1.0, STAR_FOCAL_LENGTH / star['z']))
        brightness_factor = get_flicker_brightness(base_brightness_factor)

        # Calculate final RGB color components (ensure it's an RGB tuple)
        current_color_rgb = (
            int(star['color'][0] * brightness_factor),
            int(star['color'][1] * brightness_factor),
            int(star['color'][2] * brightness_factor)
        )
        # Clamp color values to 0-255 just in case
        current_color_rgb = (
            min(255, max(0, current_color_rgb[0])),
            min(255, max(0, current_color_rgb[1])),
            min(255, max(0, current_color_rgb[2]))
        )

        if -projected_size < screen_x < SCREEN_WIDTH + projected_size and \
           -projected_size < screen_y < SCREEN_HEIGHT + projected_size:
            if star['shape'] == 'circle':
                pygame.draw.circle(screen, current_color_rgb, (screen_x, screen_y), projected_size)
            elif star['shape'] == 'square':
                rect_x = screen_x - projected_size // 2
                rect_y = screen_y - projected_size // 2
                pygame.draw.rect(screen, current_color_rgb, (rect_x, rect_y, projected_size, projected_size))

# --- Pipes Mode ---
PIPE_COLOR = (0, 255, 255) # Cyan
PIPE_COLOR_ALT = (0, 150, 200) # Darker Cyan for segments
PIPE_THICKNESS = 3
PIPE_MAX_LENGTH = 150
PIPE_MIN_LENGTH = 50
PIPE_SPAWN_INTERVAL = 30 # Frames between new pipes
PIPE_LIFETIME = 300 # Frames
PIPES_LIST = []
pipe_spawn_timer = 0

def init_pipes_mode():
    global PIPES_LIST, pipe_spawn_timer
    PIPES_LIST = []
    pipe_spawn_timer = 0

def create_pipe_segment(x, y, length, angle, color, thickness, lifetime):
    return {
        'start_pos': (x, y),
        'end_pos': (x + length * math.cos(angle), y + length * math.sin(angle)),
        'length': length,
        'angle': angle,
        'color': color,
        'thickness': thickness,
        'lifetime': lifetime,
        'current_lifetime': 0
    }

def update_pipes_mode():
    global pipe_spawn_timer
    pipe_spawn_timer += 1
    if pipe_spawn_timer >= PIPE_SPAWN_INTERVAL / global_speed_multiplier:
        pipe_spawn_timer = 0
        side = random.choice(['left', 'right', 'top', 'bottom'])
        if side == 'left':
            x = 0
            y = random.randint(0, SCREEN_HEIGHT)
            angle = random.uniform(-math.pi / 4, math.pi / 4) # Mostly right
        elif side == 'right':
            x = SCREEN_WIDTH
            y = random.randint(0, SCREEN_HEIGHT)
            angle = random.uniform(3 * math.pi / 4, 5 * math.pi / 4) # Mostly left
        elif side == 'top':
            x = random.randint(0, SCREEN_WIDTH)
            y = 0
            angle = random.uniform(math.pi / 4, 3 * math.pi / 4) # Mostly down
        else: # bottom
            x = random.randint(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT
            angle = random.uniform(-3 * math.pi / 4, -math.pi / 4) # Mostly up

        length = random.uniform(PIPE_MIN_LENGTH, PIPE_MAX_LENGTH)
        thickness = random.randint(PIPE_THICKNESS - 1, PIPE_THICKNESS + 1)
        PIPES_LIST.append(create_pipe_segment(x, y, length, angle, PIPE_COLOR, thickness, PIPE_LIFETIME))

    pipes_to_remove = []
    for pipe in PIPES_LIST:
        pipe['current_lifetime'] += 1
        if pipe['current_lifetime'] >= pipe['lifetime']:
            pipes_to_remove.append(pipe)
            continue

        # Move the pipe segment
        move_amount = 3 * global_speed_multiplier
        pipe['start_pos'] = (pipe['start_pos'][0] + move_amount * math.cos(pipe['angle']),
                             pipe['start_pos'][1] + move_amount * math.sin(pipe['angle']))
        pipe['end_pos'] = (pipe['end_pos'][0] + move_amount * math.cos(pipe['angle']),
                           pipe['end_pos'][1] + move_amount * math.sin(pipe['angle']))

        # Optionally, create a new segment at the head to extend the pipe
        if random.random() < 0.1 * global_speed_multiplier: # Chance to grow
            new_angle = pipe['angle'] + random.uniform(-math.pi/8, math.pi/8) # Slight turn
            new_length = random.uniform(10, 30)
            PIPES_LIST.append(create_pipe_segment(pipe['end_pos'][0], pipe['end_pos'][1],
                                                    new_length, new_angle, PIPE_COLOR_ALT,
                                                    pipe['thickness'], pipe['lifetime'] // 2)) # Shorter tail segments

    for pipe in pipes_to_remove:
        if pipe in PIPES_LIST: # Check if it hasn't been removed by new segment creation
            PIPES_LIST.remove(pipe)

def draw_pipes_mode(screen):
    for pipe in PIPES_LIST:
        alpha = 255 * (1 - pipe['current_lifetime'] / pipe['lifetime'])
        color = (pipe['color'][0], pipe['color'][1], pipe['color'][2], int(alpha))
        # Use a temporary surface for drawing with alpha
        temp_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.line(temp_surf, color, pipe['start_pos'], pipe['end_pos'], pipe['thickness'])
        screen.blit(temp_surf, (0,0))


# --- Binary Mode ---
FONT_SIZE = 24
BINARY_COLUMN_WIDTH = FONT_SIZE
BINARY_DROP_SPEED_MIN = 2
BINARY_DROP_SPEED_MAX = 5
BINARY_TEXT_COLORS = [
    (0, 255, 0),    # Bright Green
    (50, 200, 50),  # Medium Green
    (100, 255, 100) # Light Green
]
BINARY_ACTIVE_COLOR = (255, 255, 255) # White for the leading character
BINARY_TRAIL_LENGTH = 20 # How many characters in a column
BINARY_CHARS_PER_COLUMN = math.ceil(SCREEN_HEIGHT / FONT_SIZE) # Max chars in a column

font = pygame.font.Font(None, FONT_SIZE)

# Initialize binary_columns for the first time
binary_columns = []
def init_binary_columns_data():
    global binary_columns
    binary_columns = []
    for i in range(SCREEN_WIDTH // BINARY_COLUMN_WIDTH):
        binary_columns.append({
            'x': i * BINARY_COLUMN_WIDTH,
            'y': random.randint(-SCREEN_HEIGHT, 0), # Start off-screen
            'speed': random.uniform(BINARY_DROP_SPEED_MIN, BINARY_DROP_SPEED_MAX),
            'chars': [random.choice(['0', '1']) for _ in range(BINARY_TRAIL_LENGTH + BINARY_CHARS_PER_COLUMN * 2)], # Pre-generate characters
            'current_char_index': random.randint(0, BINARY_CHARS_PER_COLUMN * 2 - 1) # Random start char
        })

def init_binary_mode():
    init_binary_columns_data() # Call the helper to re-initialize

def update_binary_mode():
    for column in binary_columns:
        column['y'] += column['speed'] * global_speed_multiplier
        # When column goes off screen, reset its position and speed
        if column['y'] - (BINARY_TRAIL_LENGTH + 1) * FONT_SIZE > SCREEN_HEIGHT: # Adjusted reset point
            column['y'] = random.randint(-SCREEN_HEIGHT // 2, 0) # Reset to top half of screen (or just above)
            column['speed'] = random.uniform(BINARY_DROP_SPEED_MIN, BINARY_DROP_SPEED_MAX)
            column['current_char_index'] = random.randint(0, len(column['chars']) - 1) # Reset char index to a random point


def draw_binary_mode(screen):
    # Draw a transparent black rectangle over the entire screen to create the "trail" effect
    # This needs to be drawn on the main screen each frame to create the fading effect
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    fade_surface.fill(TRANSPARENT_BLACK)
    screen.blit(fade_surface, (0, 0))

    for column in binary_columns:
        for i in range(BINARY_TRAIL_LENGTH):
            char_y = int(column['y']) - i * FONT_SIZE # Cast to int for drawing
            
            # Only draw if character is within screen bounds (roughly)
            if char_y < -FONT_SIZE or char_y > SCREEN_HEIGHT:
                continue

            char_index = (column['current_char_index'] - i) % len(column['chars'])
            char = column['chars'][char_index]

            if i == 0: # Leading character is active color
                text_color = BINARY_ACTIVE_COLOR
            else: # Trailing characters get dimmer
                # Distribute trail colors evenly across the trail length
                color_idx_float = (i / BINARY_TRAIL_LENGTH) * (len(BINARY_TEXT_COLORS) - 1)
                color_idx = int(color_idx_float)
                
                # Interpolate between colors for smoother fade, if desired
                # For simplicity here, we'll just pick the nearest color
                text_color = BINARY_TEXT_COLORS[color_idx]

            text_surface = font.render(char, True, text_color)
            screen.blit(text_surface, (column['x'], char_y))

# --- Transition Function ---
def start_transition(next_mode_val):
    global transitioning, transition_alpha, next_mode_after_transition
    transitioning = True
    transition_alpha = 0
    next_mode_after_transition = next_mode_val

def update_transition():
    global transitioning, transition_alpha, current_mode

    if transitioning:
        # Phase 1: Fade out current mode to black
        if transition_alpha < 255:
            transition_alpha += transition_speed * (255 / FPS) * 2 # Speed up fade to black
            if transition_alpha >= 255:
                transition_alpha = 255
                # Once fully black, switch mode and initialize
                current_mode = next_mode_after_transition
                if current_mode == MODE_STARS:
                    init_stars_mode()
                elif current_mode == MODE_PIPES:
                    init_pipes_mode()
                elif current_mode == MODE_BINARY:
                    init_binary_mode()
        # Phase 2: Fade in new mode from black
        else: # transition_alpha is 255 (fully black)
            transition_alpha -= transition_speed * (255 / FPS) * 2 # Speed up fade from black
            if transition_alpha <= 0:
                transition_alpha = 0
                transitioning = False

def draw_transition(screen):
    if transitioning:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        # Use current transition_alpha to determine transparency of the black overlay
        overlay.fill((0, 0, 0, int(min(255, transition_alpha))))
        screen.blit(overlay, (0, 0))

# --- Main Game Loop ---
running = True
clock = pygame.time.Clock()

# Initialize the first mode
init_stars_mode() # Start with stars

# Initialize binary columns data initially (even if not in binary mode yet)
# to avoid errors if font is used later or column data is accessed
init_binary_columns_data()

while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                global_speed_multiplier = min(global_speed_multiplier + 0.1, 3.0)
            elif event.key == pygame.K_DOWN:
                global_speed_multiplier = max(global_speed_multiplier - 0.1, 0.1)
            elif event.key == pygame.K_1: # Switch to Stars Mode
                if current_mode != MODE_STARS and not transitioning:
                    start_transition(MODE_STARS)
            elif event.key == pygame.K_2: # Switch to Pipes Mode
                if current_mode != MODE_PIPES and not transitioning:
                    start_transition(MODE_PIPES)
            elif event.key == pygame.K_3: # Switch to Binary Mode
                if current_mode != MODE_BINARY and not transitioning:
                    start_transition(MODE_BINARY)
            elif event.key == pygame.K_LEFT: # Star Density control (only in star mode)
                if current_mode == MODE_STARS:
                    STAR_DENSITY = max(0.1, STAR_DENSITY - 0.1)
                    # Re-populate stars based on new density
                    # This is a simple way; for very precise control, you might need to
                    # remove a percentage or add stars to reach the target density
                    STARS_LIST = [star for star in STARS_LIST if random.random() < STAR_DENSITY]
                    while len(STARS_LIST) < NUM_STARS * STAR_DENSITY:
                        star = create_star_data()
                        if star:
                            STARS_LIST.append(star)

            elif event.key == pygame.K_RIGHT: # Star Density control (only in star mode)
                if current_mode == MODE_STARS:
                    STAR_DENSITY = min(1.0, STAR_DENSITY + 0.1)
                    # Add new stars to reach new density
                    while len(STARS_LIST) < NUM_STARS * STAR_DENSITY:
                        star = create_star_data()
                        if star:
                            STARS_LIST.append(star)

            elif event.key == pygame.K_r: # Randomize Nebula Palette (only in star mode)
                if current_mode == MODE_STARS:
                    current_nebula_palette = random.choice(NEBULA_PALETTES)
                    NEBULA_ELEMENTS = []
                    for _ in range(NUM_NEBULAE):
                        nebula_color = random.choice(current_nebula_palette)
                        nebula_radius = random.randint(150, 400)
                        nebula_x = random.randint(0, SCREEN_WIDTH)
                        nebula_y = random.randint(0, SCREEN_HEIGHT)
                        NEBULA_ELEMENTS.append({'pos': (nebula_x, nebula_y), 'radius': nebula_radius, 'color': nebula_color})
            elif event.key == pygame.K_ESCAPE:
                running = False


    # --- Update Logic ---
    if not transitioning:
        if current_mode == MODE_STARS:
            update_stars_mode()
        elif current_mode == MODE_PIPES:
            update_pipes_mode()
        elif current_mode == MODE_BINARY:
            update_binary_mode()
    else:
        update_transition()

    # --- Drawing ---
    # Fill the screen with black if not in binary mode, as binary mode handles its own background for trailing effect
    if current_mode != MODE_BINARY:
        screen.fill(BLACK)

    if current_mode == MODE_STARS:
        draw_stars_mode(screen)
    elif current_mode == MODE_PIPES:
        draw_pipes_mode(screen)
    elif current_mode == MODE_BINARY:
        draw_binary_mode(screen) # Binary mode draws its own background for trail

    draw_transition(screen) # Draw transition overlay if active

    # --- Update Display ---
    pygame.display.flip()

    # --- Frame Rate Control ---
    clock.tick(FPS)

# --- Quit Pygame ---
pygame.quit()
sys.exit()