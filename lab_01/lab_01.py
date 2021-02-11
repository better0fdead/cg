from tkinter import *
from tkinter import messagebox
from math import sqrt, acos, degrees
y_coordinates = []
x_coordinates = []
pi = 3.14

def del_list():
    select = list(listbox.curselection())
    select.reverse()
    for i in select:
        listbox.delete(i)

def create_circle(x, y, r, canvasName, colorname):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1, outline = colorname)

def paint_triangle(x1,y1,x2,y2,x3,y3,x_v, y_v, r_v, x_o, y_o, r_o):
	canva.create_line(x1,y1,x2,y2)
	canva.create_line(x2,y2,x3,y3)
	canva.create_line(x3,y3,x1,y1)
	print(x1,y1,x2,y2,x3,y3, x_v, y_v, x_o, y_o)
	create_circle(x_v, y_v, r_v, canva, "red")
	create_circle(x_o, y_o, r_o, canva, "green")

#очистка холста
def clear():
	canva.delete("all")
	x_coordinates.clear()
	y_coordinates.clear()
	#del_list()
	listbox.delete(0, 'end')
#Добавление точки рисунком
def paint(event):
	x, y = (event.x), (event.y)
	canva.create_oval(x, y, x, y, width = 0, fill = "red")
	x_coordinates.append(x)
	y_coordinates.append(y)
#Ручное добавление точки
def add_point():
	try:
		x = float(X.get())
		y = float(Y.get())
		if x > 660 or x < 0 or y > 300 or y < 0:
			messagebox.showerror('Ошибка', 'Некорректный ввод')
			return
		canva.create_oval(x, y, x, y, width = 0, fill = "red")
		x_coordinates.append(x)
		y_coordinates.append(y)
	except ValueError:
		messagebox.showerror('Ошибка', 'Некорректный ввод')
		return
	listbox.insert(0, "x = " + str(x) + " y = " + str(y))
#Поиск вершин треугольника
def find_triangle():
	n = len(x_coordinates)
	if n <= 2 or (n == 3 and (x_coordinates[0] == x_coordinates[1] == x_coordinates[2] or y_coordinates[0] == y_coordinates[1] == y_coordinates[2])):
		messagebox.showerror('Ошибка', 'Введено недостаточно точек или все точки лежат на одной прямой')
	else:
		canva.delete("all")
		min_raz = 100000
		r_vp = 0
		r_op = 0
		p = 0
		x1 = y1 = x2 = y2 = x3 = y3 = 0
		raz = 0
		for i in range(n - 2):
			for j in range(i + 1, n - 1):
				for k in range(j + 1, n):
					a = sqrt((x_coordinates[i] - x_coordinates[j]) ** 2 + (y_coordinates[i] - y_coordinates[j]) ** 2)
					b = sqrt((x_coordinates[j] - x_coordinates[k]) ** 2 + (y_coordinates[j] - y_coordinates[k]) ** 2)
					c = sqrt((x_coordinates[i] - x_coordinates[k]) ** 2 + (y_coordinates[i] - y_coordinates[k]) ** 2)
					p = (a + b + c) / 2
					#print(a)
					#print(b)
					#print(c)
					try:
						r_vp = sqrt(((p - a) * (p - b) * (p - c)) / p)
						r_op = (a * b * c) / (4 * sqrt(p * (p - a) * (p - b) * (p - c)))
					except ZeroDivisionError:
						messagebox.showerror('Ошибка', 'Одна из троек вершин лежит на одной прямой')
						continue
					raz = pi*(r_op**2) - pi*(r_vp**2)
					#print(r_vp)
					#print(r_op)
					#angle1 = degrees(acos((b * b + c * c - a * a) / (2 * b * c)))
					#angle2 = degrees(acos((a * a + c * c - b * b) / (2 * a * c)))
					#angle3 = 180.0 - angle1 - angle2
					#if (angle1 >= 175.0 or angle2 >= 175.0 or angle3 >= 175.0):
					#	continue
					print(r_op)
					if raz < min_raz:
						min_raz = raz
						x1 = x_coordinates[i]
						y1 = y_coordinates[i]
						x2 = x_coordinates[j]
						y2 = y_coordinates[j]
						x3 = x_coordinates[k]
						y3 = y_coordinates[k]
						x_v = (b * x1 + c * x2 + a * x3) / (a + b + c)
						y_v = (b * y1 + c * y2 + a * y3) / (a + b + c)
						r_v = r_vp
						r_o = r_op
						d = 2*(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
						y_o = ((x1**2 + y1**2) * (x3 - x2) + (x2**2 + y2**2) * (x1 - x3) + (x3**2 + y3**2) * (x2 - x1)) /d
						x_o = ((x1**2 + y1**2) * (y2 - y3) + (x2**2 + y2**2) * (y3 - y1) + (x3**2 + y3**2) * (y1 - y2))/d
		paint_triangle(x1,y1,x2,y2,x3,y3, x_v, y_v, r_v, x_o, y_o, r_o)
	
root = Tk()
listbox = Listbox(width = 20, height = 20)
listbox.place(x = 210, y = 80)
root.title("Задача с треугольником")
root.geometry('810x800')
text_1 = Label(text = "Поиск треугольника, разность площадей описанной и вписанной окружностей минимальна.")
text_1.pack(side = TOP)
X = Entry()
X.place(x = 100, y = 100, width = 100, height = 30)
Y = Entry()
Y.place(x=100, y=150, width=100, height = 30)
text_x = Label(text = "x = ")
text_x.place(x = 60, y = 100)
text_y = Label(text = "y = ")
text_y.place(x = 60, y = 150)
point = Button(text = "Добавить точку", command = add_point)
point.place(x = 90, y = 210, width=100, height = 34)
triangle = Button(text = "Найти и построить треугольник", command = find_triangle)
triangle.place(x = 420, y = 210, width = 200, height = 50)
clear = Button(text = "Очистить", command = clear)
clear.place(x = 420, y = 120, width = 200, height = 50)
canva = Canvas(width = 660, height = 300, bg = "white")
canva.place(x = 20, y = 280)
canva.bind("<Button-1>", paint)
mainloop()