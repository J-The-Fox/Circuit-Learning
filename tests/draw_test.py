
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)

run = True
width = 3
points = []
while run:

    draw = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and draw:
            points.append(event.pos)
        # if event.type == pygame.MOUSEBUTTONUP:
        #     points.append(event.pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                points = []
            if event.key == pygame.K_BACKSPACE:
                points = points[:-1]
            if event.key == pygame.K_UP:
                width += 1
            if event.key == pygame.K_DOWN:
                width -= 1

    screen.fill(0)
    if len(points) > 1:
        pygame.draw.lines(screen, (255, 255, 255), False, points, width)
    if len(points):
        pygame.draw.line(screen, (255, 255, 255), points[-1], pygame.mouse.get_pos(), width)
    pygame.display.flip()