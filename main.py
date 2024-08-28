import pygame
import heapq
import sys
import random
import asyncio

pygame.init()

# 设置窗口大小
cell_size = 40
num_cells = 15

screen = pygame.display.set_mode((cell_size * num_cells, cell_size * num_cells))
pygame.display.set_caption("Pygame Bomberman Map")

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
SLATE_GRAY = (112, 128, 144)
BROWN = (139, 69, 19)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
SAPPHIRE = (15, 82, 186)

# 敌人类型的颜色
ENEMY_COLORS = [
    (255, 69, 0),     # 橙色
    (0, 191, 255),    # 深天蓝
    (144, 238, 144),  # 浅绿色
    (148, 0, 211)     # 深紫罗兰
]

# 游戏状态定义
STATE_INITIAL = "initial"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
game_state = STATE_INITIAL

# 地图配置
map_grids = {
    "first": [
        [0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0],
        [0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0],
        [0, 4, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 4, 0],
        [0, 4, 0, 3, 0, 0, 0, 0, 0, 0, 0, 3, 0, 4, 0],
        [0, 4, 0, 3, 0, 1, 1, 1, 1, 1, 0, 3, 0, 4, 0],
        [0, 4, 0, 3, 0, 1, 0, 0, 0, 1, 0, 3, 0, 4, 0],
        [0, 4, 0, 3, 0, 1, 0, 0, 0, 1, 0, 3, 0, 4, 0],
        [0, 4, 0, 3, 0, 1, 0, 0, 0, 1, 0, 3, 0, 4, 0],
        [0, 4, 0, 3, 0, 1, 1, 1, 1, 1, 0, 3, 0, 4, 0],
        [0, 4, 0, 3, 0, 0, 0, 0, 0, 0, 0, 3, 0, 4, 0],
        [0, 4, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 4, 0],
        [0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0],
        [0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],
    "second": [
        [4, 3, 1, 2, 3, 1, 4, 0, 4, 1, 3, 2, 1, 3, 4],
        [3, 1, 0, 1, 3, 0, 1, 4, 1, 0, 3, 1, 0, 1, 3],
        [1, 0, 4, 0, 1, 4, 0, 3, 0, 4, 1, 0, 4, 0, 1],
        [2, 1, 0, 1, 3, 0, 1, 4, 1, 0, 3, 1, 0, 1, 2],
        [3, 3, 1, 0, 4, 0, 4, 0, 4, 0, 4, 0, 1, 3, 3],
        [1, 0, 4, 1, 0, 3, 0, 1, 0, 3, 0, 1, 4, 0, 1],
        [4, 1, 0, 4, 3, 0, 1, 4, 1, 0, 3, 4, 0, 1, 4],
        [0, 4, 3, 1, 0, 4, 0, 0, 0, 4, 0, 1, 3, 4, 0],
        [4, 1, 0, 4, 3, 0, 1, 4, 1, 0, 3, 4, 0, 1, 4],
        [1, 0, 4, 1, 0, 3, 0, 1, 0, 3, 0, 1, 4, 0, 1],
        [3, 3, 1, 0, 4, 0, 4, 0, 4, 0, 4, 0, 1, 3, 3],
        [2, 1, 0, 1, 3, 0, 1, 4, 1, 5, 3, 1, 0, 1, 2],
        [1, 0, 4, 0, 1, 4, 0, 3, 0, 4, 1, 0, 4, 0, 1],
        [3, 1, 0, 1, 3, 0, 1, 4, 1, 0, 3, 1, 0, 1, 3],
        [4, 3, 1, 2, 3, 1, 4, 0, 4, 1, 3, 2, 1, 3, 4]
    ],
    "final": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0],
        [0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0],
        [0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0],
        [0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0],
        [0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0],
        [0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0],
        [0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0],
        [0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0],
        [0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0],
        [0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0],
        [0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0],
        [0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0],
        [0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],
    "final2": [
        [0, 0, 2, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 0, 0],
        [2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 2, 2, 0, 2, 0, 2, 0, 2, 0, 2, 2, 2, 0],
        [0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0],
        [2, 2, 2, 0, 2, 2, 0, 2, 0, 2, 2, 0, 2, 2, 2],
        [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 2, 2, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 2, 0],
        [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
        [2, 2, 2, 0, 2, 2, 0, 2, 0, 2, 2, 0, 2, 2, 2],
        [0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0],
        [0, 2, 2, 2, 0, 2, 0, 2, 0, 2, 0, 2, 2, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2],
        [0, 0, 2, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 0, 0]
    ],
    "esther": [
        [3, 3, 3, 0, 1, 0, 3, 1, 1, 1, 1, 0, 0, 0, 0],
        [3, 0, 0, 0, 0, 0, 3, 0, 0, 3, 1, 1, 4, 2, 1],
        [3, 0, 2, 2, 0, 3, 3, 1, 1, 1, 0, 1, 4, 2, 1],
        [3, 0, 4, 1, 1, 1, 3, 1, 1, 1, 0, 1, 4, 3, 1],
        [4, 0, 4, 1, 0, 0, 4, 4, 4, 1, 0, 1, 0, 3, 0],
        [4, 2, 4, 1, 0, 1, 3, 3, 4, 4, 0, 0, 0, 3, 1],
        [4, 4, 4, 1, 0, 2, 0, 0, 3, 4, 4, 2, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 3, 0, 3, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 2, 4, 4, 3, 0, 0, 2, 0, 1, 4, 4, 4],
        [1, 3, 0, 0, 0, 4, 4, 3, 3, 1, 0, 1, 4, 2, 4],
        [0, 3, 0, 1, 0, 1, 4, 4, 4, 0, 0, 0, 1, 4, 0],
        [1, 3, 4, 1, 0, 1, 1, 1, 1, 3, 1, 1, 4, 0, 3],
        [1, 2, 4, 1, 0, 1, 1, 1, 3, 3, 0, 2, 2, 0, 3],
        [1, 2, 4, 1, 1, 3, 0, 0, 3, 0, 0, 0, 0, 0, 3],
        [5, 0, 0, 0, 1, 1, 1, 3, 0, 1, 0, 3, 3, 3, 3]
    ]
}

# 初始化游戏变量
player_pos = [5, 12]
player_lives = 9
current_level = 1
max_levels = 4
enemies_spawned_in_level_2 = 1
enemy_move_delay = 500
player_move_delay = 200
bomb_place_delay = 200
enemy_bomb_place_delay = 2000
level_3_start_time = 0
last_player_move_time = pygame.time.get_ticks()
last_bomb_place_time = pygame.time.get_ticks()
last_enemy_spawn_time = pygame.time.get_ticks()

# 创建敌人类型
def create_enemy(enemy_type, pos):
    return {
        'pos': list(pos),
        'lives': random.randint(1, 9) if enemy_type in [0, 2] else 10,
        'last_move_time': pygame.time.get_ticks(),
        'last_bomb_place_time': pygame.time.get_ticks() if enemy_type in [0, 1] else None,
        'can_place_bombs': enemy_type in [0, 1],
        'color': ENEMY_COLORS[enemy_type]
    }

# 显示初始界面
def show_initial_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    for i in range(1, 4):
        text = font.render(f"Press {i} for Level {i}", True, WHITE)
        screen.blit(text, (50, i * 50))
    pygame.display.flip()

# 处理初始界面事件
def handle_initial_screen_events():
    global game_state, current_level, enemies, map_grid
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                current_level = int(event.unicode)
                enemies, map_grid = setup_level(current_level)
                game_state = STATE_PLAYING

# 设置关卡
def setup_level(level_number):
    global level_3_start_time, player_pos
    enemies = []
    if level_number == 1:
        initial_positions = [(14, 0), (0, 14), (1, 1), (13, 13)]
        enemies = [create_enemy(2, pos) for pos in initial_positions]
        return enemies, map_grids["esther"]

    if level_number == 2:
        return [create_enemy(0, [0, 0])], map_grids["first"]

    if level_number == 3:
        corner_positions = [(0, 0), (0, num_cells - 1), (num_cells - 1, 0), (num_cells - 1, num_cells - 1)]
        enemies = [create_enemy(1, pos) for pos in corner_positions]
        level_3_start_time = pygame.time.get_ticks()
        player_pos = [num_cells // 2, num_cells // 2]
        return enemies, map_grids["final"]

    if level_number == 4:
        return [create_enemy(0, [0, 0])], map_grids["final2"]

# 下一关
def next_level():
    global current_level, enemies, map_grid, enemies_spawned_in_level_2, game_state
    if current_level < max_levels:
        current_level += 1
        enemies, map_grid = setup_level(current_level)
        if current_level in [2, 4]:
            enemies_spawned_in_level_2 = 1
    else:
        show_game_over("Victory! All levels completed!")
        game_state = STATE_GAME_OVER
        handle_game_over_screen_events()

# A* 算法
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(map_grid, start, goal):
    neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []
    heapq.heappush(oheap, (fscore[start], start))

    while oheap:
        current = heapq.heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data[::-1]

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            if 0 <= neighbor[0] < num_cells and 0 <= neighbor[1] < num_cells:
                if map_grid[neighbor[0]][neighbor[1]] != 0:
                    continue

                tentative_g_score = gscore[current] + 1
                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                    continue

                if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(oheap, (fscore[neighbor], neighbor))

    return False

# 炸弹列表和爆炸效果列表
bombs = []
explosions = []

# 处理瓦片破坏逻辑
def process_tile_destruction(nx, ny):
    if map_grid[nx][ny] == 4:  # 检查褐色砖块
        map_grid[nx][ny] = 3  # 降级为深灰色砖块
        return True
    elif map_grid[nx][ny] == 3:  # 检查深灰色砖块
        map_grid[nx][ny] = 1  # 降级为普通灰色砖块
        return True
    elif map_grid[nx][ny] == 1:  # 检查普通灰色砖块
        map_grid[nx][ny] = 0  # 被炸毁变为空地
        return True
    elif map_grid[nx][ny] == 2:  # 检查不可破坏的蓝色砖块
        return True  # 不降级，爆炸停止
    return False  # 空地或其他情况，允许爆炸继续传播

# 炸弹爆炸
def explode_bomb(bomb):
    global player_lives, enemies, enemies_spawned_in_level_2, game_state
    if bomb not in bombs:
        return

    x, y = bomb['pos']
    bomb_range = bomb['range']
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    affected_tiles = []
    immediate_explosions = []

    for dx, dy in directions:
        for step in range(1, bomb_range + 1):
            nx, ny = x + dx * step, y + dy * step
            if 0 <= nx < num_cells and 0 <= ny < num_cells:
                if process_tile_destruction(nx, ny):
                    break
                affected_tiles.append((nx, ny))

                for other_bomb in bombs:
                    if other_bomb['pos'] == [nx, ny] and other_bomb not in immediate_explosions:
                        immediate_explosions.append(other_bomb)
            else:
                break

    bombs.remove(bomb)
    explosions.append({'tiles': affected_tiles, 'end_time': pygame.time.get_ticks() + 500})

    if tuple(player_pos) in affected_tiles:
        if player_lives < 10:
            player_lives -= 1
            if player_lives <= 0:
                show_game_over("Game Over! Player died!")
                game_state = STATE_GAME_OVER
                handle_game_over_screen_events()

    for enemy in enemies[:]:
        if enemy['pos'] is not None and tuple(enemy['pos']) in affected_tiles:
            if enemy['lives'] is not None and enemy['lives'] < 10:
                enemy['lives'] -= 1
                if enemy['lives'] <= 0:
                    map_grid[enemy['pos'][0]][enemy['pos'][1]] = 0
                    enemies.remove(enemy)

                    if current_level in [2, 4] and enemies_spawned_in_level_2 < 5:
                        new_enemy = create_enemy(0, random_empty_position())
                        enemies.append(new_enemy)
                        enemies_spawned_in_level_2 += 1
                    elif len(enemies) == 0:
                        next_level()

    for bomb_to_explode in immediate_explosions:
        explode_bomb(bomb_to_explode)

# 绘制瓦片
def draw_tile(x, y, rect):
    color_map = {
        1: GREY,
        2: BLUE,
        3: SLATE_GRAY,
        4: BROWN,
        5: CYAN,
        6: SAPPHIRE,
    }
    pygame.draw.rect(screen, color_map.get(map_grid[x][y], WHITE), rect)
    pygame.draw.rect(screen, BLACK, rect, 1)

# 绘制网格
def draw_grid():
    for x in range(num_cells):
        for y in range(num_cells):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            draw_tile(x, y, rect)

    player_rect = pygame.Rect(player_pos[0] * cell_size, player_pos[1] * cell_size, cell_size, cell_size)
    pygame.draw.ellipse(screen, RED, player_rect)

    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy['pos'][0] * cell_size, enemy['pos'][1] * cell_size, cell_size, cell_size)
        pygame.draw.ellipse(screen, enemy['color'], enemy_rect)

    for bomb in bombs:
        if pygame.time.get_ticks() - bomb['time'] < 2000:
            bomb_rect = pygame.Rect(bomb['pos'][0] * cell_size, bomb['pos'][1] * cell_size, cell_size, cell_size)
            pygame.draw.ellipse(screen, YELLOW, bomb_rect)
        else:
            explode_bomb(bomb)

    current_time = pygame.time.get_ticks()
    for explosion in explosions[:]:
        if current_time < explosion['end_time']:
            for (ex, ey) in explosion['tiles']:
                rect = pygame.Rect(ex * cell_size, ey * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, GOLD, rect)
        else:
            explosions.remove(explosion)

    font = pygame.font.Font(None, 36)
    lives_text = font.render(f"Lives: {player_lives}", True, BLACK)
    screen.blit(lives_text, (10, 10))

    for i, enemy in enumerate(enemies):
        lives_text = font.render(
            f"Enemy {i + 1} Lives: {'Invincible' if enemy['lives'] == 10 else enemy['lives']}", True, BLACK)
        screen.blit(lives_text, (10, 50 + i * 40))

# 玩家移动
def move_player(dx, dy):
    global last_player_move_time, player_pos
    current_time = pygame.time.get_ticks()
    if current_time - last_player_move_time < player_move_delay:
        return

    new_x, new_y = player_pos[0] + dx, player_pos[1] + dy
    if 0 <= new_x < num_cells and 0 <= new_y < num_cells and map_grid[new_x][new_y] == 0:
        player_pos = [new_x, new_y]

    last_player_move_time = current_time

# 放置炸弹
def place_bomb():
    global last_bomb_place_time
    current_time = pygame.time.get_ticks()
    if current_time - last_bomb_place_time < bomb_place_delay:
        return

    bomb_range = 1 if current_level == 3 else 3
    if not any(bomb['pos'] == player_pos for bomb in bombs):
        bombs.append({'pos': player_pos.copy(), 'time': pygame.time.get_ticks(), 'range': bomb_range})
        last_bomb_place_time = current_time

# 敌人放置炸弹
def enemy_place_bomb(enemy):
    current_time = pygame.time.get_ticks()

    # 根据关卡不同调整敌人的炸弹范围
    bomb_range = 1 if current_level == 3 else 3

    if current_time - enemy['last_bomb_place_time'] >= enemy_bomb_place_delay:
        bombs.append({'pos': enemy['pos'].copy(), 'time': pygame.time.get_ticks(), 'range': bomb_range})
        enemy['last_bomb_place_time'] = current_time

# 找到地图中的空位置
def random_empty_position():
    empty_positions = [(x, y) for x in range(num_cells) for y in range(num_cells) if map_grid[x][y] == 0]
    if empty_positions:
        return random.choice(empty_positions)
    return None

# 敌人移动
def move_enemy():
    current_time = pygame.time.get_ticks()

    for enemy in enemies:
        if current_time - enemy['last_move_time'] > enemy_move_delay:
            enemy_path = a_star_search(map_grid, tuple(enemy['pos']), tuple(player_pos))

            if enemy_path:
                next_pos = enemy_path.pop(0)
                enemy['pos'] = list(next_pos)
                enemy['last_move_time'] = current_time

                if enemy['pos'] == player_pos and player_lives < 10:
                    show_game_over("Game Over! Player died!")
                    game_state = STATE_GAME_OVER
                    handle_game_over_screen_events()

            else:
                random_move_enemy(enemy)

            if enemy['can_place_bombs'] and current_time - enemy['last_bomb_place_time'] >= enemy_bomb_place_delay:
                enemy_place_bomb(enemy)

# 敌人随机移动
def random_move_enemy(enemy):
    current_time = pygame.time.get_ticks()
    if current_time - enemy['last_move_time'] < enemy_move_delay:
        return

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    random.shuffle(directions)

    for dx, dy in directions:
        new_x, new_y = enemy['pos'][0] + dx, enemy['pos'][1] + dy
        if 0 <= new_x < num_cells and 0 <= new_y < num_cells and map_grid[new_x][new_y] == 0:
            enemy['pos'] = [new_x, new_y]
            enemy['last_move_time'] = current_time
            break

# 找到地图中的空边缘位置
def random_edge_empty_position():
    edge_positions = []

    # 上边缘
    for y in range(num_cells):
        if map_grid[0][y] == 0:
            edge_positions.append((0, y))

    # 下边缘
    for y in range(num_cells):
        if map_grid[num_cells - 1][y] == 0:
            edge_positions.append((num_cells - 1, y))

    # 左边缘
    for x in range(num_cells):
        if map_grid[x][0] == 0:
            edge_positions.append((x, 0))

    # 右边缘
    for x in range(num_cells):
        if map_grid[x][num_cells - 1] == 0:
            edge_positions.append((x, num_cells - 1))

    if edge_positions:
        return random.choice(edge_positions)
    return None

# 更新游戏状态
def update_game_state():
    if current_level == 3 and pygame.time.get_ticks() - level_3_start_time >= 20000:
        next_level()

# 显示游戏结束
def show_game_over(message):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(cell_size * num_cells // 2, cell_size * num_cells // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)

# 处理游戏结束事件
def handle_game_over_screen_events():
    global game_state, enemies, player_pos, player_lives, current_level
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            current_level = 1
            player_pos = [5, 12]
            player_lives = 9
            enemies, map_grid = setup_level(current_level)
            game_state = STATE_INITIAL
            show_initial_screen()

async def main():
    global game_state, last_enemy_spawn_time

    clock = pygame.time.Clock()
    running = True
    while running:
        if game_state == STATE_INITIAL:
            show_initial_screen()
            handle_initial_screen_events()

        elif game_state == STATE_PLAYING:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    place_bomb()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]: move_player(-1, 0)
            elif keys[pygame.K_RIGHT]: move_player(1, 0)
            elif keys[pygame.K_UP]: move_player(0, -1)
            elif keys[pygame.K_DOWN]: move_player(0, 1)
            if keys[pygame.K_SPACE]: place_bomb()

            screen.fill(BLACK)
            move_enemy()
            draw_grid()
            pygame.display.flip()
            clock.tick(60)
            update_game_state()

            if current_level == 3 and pygame.time.get_ticks() - last_enemy_spawn_time >= 1000:
                new_enemy_pos = random_edge_empty_position()
                if new_enemy_pos:
                    enemies.append(create_enemy(1, new_enemy_pos))
                    last_enemy_spawn_time = pygame.time.get_ticks()

            await asyncio.sleep(0)

        elif game_state == STATE_GAME_OVER:
            show_game_over("Victory! Press any key to return to the main menu")
            handle_game_over_screen_events()

    pygame.quit()
    sys.exit()

# 运行异步主循环
asyncio.run(main())