import Draw
import random

gridSize = 20
canvaSize= 500

NUM_COLS = canvaSize // gridSize
NUM_ROWS = canvaSize // gridSize

def drawBoard(snake, appleRow, appleCol, gridSize, score):
    #creating red apple
    Draw.clear()
    Draw.setColor(Draw.RED)
    Draw.filledOval(appleRow*gridSize, appleCol*gridSize, gridSize, gridSize) 
    
    #pixel coordinate get row num and col num multiply by gridsize 
    Draw.setColor(Draw.GREEN)
    
    #iterate over each segment in the snake
    for segment in snake:
        #x coordinate * size of grid cell, y coordinate * segment(gridsize)
        Draw.filledOval(segment[0]*gridSize , segment[1]*gridSize, gridSize, gridSize) 
        
    Draw.setColor(Draw.RED)
    Draw.setFontSize(18)
    #keeps track of the score
    Draw.string("Score: " + str(score), 420,480)
    
    Draw.show(200)
    
    
def moveSnake(snake, dx, dy):
    #head of the snake + change in coordinates
    newHeadRow = snake[0][0] + dy
    newHeadCol = snake[0][1] + dx
    
    #creating new list for new position of snakes head
    newPoint = [newHeadRow, newHeadCol]
    newSnake = [newPoint] + snake[:-1] #combines new position of the head with the rest of the body without the last segment 
    return newSnake

def snakeHitWall(snake):
    #get row num and col num of snakehead and saved into variable snake row and snake col
    #assigns x and y coordinate to 
    snakeHeadX = snake[0][0] 
    snakeHeadY = snake[0][1]
    
    #assign from the list
    if snakeHeadX < 0 or snakeHeadX > NUM_ROWS-1: #makes sure snake doesnt go out of the canvas
        return True 
    
    if snakeHeadY < 0 or snakeHeadY > NUM_COLS-1:
        return True
    
    return False


def snakeHitApple(snake, appleRow, appleCol):
    #get row num and col num of snakehead and save into variable snake row and snake col
    snakeHeadX = snake[0][0]
    snakeHeadY = snake[0][1]
    
    if snakeHeadX == appleRow and snakeHeadY == appleCol:
        return True
    
    return False


def snakeHitsSelf(snake):
    return (snake[0] in snake[1:]) #makes sure the snake head doesnt have same coordinates as the snakes body

       
def placeApple(prevSnake):
    appleCol = random.randint(0, NUM_COLS-1) 
    appleRow = random.randint(0, NUM_ROWS-1) 
    return [appleCol, appleRow]
    
        
def playGame(prevSnake, prevDirection, score):
    apple = placeApple(prevSnake) #apple new coordinate
    #if the coordinate of the apple exists in the snake, replace apple position 
    while apple in prevSnake:
        apple = placeApple(prevSnake)

    snake = prevSnake
    
    dx = 1
    dy = 0

    direction = prevDirection
    if direction == "Left":
        dx = -1
        dy = 0 
    if direction == "Right":
        dx = 1
        dy = 0 
    if direction == "Up":
        dx = 0
        dy = -1 
    if direction == "Down":
        dx = 0
        dy = 1 
    while True:
        #if a key was pressed, change based on the key 
        if Draw.hasNextKeyTyped():
          
            newKey = Draw.nextKeyTyped()
            
            #when key is pressed, track new direction and update dx and dy 
            if newKey == "Left":
                direction = "Left"
                dx = -1
                dy = 0 
                
            if newKey == "Right":
                direction = "Right"
                dx = 1
                dy = 0 
                
            if newKey == "Up":
                direction = "Up"
                dx = 0
                dy = -1
                
            if newKey == "Down":
                direction = "Down"
                dx = 0 
                dy = 1        
       
        snake = moveSnake(snake, dy, dx) 
        #drawing a new board everytime the snake moves
        drawBoard(snake, apple[0], apple[1], gridSize, score) 
        
        if snakeHitWall(snake): #game ends when hit the wall
            return False
        
        elif snakeHitsSelf(snake): #game ends when hit self
            return False  
        
        elif snakeHitApple(snake, apple[0], apple[1]):
            new_point = [snake[0][0] + dx, snake[0][1] + dy]
            biggerSnake = [new_point] + snake #adds new point to the head of the snake

            return {'snake': biggerSnake, 'direction': direction}
    

def main():
    Draw.setCanvasSize(500,500)
    Draw.setBackground(Draw.GRAY)
    
    #introducing the game
    Draw.picture("snakelogo.gif", -13, 40)
    Draw.show(700)
    
    #instantating values
    score = 0
    snake = [[0,2], [0, 1], [0, 0]] #3 segment snake 
    direction = "Right" 
    
    for size in range(2, 23):
        result = playGame(snake, direction, score)
        if result == False:
            Draw.clear()
            Draw.picture("gameover.gif", -415, -120)
            Draw.show(700)
            break
        else:
            score += 1
            snake = result['snake'] 
            direction = result['direction']
            if score == 20:
                Draw.clear()
                Draw.setColor(Draw.RED)
                Draw.picture("youwin.gif", 20, 90)
                
                Draw.show()
                break
    
main()