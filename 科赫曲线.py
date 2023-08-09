import turtle


def koch(size, n):
    if n == 0:
        turtle.fd(size)
    else:
        for angle in [0, 60, -120, 60]:
            turtle.left(angle)
            koch(size / 3, n - 1)


def main():
    turtle.setup(1920, 800)
    turtle.bgcolor("black")
    turtle.speed(0)  # 控制绘制速度
    turtle.hideturtle()  # 隐藏海龟，可显著加快绘制速度

    turtle.penup()
    turtle.goto(-900, 150)
    turtle.pencolor("orange")
    turtle.pendown()
    turtle.pensize(2)
    koch(500, 0)  # 阶数1

    turtle.penup()
    turtle.goto(-300, 150)
    turtle.pendown()
    turtle.pensize(2)
    koch(500, 1)  # 阶数2

    turtle.penup()
    turtle.goto(300, 150)
    turtle.pendown()
    turtle.pensize(2)
    koch(500, 2)  # 阶数3

    turtle.penup()
    turtle.goto(-900, -150)
    turtle.pencolor("orange")
    turtle.pendown()
    turtle.pensize(2)
    koch(500, 3)  # 阶数4

    turtle.penup()
    turtle.goto(-300, -150)
    turtle.pendown()
    turtle.pensize(2)
    koch(500, 4)  # 阶数5

    turtle.penup()
    turtle.goto(300, -150)
    turtle.pendown()
    turtle.pensize(2)
    koch(500, 5)  # 阶数6

    print('完成')
    turtle.done()


main()
