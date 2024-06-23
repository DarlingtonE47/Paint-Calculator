import tkinter as tk
import sounddevice as sd
from scipy.io.wavfile import read
from tkinter import messagebox
import webbrowser
import shutil
import time
import sqlite3
import json
import os


#username = os.getlogin()
#conn = sqlite3.connect(f'/home/{username}/Documents/PAINT.db')
filepath = "./configs/main_config.json"

def request():
	global config_data
	with open(filepath, 'r') as jsonfile:
		config_data = json.load(jsonfile)

def commit():
	global config_data
	with open(filepath, 'w') as jsonfile:
	    json.dump(config_data, jsonfile, indent=4)
request()
db_main = config_data["main"]["db_info"]["main_db_path"]
db_back = config_data["main"]["db_info"]["backup_db_path"]
err1 = config_data["resource"]["buzz_err"]
err2 = config_data["resource"]["ring_err"]
info1 = config_data["resource"]["bing_info"]

conn = sqlite3.connect(db_main)
cursor = conn.cursor()
# Створення таблиці, якщо вона не існує

cursor.execute('''CREATE TABLE IF NOT EXISTS paints (
					id INTEGER PRIMARY KEY,
					Дата_приходу DATE,
					Дата_тестування DATE,
			   		Номер_протоколу TEXT,
					Виробник TEXT,
					Назва_фарби TEXT,
					Марка_фарби TEXT,
					Середній_залишок REAL,
					Ступінь_перетиру REAL
				)''')
conn.commit()


def open_webpage(url):
	print(f"Trying to open {url}")
	webbrowser.open(url)

def playaudio(filepath):
	sample_rate, waveform = read(filepath)

	sd.play(waveform, sample_rate, blocksize=2048)
	sd.wait()

def check_start_index():
	request()
	start_status = config_data["system"]["start_index"]
	if start_status == 0:
		show_error("Інформація", "Ця програма розповсюджується безкоштовно на даному етапі, \
тож прошу підтримати автора для подальшого швидкого розвитку проєкту", info1, "Підтримати", "Відмовити")
		config_data["system"]["start_index"] = 1
		commit()
	else:
		pass

def show_error(title, text, audio, button, buttoni):
	tittle1 = title
	text1 = text
	audio1 = audio
	button1 = button
	button2 = buttoni
	error_window = tk.Toplevel(root)
	error_window.attributes("-topmost", True)
	error_window.attributes('-fullscreen', False)
	
	#error_window.geometry("350x400")
	#error_window.resizable(False, False)
	playaudio(audio1)
	error_window.title(tittle1)
	# Додавання елементів до вікна помилки з використанням grid
	label = tk.Label(error_window, text=text1, justify='center', wraplength=350)
	label.grid(row=0, column=0, columnspan=2, pady=10, sticky='nsew')

	# Функція, яка буде викликана при натисканні на кнопку "OK"
	def close_error_window():
		error_window.destroy()
	def payment():
		open_webpage("https://donatello.to/DarlingtonE47")
		close_error_window()

	ok_button = tk.Button(error_window, text=button1, command=payment )
	ok_button.grid(row=1, column=0, columnspan=2, pady=10, sticky='w')
	ignore_button = tk.Button(error_window, text = button2, command=close_error_window)
	ignore_button.grid(row=1, column=1, columnspan=2, pady=10,sticky='e')
	

def calculatefirst():
	bank = str(entry_num.get())
	m01 = float(entry_m0.get())
	m11 = float(entry_m1.get())
	m21 = float(entry_m2.get())
	x1 = m21 - m01
	x2 = m11 - m01
	x3 = x1 / x2
	res = x3 * 100
	resout1 = float(f"{res:.4f}")
	total_label.config(text='')
	result_label.config(text = f"\n\nЧашка №{bank} має залишок: {res:.2f}")
	return resout1


def calculatesecond():
	bank = str(entry_num_right.get())
	m02 = float(entry_m0_right.get())
	m12 = float(entry_m1_right.get())
	m22 = float(entry_m2_right.get())
	x1 = m22 - m02
	x2 = m12 - m02
	x3 = x1 / x2
	res = x3 * 100
	resout2 = float(f"{res:.4f}")
	total_label.config(text='')
	result_label_right.config(text = f"\nЧашка №{bank} має залишок: {res:.2f}")
	return resout2

def calculate_average_and_total():
	if not entry_num.get() or not entry_m0.get() or not entry_m1.get() or not entry_m2.get() or not entry_num_right.get() or not entry_m0_right.get() or not entry_m1_right.get() or not entry_m2_right.get():
		# Вивести повідомлення про незаповнені поля або обробити іншим чином
		return
	
	resout1 = calculatefirst()
	resout2 = calculatesecond()
	finres = (resout1 + resout2) / 2
	out = float(f"{finres:.2f}")
	return out


def total(out):
	bank1 = str(entry_num.get())
	bank2 = str(entry_num_right.get())
	resout1 = calculatefirst()
	resout2 = calculatesecond()
	date = str(entry_date.get())
	test_date = str(entry_test_date.get())
	protocol = str(protocol_entry.get())
	creator = str(entry_creator.get())
	name = str(entry_paint.get())
	mark = str(entry_mark.get())
	friction = str(friction_entry.get())
	result_label.config(text='')
	result_label_right.config(text='')
	total_label.config(text=f"Дата приходу: {date}\nДата тестування: {test_date}\nНомер протоколу: {protocol}\nВиробник: {creator}\nНазва: {name}\nМарка фарби: {mark}\nЧашка №{bank1}: {resout1}\nЧашка №{bank2}: {resout2}\nСередній залишок: {out}\nСтупінь перетиру: {friction}\n\nДАНІ ВНЕСЕНО ДО БАЗИ")

def db_register(out):
	date = str(entry_date.get())
	test_date = str(entry_test_date.get())
	protocol = str(protocol_entry.get())
	creator = str(entry_creator.get())
	name = str(entry_paint.get())
	mark = str(entry_mark.get())
	friction = str(friction_entry.get())

	cursor.execute('''INSERT INTO paints (Дата_приходу, Дата_тестування, Номер_протоколу, Виробник, Назва_фарби, Марка_фарби, Середній_залишок, Ступінь_перетиру)
					VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (date, test_date, protocol, creator, name, mark, out, friction ))
	#cursor.execute('''INSERT INTO paints (Дата_приходу, Дата_тестування, Номер_протоколу, Виробник, Назва_фарби, Марка_фарби, Середній_залишок, Ступінь_перетиру)
	#				VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (date, test_date, protocol, creator, name, mark, out ,friction))
	conn.commit()
	

def both():
	db_register(calculate_average_and_total())
	total(calculate_average_and_total())

def clear():
	entry_m0.delete(0, 'end')
	entry_m1.delete(0, 'end')
	entry_m2.delete(0, 'end')
	entry_num.delete(0, 'end')
	entry_date.delete(0, 'end')
	entry_paint.delete(0, 'end')
	entry_creator.delete(0, 'end')
	entry_m0_right.delete(0, 'end')
	entry_m1_right.delete(0, 'end')
	entry_m2_right.delete(0, 'end')
	entry_num_right.delete(0, 'end')
	entry_mark.delete(0, 'end')
	entry_test_date.delete(0, 'end')
	friction_entry.delete(0, 'end')
	protocol_entry.delete(0, 'end')
	result_label_right.config(text='')
	result_label.config(text='')
	total_label.config(text='')


root = tk.Tk()
root.title("Сухий залишок")
#перша колонка
# Створення LabelFrame для першого блоку даних
check_start_index()
#Tech data frame:

tech_data_frame = tk.LabelFrame(root, text="Інформація про фарбу", labelanchor='n', labelwidget=None)
tech_data_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

paint_name = tk.Label(tech_data_frame, text="Назва фарби:")
paint_mark = tk.Label(tech_data_frame, text="Марка фарби:")
creator = tk.Label(tech_data_frame, text="Виробник:")
date = tk.Label(tech_data_frame, text="Дата приходу:")
test_date = tk.Label(tech_data_frame, text="Дата тестування:")
protocol_num = tk.Label(tech_data_frame, text="Номер протоколу:")

entry_test_date = tk.Entry(tech_data_frame)
entry_creator = tk.Entry(tech_data_frame)
entry_paint = tk.Entry(tech_data_frame)
entry_date = tk.Entry(tech_data_frame)
entry_mark = tk.Entry(tech_data_frame)
protocol_entry = tk.Entry(tech_data_frame)

date.grid(row=0, column=0, sticky='e')
entry_date.grid(row=0, column=1, sticky='w')
paint_name.grid(row=1, column=2, sticky='e')
entry_paint.grid(row=1, column=3, sticky='w')
creator.grid(row=0, column=2, sticky='e')
entry_creator.grid(row=0, column=3, sticky='w')
paint_mark.grid(row=2, column=2, sticky='e')
entry_mark.grid(row=2, column=3, sticky='w')
test_date.grid(row=1, column=0, sticky='e')
entry_test_date.grid(row=1,column=1,sticky='w')
protocol_num.grid(row=2, column=0, sticky='e')
protocol_entry.grid(row=2, column=1,sticky='w')


#Test block
test_block = tk.LabelFrame(root, text="Тестовий блок", labelanchor='n', labelwidget=None)
left_data_frame = tk.LabelFrame(test_block, text="Перша чашка")
num = tk.Label(left_data_frame, text="Номер чашки:")
friction_stage = tk.Label(test_block, text= "Ступінь перетиру:")
label_m0 = tk.Label(left_data_frame, text="M0:")
label_m1 = tk.Label(left_data_frame, text="M1:")
label_m2 = tk.Label(left_data_frame, text="M2:")

entry_num = tk.Entry(left_data_frame)
entry_m0 = tk.Entry(left_data_frame)
entry_m1 = tk.Entry(left_data_frame)
entry_m2 = tk.Entry(left_data_frame)
friction_entry = tk.Entry(test_block)
calculate_button1 = tk.Button(left_data_frame, text="Обчислити чашку", command=lambda: calculatefirst())


test_block.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
left_data_frame.grid(row=0, column=0, padx=10, pady=10)
num.grid(row=1, column=1)
entry_num.grid(row=1, column=2)
label_m0.grid(row=2, column=1, sticky = "e")
entry_m0.grid(row=2, column=2)
label_m1.grid(row=3, column=1, sticky = "e")
entry_m1.grid(row=3, column=2)
label_m2.grid(row=4, column=1, sticky = "e")
entry_m2.grid(row=4, column=2)
friction_stage.grid(row=1, column=0,sticky='e')
friction_entry.grid(row=1, column=1, pady=10, sticky='w')
calculate_button1.grid(row=5, column=2, sticky = "nsew")


# Створення LabelFrame для другого блоку даних
right_data_frame = tk.LabelFrame(test_block, text="Друга чашка")
num_right = tk.Label(right_data_frame, text="Номер чашки:")
label_m0_right = tk.Label(right_data_frame, text="M0:")
label_m1_right = tk.Label(right_data_frame, text="M1:")
label_m2_right = tk.Label(right_data_frame, text="M2:")
clear_button = tk.Button(root, text = "Очистити", command = lambda: clear())
calculate_button2 = tk.Button(right_data_frame, text="Обчислити чашку", command=lambda: calculatesecond())

entry_num_right = tk.Entry(right_data_frame)
entry_m0_right = tk.Entry(right_data_frame)
entry_m1_right = tk.Entry(right_data_frame)
entry_m2_right = tk.Entry(right_data_frame)

right_data_frame.grid(row=0, column=1, padx=10, pady=10)
clear_button.grid(row=6, column=1, padx=10, sticky="e")
num_right.grid(row=1, column=1)
entry_num_right.grid(row=1, column=2)
label_m0_right.grid(row=2, column=1, sticky = "e")
entry_m0_right.grid(row=2, column=2)
label_m1_right.grid(row=3, column=1, sticky = "e")
entry_m1_right.grid(row=3, column=2)
label_m2_right.grid(row=4, column=1, sticky = "e")
entry_m2_right.grid(row=4, column=2)
calculate_button2.grid(row=5, column=2, sticky = 'nsew')
# Створення кнопки для обчислення середнього залишку
calculate_average_button = tk.Button(root, text="Обчислити середній залишок", command=lambda: both())
calculate_average_button.grid(row=6, column=0, columnspan=2)


result_label = tk.Label(root,text="",justify="left")
result_label.grid(row=8, column=0, sticky='w')
result_label_right = tk.Label(root, text = "", justify='left')
result_label_right.grid(row=9, column=0,sticky='w')
total_label = tk.Label(root, text="", justify ='left')
total_label.grid(row=8, column=0, sticky='w')
copyright = tk.Label(root, text="(c) Malyi Bohdan(2024)")
copyright.grid(row=11, column=1, sticky='e')
version = tk.Label(root, text='v3.4.0b (2024 beta build for MONOPACK LLC)')
version.grid(row=11, column=0, sticky='w')

root.mainloop()
conn.close()
