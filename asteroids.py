from tkinter import *
import math

#To do: add shooting that wraps around the screen along with the asteroids, learn more about how the game "asteroids" works

class window():
    def __init__(s):
        s.root = Tk()
        s.root.title("Asteroids!")
        s.root.grid()

        s.root.bind("<KeyPress>", lambda event="<KeyPress>": window.keypress(event, s))
        s.root.bind("<KeyRelease>", lambda event="<KeyRelease>": window.keyrelease(event, s))


        s.canvas = Canvas(height = 900, width = 900, bg = "Black")
        s.canvas.grid()

        s.vertices = [600, 850, 500, 800, 550, 750]
        s.triangle = s.canvas.create_polygon(s.vertices, fill = "Yellow")

        s.rotate = "False"
        s.move = "False"
        s.shoot = "False"
        s.completed = "True"
        s.bullet = list()
        s.bulletvelx = list()
        s.bulletvely = list()
        s.bulletdistance = list()
        s.vel = 0 #Velocity of player
        window.movement(s)
        
        s.root.mainloop()

    def keypress(event, s):
        key = event.keysym
        if key == "d" or key == "a":
            s.rotate = "True"
            if key == "a":
                s.direction = "Right"
            elif key == "d":
                s.direction = "Left"

        elif key == "w":
            s.move = "True"
            
        elif key == "space":
            if s.completed == "True":
                s.shoot = "True"
                s.completed = "False"

    def keyrelease(event, s):
        key = event.keysym
        if key == "a" or key == "d":
            s.rotate = "False"
        elif key == "w":
            s.move = "False"
        elif key == "space":
            s.completed = "True"
        
    def movement(s):
        s.centerx = round((s.vertices[0] + s.vertices[2] + s.vertices[4]) / 3)
        s.centery = round((s.vertices[1] + s.vertices[3] + s.vertices[5]) / 3)

        if s.rotate == "True":
            for i in range(0, int(len(s.vertices) / 2) + 2, 2):
                xvalue = s.vertices[i]
                yvalue = s.vertices[i + 1]

                changeinx = xvalue - s.centerx
                changeiny = yvalue - s.centery

                length = math.sqrt((changeinx * changeinx) + (changeiny * changeiny))

                angle = math.degrees(math.asin(changeinx / length))

                if changeiny < 0:
                    temp = 90 - angle
                    angle = 90 + temp

                if s.direction == "Right":
                    angle += 3
                elif s.direction == "Left":
                    angle -= 3
                    
                afterchangeinx = round(((math.sin(math.radians(angle)) * length) + 100000), 6)
                afterchangeiny = round(((math.cos(math.radians(angle)) * length) + 100000), 6)

                afterchangeinx -= 100000
                afterchangeiny -= 100000
                
            
                s.vertices[i] = afterchangeinx + s.centerx
                s.vertices[i + 1] = afterchangeiny + s.centery
                
            s.canvas.delete(s.triangle)
            s.triangle = s.canvas.create_polygon(s.vertices, fill = "Yellow")

            s.centerx = int((s.vertices[0] + s.vertices[2] + s.vertices[4]) / 3)
            s.centery = int((s.vertices[1] + s.vertices[3] + s.vertices[5]) / 3)

        if s.move == "True":
            if s.vel < 200:
                s.vel += 1
        else:
            if s.vel > 0:
                s.vel -= 1


        xvalue = s.vertices[0]
        yvalue = s.vertices[1]

        s.changeinx = xvalue - s.centerx
        s.changeiny = yvalue - s.centery
        
        if s.vel > 0:
            done = "N"
            changeinx = int(s.changeinx * (s.vel / 1000))
            changeiny = int(s.changeiny * (s.vel / 1000))
            #----------------------------THIS PART OF THE PROGRAM ACCOUNTS FOR THE SHIP'S SCREEN-WRAP-----------------------------
            for i in range(0, int(len(s.vertices) / 2) + 2, 2):
                s.vertices[i] += changeinx
                s.vertices[i + 1] += changeiny

                directx = 0
                directy = 0

                if done == "N":
                    loop = "N"
                    if s.vertices[i] >= 900:
                        directx = -780
                        loop = "Y"
                    elif s.vertices[i] <= 0:
                        directx = 780
                        loop = "Y"
                    if s.vertices[i + 1] >= 900:
                        directy = -780
                        loop = "Y"
                    elif s.vertices[i + 1] <= 0:
                        directy = 780
                        loop = "Y"

                    if loop == "Y":    
                        for x in range(0, int(len(s.vertices) / 2) + 2, 2):
                            s.vertices[x] += directx
                            s.vertices[x + 1] += directy
                        done = "Y"

            s.canvas.delete(s.triangle)
            s.triangle = s.canvas.create_polygon(s.vertices, fill = "Yellow")

        if s.shoot == "True":
            s.shoot = "False"
            
            s.bullet.append(s.canvas.create_line(xvalue, yvalue, xvalue + int(s.changeinx / 2), yvalue + int(s.changeiny / 2), fill = "Red", width = 10))
            s.bulletvelx.append(int(s.changeinx / 10))
            s.bulletvely.append(s.changeiny / 10)
            s.bulletdistance.append(0)


        i = 0
        while i < len(s.bullet):
            s.canvas.move(s.bullet[i], s.bulletvelx[i], s.bulletvely[i])
            s.bulletdistance[i] += 1
            if s.bulletdistance[i] > 50:
                s.canvas.delete(s.bullet[i])
                del s.bullet[i]
                del s.bulletvelx[i]
                del s.bulletvely[i]
                del s.bulletdistance[i]
            i += 1

            
                


        s.root.after(10, window.movement, s)

        

if __name__ == "__main__":
    shape = window()

