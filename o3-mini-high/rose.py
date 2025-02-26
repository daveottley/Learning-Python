#!/usr/bin/env python3
import turtle
import math

def draw_red_rose(scale=100):
    # Set up turtle
    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
    t.color("red")
    turtle.bgcolor("white")

    # Begin filling the rose shape
    t.begin_fill()
    first_point = True

    # Draw rose curve: r = scale * sin(5 * theta)
    for deg in range(0, 361):
        theta = math.radians(deg)
        r = scale * math.sin(5 * theta)
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        if first_point:
            t.penup()
            t.goto(x, y)
            t.pendown()
            first_point = False
        else:
            t.goto(x, y)
    t.end_fill()

if __name__ == "__main__":
    draw_red_rose()
    turtle.done()
