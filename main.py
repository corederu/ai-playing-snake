import pygame
import sys
import random
import utils
from math import sqrt

def move(direction, body, foodX, foodY, score) : 

    # Haut
    if direction == 1 :
        if body[0][1] != 0 :
            # si pas le haut de la grille
            newCoord = [body[0][0], body[0][1]-1]
        else :
            # si le haut de la grille on va en bas ( y = 39 )
            newCoord = [body[0][0], 39] 
    
    # Droite
    if direction == 2 :
        if body[0][0] != 39 :
            # si pas la droite de la grille
            newCoord = [body[0][0]+1, body[0][1]]
        else :
            # si la droite de la grille on va à gauche ( x = 0 )
            newCoord = [0, body[0][1]]
    
    # Bas
    if direction == 3 :
        if body[0][1] != 39 :
            # si pas le bas de la grille
            newCoord = [body[0][0], body[0][1]+1]
        else :
            # si le bas de la grille on va en haut ( y = 0 )
            newCoord = [body[0][0], 0]
    
    # Gauche
    if direction == 4 :
        if body[0][0] != 0 :
            # si pas la gauche de la grille
            newCoord = [body[0][0]-1, body[0][1]]
        else :
            # si la gauche de la grille on va à droite ( x = 39 )
            newCoord = [39, body[0][1]]
    
    # Verifie si newCoord pas déjà dans la liste -> crash
    if newCoord in body :
        body = []

    # Verifie si food
    elif newCoord[0] == foodX and newCoord[1] == foodY :
        body.insert(0, newCoord)
        score = score + 1
        
        # Genere nouveau food
        foodX = random.randint(0, 39)
        foodY = random.randint(0, 39)
        while [foodX, foodY] in body :
            foodX = random.randint(0, 39)
            foodY = random.randint(0, 39)

    # Deplacement normal
    else :
        body.insert(0, newCoord)
        body.pop()
    
    return body, foodX, foodY, score


def show(window, body, foodX, foodY, walk) :

    # Walk 
    if True :
        for [x,y] in walk :
            # Dessine un carré 
            pygame.draw.rect(window, (0,255,0), (x*15+7.5, y*15+7.5, 2, 2))

    # Snake
    for [x,y] in body :
        # Dessine un carré 
        pygame.draw.rect(window, (255,255,255), (x*15, y*15, 15, 15))
    
    # Food
    pygame.draw.rect(window, (255,0,0), (foodX*15, foodY*15, 15, 15))


class Node:
    def __init__(self, x, y, foodX, foodY, body, direction, previous, cost):
        self.x = x
        self.y = y
        self.foodX = foodX
        self.foodY = foodY
        self.body = body
        self.direction = direction
        self.previous = previous
        self.cost = cost

    def isGoal(self):
        if self.x == self.foodX and self.y == self.foodY:
            return True
        return False

    def extend(self):
        newNodes = []

        # Haut
        if self.y != 0 and self.direction != 3 and [self.x, self.y - 1] not in self.body:
            newNode = Node(self.x, self.y - 1, self.foodX, self.foodY, self.body + [[self.x, self.y - 1]], 1, self, self.cost + 1)
            newNodes.append(newNode)
        if self.y == 0 and self.direction != 3 and [self.x, 39] not in self.body:
            newNode = Node(self.x, 39, self.foodX, self.foodY, self.body + [[self.x, 39]], 1, self, self.cost + 1)
            newNodes.append(newNode)

        # Bas
        if self.y != 39 and self.direction != 1 and [self.x, self.y + 1] not in self.body:
            newNode = Node(self.x, self.y + 1, self.foodX, self.foodY, self.body + [[self.x, self.y + 1]], 3, self, self.cost + 1)
            newNodes.append(newNode)
        if self.y == 39 and self.direction != 1 and [self.x, 0] not in self.body:
            newNode = Node(self.x, 0, self.foodX, self.foodY, self.body + [[self.x, 0]], 3, self, self.cost + 1)
            newNodes.append(newNode)

        # Gauche
        if self.x != 0 and self.direction != 2 and [self.x - 1, self.y] not in self.body:
            newNode = Node(self.x - 1, self.y, self.foodX, self.foodY, self.body + [[self.x - 1, self.y]], 4, self, self.cost + 1)
            newNodes.append(newNode)
        if self.x == 0 and self.direction != 2 and [39, self.y] not in self.body:
            newNode = Node(39, self.y, self.foodX, self.foodY, self.body + [[39, self.y]], 4, self, self.cost + 1)
            newNodes.append(newNode)

        # Droite
        if self.x != 39 and self.direction != 4 and [self.x + 1, self.y] not in self.body:
            newNode = Node(self.x + 1, self.y, self.foodX, self.foodY, self.body + [[self.x + 1, self.y]], 2, self, self.cost + 1)
            newNodes.append(newNode)
        if self.x == 39 and self.direction != 4 and [0, self.y] not in self.body:
            newNode = Node(0, self.y, self.foodX, self.foodY, self.body + [[0, self.y]], 2, self, self.cost + 1)
            newNodes.append(newNode)

        return newNodes

    def h(self):        
        h = self.cost

        # distance vers la droite avec passage bord possible 
        if abs(self.foodX - self.x) > 20 :
            # passage par un bord
            if self.foodX > self.x :
                h += 40 - self.foodX + self.x
            if self.foodX < self.x :
                h += 40 - self.x + self.foodX
        else :
            h += abs(self.foodX - self.x)
        
        # distance vers le haut avec passage bord possible 
        if abs(self.foodY - self.y) > 20 :
            # passage par un bord
            if self.foodY > self.y :
                h += 40 - self.foodY + self.y
            if self.foodY < self.y :
                h += 40 - self.y + self.foodY

        else :
            h += abs(self.foodY - self.y)
        
        return h

    
    def __lt__(self, other):
        # Comparaison basée sur la valeur de 'h' pour les nœuds
        return self.h() < other.h()

def ia(direction, body, foodX, foodY):
    headX = body[0][0]
    headY = body[0][1]

    # Recherche du chemin le plus court
    head = Node(headX, headY, foodX, foodY, body, direction, None, 0)
    queue = utils.PriorityQueue(order='min')

    finalNode = None
    walk = []
    expored = []
    expored.append([head.x, head.y])

    queue.append(head)
    while len(queue) != 0:
        currentNode = queue.pop()
        if currentNode.isGoal():
            finalNode = currentNode
            break
        newNodes = currentNode.extend()
        for node in newNodes:
            if [node.x, node.y] not in expored :
                queue.append(node)
                expored.append([node.x, node.y])
    
    if finalNode is None :
        # pas de chemin vers la cible -> fait un mouvement qui le tue pas
        if ([headX, headY-1] not in body and headY != 0) or ([headX, 39] not in body and headY == 0):
            return 1, []
        elif ([headX, headY+1] not in body and headY != 39) or ([headX, 0] not in body and headY == 39) :
            return 3, []
        elif ([headX-1, headY] not in body and headX != 0) or ([39, headY] not in body and headX == 0):
            return 4, []
        elif ([headX+1, headY] not in body and headX != 39) or ([0, headY] not in body and headX == 39):
            return 2, []
        else : 
            return 1, []

    while finalNode.previous is not None:
        walk.append([finalNode.x, finalNode.y])
        finalNode = finalNode.previous

    [nextposX, nextposY] = walk.pop()

    if (nextposX < headX and abs(nextposX-headX) == 1) or (nextposX > headX and abs(nextposX-headX) > 5):
        return 4, walk
    if (nextposX > headX and abs(nextposX-headX) == 1) or (nextposX < headX and abs(nextposX-headX) > 5):
        return 2, walk
    if (nextposY < headY and abs(nextposY-headY) == 1) or (nextposY > headY and abs(nextposY-headY) > 5):
        return 1, walk
    if (nextposY > headY and abs(nextposY-headY) == 1) or (nextposY < headY and abs(nextposY-headY) > 5) :
        return 3, walk


        




##############################

# Initialisation de Pygame
pygame.init()

# Création de la fenêtre
window = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Snake")

# Variables de jeu (40x40)
body = [[20,20]]    # liste des positions du corps
direction = 1   # 1 haut ; 2 droite ; 3 bas ; 4 gauche
foodX = random.randint(0, 39)
foodY = random.randint(0, 39)
score = 0
delay = 25

start = True
while start:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            start = False
        elif events.type == pygame.KEYDOWN:
            if events.key == pygame.K_z:
                delay = delay * 2
            if events.key == pygame.K_a:
                delay = int(delay / 2)

    # Ralentir
    pygame.time.delay(delay)
    
    # Efface la fenetre
    window.fill((0, 0, 0))

    # IA choisi la direction 
    direction, walk = ia(direction, body, foodX, foodY)

    # Bouge le corps et calcule les nouvelles positions du corps ;  return une liste vide si collision
    body, foodX, foodY, score = move(direction, body, foodX, foodY, score)
    

    # Affiche le snake
    show(window, body, foodX, foodY, walk)

    # Si crash
    if len(body) == 0 :
        print("SCORE : " + str(score))
        body = [[20,20]]
        foodX = random.randint(0, 39)
        foodY = random.randint(0, 39)
        score = 0

        # Affiche le snake
        show(window, body, foodX, foodY, walk)

    
    # Refresh
    pygame.display.flip()


# Quitter Pygame
pygame.quit()
sys.exit()
