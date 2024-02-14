import pygame
import sys

# 初始化pygame
pygame.init()

# 设置屏幕尺寸
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("推箱子游戏")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 加载图像
PLAYER = pygame.image.load("1.jpg").convert_alpha()
WALL = pygame.image.load("2.jpg").convert()
BOX = pygame.image.load("3.jpg").convert_alpha()
TARGET = pygame.image.load("4.jpg").convert_alpha()

# 设置游戏地图
level = [
    "WWWWWWWWWWWWWWWWWWWW",
    "W             T    W",
    "W              T  W",
    "W     BBB        TW",
    "W     B B         W",
    "W     BBB         W",
    "W                  W",
    "W                  W",
    "W    PPPPP         W",
    "W                  W",
    "W                  W",
    "W                  W",
    "W                  W",
    "W                  W",
    "W                  W",
    "WWWWWWWWWWWWWWWWWWWW"
]

# 根据地图设置游戏物体
walls = []
boxes = []
targets = []
player_pos = None

for y, row in enumerate(level):
    for x, tile in enumerate(row):
        if tile == "W":
            walls.append(pygame.Rect(x * 50, y * 50, 50, 50))
        elif tile == "B":
            boxes.append(pygame.Rect(x * 50, y * 50, 50, 50))
        elif tile == "T":
            targets.append(pygame.Rect(x * 50, y * 50, 50, 50))
        elif tile == "P":
            player_pos = [x * 50, y * 50]

# 设置游戏变量
moving_box = None
running = True

# 主循环
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_pos[1] -= 50
            elif event.key == pygame.K_DOWN:
                player_pos[1] += 50
            elif event.key == pygame.K_LEFT:
                player_pos[0] -= 50
            elif event.key == pygame.K_RIGHT:
                player_pos[0] += 50

            # 碰撞检测
            player_rect = pygame.Rect(player_pos[0], player_pos[1], 50, 50)
            for wall in walls:
                if player_rect.colliderect(wall):
                    if event.key == pygame.K_UP:
                        player_pos[1] += 50
                    elif event.key == pygame.K_DOWN:
                        player_pos[1] -= 50
                    elif event.key == pygame.K_LEFT:
                        player_pos[0] += 50
                    elif event.key == pygame.K_RIGHT:
                        player_pos[0] -= 50
            for box in boxes:
                if player_rect.colliderect(box):
                    moving_box = box

    WIN.fill(WHITE)

    # 绘制地图
    for wall in walls:
        WIN.blit(WALL, wall)
    for target in targets:
        WIN.blit(TARGET, target)
    for box in boxes:
        WIN.blit(BOX, box)

    # 绘制玩家
    WIN.blit(PLAYER, player_pos)

    # 如果箱子移动了，更新箱子位置
    if moving_box:
        moving_box.center = player_rect.center

    # 碰撞检测
    for target in targets:
        for box in boxes:
            if target.colliderect(box):
                boxes.remove(box)

    pygame.display.flip()

# 退出游戏
pygame.quit()
sys.exit()
