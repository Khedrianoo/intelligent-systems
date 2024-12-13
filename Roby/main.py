import pygame
import sys
from collections import deque

pygame.init()

custom_font_path = r"PixelGame.otf"
font_size = 32
font = pygame.font.Font(custom_font_path, font_size)

WHITE = (253, 184, 39)
BLACK = (35, 18, 11)
GRAY = (35, 18, 11)
OBSTACLE_COLOR = (35, 18, 11)
BACKGROUND_COLOR = (241, 241, 241)
HIGHLIGHT_COLOR = (33, 32, 156)
PATH_COLOR = (33, 32, 156)

WINDOW_SIZE = 1000
BUTTON_COLUMN_WIDTH = 200
GRID_AREA_SIZE = WINDOW_SIZE - BUTTON_COLUMN_WIDTH
FPS = 60

# Load the logo image
logo = pygame.image.load("logo.png")

# Set the window icon
pygame.display.set_icon(logo)


roby_position = None
goal_position = None
obstacles = []
history = []
clock = pygame.time.Clock()

start_image = pygame.image.load(r"start.png")
target_image = pygame.image.load(r"target.png")

bfs_path = []
astar_path = []
dfs_path = []
gbfs_path = []

def draw_grid(screen, grid_size, cell_size):
    for x in range(0, grid_size * cell_size, cell_size):
        pygame.draw.line(screen, BLACK, (x, 0), (x, grid_size * cell_size))
        pygame.draw.line(screen, BLACK, (0, x), (grid_size * cell_size, x))

def menu_screen():
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Enter Grid Size")

    input_text = ""
    active = True

    while True:
        screen.fill(BACKGROUND_COLOR)

        # Updated to use the custom font
        prompt = font.render("Enter Grid Size (e.g., 10 for 10x10):", True, WHITE)
        prompt_rect = prompt.get_rect(center=(300, 150))
        screen.blit(prompt, prompt_rect)

        input_box = pygame.Rect(200, 200, 200, 50)
        pygame.draw.rect(screen, WHITE, input_box, 2)

        # Updated to use the custom font
        input_surface = font.render(input_text, True, WHITE)
        input_rect = input_surface.get_rect(center=input_box.center)
        screen.blit(input_surface, input_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if input_text.isdigit():
                            return int(input_text)
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

        pygame.display.flip()
        clock.tick(FPS)

# B  F  S
def bfs(start, goal, grid_size):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    queue = deque([start])
    visited = set()
    parent = {}
    visited.add(start)

    while queue:
        current = queue.popleft()

        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = parent[current]
            path.reverse()
            if len(path) > 1:
                path.pop()
            return path

        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if (0 <= neighbor[0] < grid_size and 0 <= neighbor[1] < grid_size and
                    neighbor not in visited and neighbor not in obstacles):
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current

    return None  

# A *
def astar(start, goal, grid_size):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    open_set = set([start])
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = min(open_set, key=lambda x: f_score.get(x, float('inf')))

        # If we are at a cell adjacent to the goal, stop before the goal
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            if len(path) > 1:
                path.pop()
            return path
        
        open_set.remove(current)

        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])

            if (0 <= neighbor[0] < grid_size and 0 <= neighbor[1] < grid_size and
                    neighbor not in obstacles):
                tentative_g_score = g_score[current] + 1

                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)

                    if neighbor not in open_set:
                        open_set.add(neighbor)

    return None


# D  F  S
def dfs(start, goal, grid_size):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    stack = [start]
    visited = set()
    parent = {}

    while stack:
        current = stack.pop()

        if current in visited:
            continue

        visited.add(current)

        # If we are at a cell adjacent to the goal, stop before the goal
        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = parent[current]
            path.reverse()
            if len(path) > 1:
                path.pop()
            return path
        
        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if (0 <= neighbor[0] < grid_size and 0 <= neighbor[1] < grid_size and
                    neighbor not in visited and neighbor not in obstacles):
                stack.append(neighbor)
                parent[neighbor] = current

    return None


# G  B  F  S
def gbfs(start, goal, grid_size):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    open_set = [start]
    visited = set()
    parent = {}

    while open_set:
        open_set.sort(key=lambda x: heuristic(x, goal))
        current = open_set.pop(0)

        if current in visited:
            continue

        visited.add(current)

        # If we are at a cell adjacent to the goal, stop before the goal
        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = parent[current]
            path.reverse()
            if len(path) > 1:
                path.pop()
            return path
        
        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if (0 <= neighbor[0] < grid_size and 0 <= neighbor[1] < grid_size and
                    neighbor not in visited and neighbor not in obstacles):
                open_set.append(neighbor)
                parent[neighbor] = current

    return None


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def main():
    global roby_position, goal_position, obstacles, history, bfs_path, astar_path, dfs_path, gbfs_path
    
    # Load the logo and set it as the window icon
    logo = pygame.image.load("logo.png")
    pygame.display.set_icon(logo)
    
    grid_size = menu_screen()

    cell_size = GRID_AREA_SIZE // grid_size

    resized_start_image = pygame.transform.scale(start_image, (cell_size, cell_size))
    resized_target_image = pygame.transform.scale(target_image, (cell_size, cell_size))

    screen = pygame.display.set_mode((WINDOW_SIZE, GRID_AREA_SIZE))
    pygame.display.set_caption("Roby Game")

    buttons = [
        {"label": "Set Start", "y": 20, "action": "set_start", "is_selected": False},
        {"label": "Set Goal", "y": 90, "action": "set_goal", "is_selected": False},
        {"label": "Add Obstacles", "y": 160, "action": "add_obstacle", "is_selected": False},
        {"label": "Clear Grid", "y": 230, "action": "clear_grid", "is_selected": False},
        {"label": "Undo", "y": 300, "action": "undo", "is_selected": False},
        {"label": "Delete", "y": 370, "action": "delete", "is_selected": False},
        {"label": "Start BFS", "y": 440, "action": "start_bfs", "is_selected": False},
        {"label": "Start A*", "y": 510, "action": "astar", "is_selected": False},
        {"label": "Start DFS", "y": 580, "action": "start_dfs", "is_selected": False},
        {"label": "Start GBFS", "y": 650, "action": "start_gbfs", "is_selected": False},
    ]

    def draw_buttons():
        button_area_height = GRID_AREA_SIZE
        button_height = button_area_height // len(buttons)
        button_y = 0

        for button in buttons:
            button_rect = pygame.Rect(
                GRID_AREA_SIZE + 5,
                button_y,
                BUTTON_COLUMN_WIDTH - 5,
                button_height
            )

            button_color = HIGHLIGHT_COLOR if button["is_selected"] else WHITE
            pygame.draw.rect(screen, button_color, button_rect)
            pygame.draw.rect(screen, GRAY, button_rect, 2)

            text = font.render(button["label"], True, BLACK)
            text_rect = text.get_rect(center=button_rect.center)
            screen.blit(text, text_rect)

            button["rect"] = button_rect
            button_y += button_height

    def handle_button_click(mouse_pos):
        x, y = mouse_pos
        if x > GRID_AREA_SIZE:
            for button in buttons:
                if button["rect"].collidepoint(mouse_pos):
                    for btn in buttons:
                        btn["is_selected"] = False
                    button["is_selected"] = True
                    return button["action"]
        return None

    def get_grid_position(mouse_pos):
        x, y = mouse_pos
        if x < GRID_AREA_SIZE and y < GRID_AREA_SIZE:
            return y // cell_size, x // cell_size
        return None

    def save_state():
        history.append({
            "roby_position": roby_position,
            "goal_position": goal_position,
            "obstacles": obstacles[:],
            "bfs_path": bfs_path[:],
            "astar_path": astar_path[:],
            "dfs_path": dfs_path[:],
            "gbfs_path": gbfs_path[:]

        })

    selected_action = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                action = handle_button_click(mouse_pos)

                if action:
                    selected_action = action
                else:
                    grid_pos = get_grid_position(mouse_pos)
                    if grid_pos:
                        if selected_action == "set_start":
                            if goal_position != grid_pos and grid_pos not in obstacles:
                                save_state()
                                roby_position = grid_pos

                        elif selected_action == "set_goal":
                            if roby_position != grid_pos and grid_pos not in obstacles:
                                save_state()
                                goal_position = grid_pos

                        elif selected_action == "add_obstacle" and grid_pos not in obstacles:
                            save_state()
                            obstacles.append(grid_pos)

                        elif selected_action == "delete":
                            save_state()
                            if grid_pos in obstacles:
                                obstacles.remove(grid_pos)
                            if grid_pos == roby_position:
                                roby_position = None
                            if grid_pos == goal_position:
                                goal_position = None

                if selected_action == "clear_grid":
                    save_state()
                    roby_position, goal_position, obstacles, bfs_path = None, None, [], []

                if selected_action == "start_bfs" and roby_position and goal_position:
                    bfs_path = bfs(roby_position, goal_position, grid_size)

                if selected_action == "astar" and roby_position and goal_position:
                    bfs_path = astar(roby_position, goal_position, grid_size)

                if selected_action == "start_dfs" and roby_position and goal_position:
                    bfs_path = dfs(roby_position, goal_position, grid_size)

                if selected_action == "start_gbfs" and roby_position and goal_position:
                    bfs_path = gbfs(roby_position, goal_position, grid_size)

                if selected_action == "undo" and history:
                    last_state = history.pop()
                    roby_position = last_state["roby_position"]
                    goal_position = last_state["goal_position"]
                    obstacles = last_state["obstacles"]
                    bfs_path = last_state["bfs_path"]
                    astar_path = last_state["astar_path"]
                    dfs_path = last_state["dfs_path"]
                    gbfs_path = last_state["gbfs_path"]


        screen.fill(BACKGROUND_COLOR)
        draw_grid(screen, grid_size, cell_size)
        draw_buttons()

        if roby_position:
            screen.blit(resized_start_image, (roby_position[1] * cell_size, roby_position[0] * cell_size))
        if goal_position:
            screen.blit(resized_target_image, (goal_position[1] * cell_size, goal_position[0] * cell_size))

        for obstacle in obstacles:
            pygame.draw.rect(
                screen, OBSTACLE_COLOR,
                (obstacle[1] * cell_size, obstacle[0] * cell_size, cell_size, cell_size)
            )
            pygame.draw.rect(
                screen, WHITE,
                (obstacle[1] * cell_size, obstacle[0] * cell_size, cell_size, cell_size), 3
            )

        if bfs_path:
            for pos in bfs_path:
                pygame.draw.rect(
                    screen, PATH_COLOR,
                    (pos[1] * cell_size, pos[0] * cell_size, cell_size, cell_size)
                )
                pygame.draw.rect(
                    screen, WHITE,
                    (pos[1] * cell_size, pos[0] * cell_size, cell_size, cell_size), 3
                )

        if astar_path:
            for pos in astar_path:
                pygame.draw.rect(
                    screen, PATH_COLOR,
                    (pos[1] * cell_size, pos[0] * cell_size, cell_size, cell_size)
                )
                pygame.draw.rect(
                    screen, WHITE,
                    (pos[1] * cell_size, pos[0] * cell_size, cell_size, cell_size), 3
                )

        if dfs_path:
            for pos in dfs_path:
                pygame.draw.rect(
                    screen, PATH_COLOR,
                    (pos[1] * cell_size, pos[0] * cell_size, cell_size, cell_size)
                )
                pygame.draw.rect(
                    screen, WHITE,
                    (pos[1] * cell_size, pos[0] * cell_size, cell_size, cell_size), 3
                )

        if gbfs_path:
            for pos in gbfs_path:
                pygame.draw.rect(
                    screen, PATH_COLOR,
                    (pos[1] * cell_size, pos[0] * cell_size, cell_size, cell_size)
                )
                pygame.draw.rect(
                    screen, WHITE,
                    (pos[1] * cell_size, pos[0] * cell_size, cell_size, cell_size), 3
                )                        

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
