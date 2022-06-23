#!/usr/bin/env python

from tkinter import *
from tkinter import filedialog
from PIL import Image
import random
import sys
import os

window = Tk()


def open_win_diag():
    path = filedialog.askopenfilename()
    return path


def get_num_pixels(filepath):
    width, height = Image.open(filepath).size
    return width, height


def get_rgb_list(list, width, height):

    rgb_list = []

    for i in range(width):
        for j in range(height):
            pixel = list.getpixel((i, j))

            if len(pixel) > 3:
                last_element_index = len(pixel)-1
                pixel = pixel[:last_element_index]

            rgb_list += pixel

    return rgb_list


def rgb_to_binary(list):
    binary_list = []
    for i in range(len(list)):
        binary_list.append(format(list[i], '08b'))
    return binary_list


def get_xor(a, b):
    xored_list = []

    for i in range(len(a)):
        xor = ''
        l = [ord(a[i]) ^ ord(b[i]) for a[i], b[i] in zip(a[i], b[i])]
        for c in range(len(l)):
            xor += str(l[c])
        xored_list.append(xor)

    return xored_list


def binary_to_rgb(list):
    for i in range(len(list)):
        list[i] = int(list[i], 2)
    return list


def split_into_chunks(list):
    chunked_list = []
    chunk_size = 3

    for i in range(0, len(list), chunk_size):
        tl = tuple(list[i:i+chunk_size])
        chunked_list.append(tl)

    return chunked_list


def generate_rgb_list(length):
    generated_rgb_list = []
    for k in range(length):
        generated_rgb_list.append(random.randint(1, 255))
    return generated_rgb_list


def get_path(img_name):
    file_path = sys.argv[0]
    file_name = os.path.basename(file_path)
    file = os.path.splitext(file_name)
    size = len(file[0] + file[1])
    path = file_path[:-size] + 'images/' + img_name
    return path


def crypt():
    label = Label(
        window, text="Please, choose an image to crypt", font='Arial 10 bold')
    label.pack(pady=20)

    img_path = open_win_diag()
    img_to_crypt = Image.open(img_path)

    img_size = get_num_pixels(img_path)

    img_rgb_list = get_rgb_list(img_to_crypt, img_size[0], img_size[1])

    generated_rgb_list = generate_rgb_list(len(img_rgb_list))

    binary_list_img = rgb_to_binary(img_rgb_list)
    binary_list_generated = rgb_to_binary(generated_rgb_list)

    binary_xored_list = get_xor(binary_list_img, binary_list_generated)

    rgb_list = binary_to_rgb(binary_xored_list)
    rgb_list_chunked = split_into_chunks(rgb_list)
    generated_rgb_list_chunked = split_into_chunks(generated_rgb_list)

    crypted = Image.new(mode="RGB", size=(img_size[1], img_size[0]))
    crypted.putdata(rgb_list_chunked)
    crypted.save(get_path('crypted.png'))

    key = Image.new(mode="RGB", size=(img_size[1], img_size[0]))
    key.putdata(generated_rgb_list_chunked)
    key.save(get_path('key.png'))

    label.destroy()
    label = Label(window, text="Done. Your crypted image and key image have been saved at " +
                  get_path(''), font='Arial 10 bold')
    label.pack(pady=20)

    quit_btn = Button(window, text='Quit', bd='15', command=lambda: quit())
    quit_btn.place(x=490, y=250)


def uncrypt():
    label = Label(window, text="Please, choose an image to uncrypt",
                  font='Arial 10 bold')
    label.pack(pady=20)

    crypted_path = open_win_diag()
    crypted = Image.open(crypted_path)

    label.destroy()
    label = Label(
        window, text="Please, choose a key to uncrypt the image", font='Arial 10 bold')
    label.pack(pady=20)

    key_path = open_win_diag()
    key = Image.open(key_path)

    crypted_size = get_num_pixels(crypted_path)
    key_size = get_num_pixels(key_path)

    rgb_list_crypted = get_rgb_list(crypted, crypted_size[0], crypted_size[1])
    rgb_list_key = get_rgb_list(key, key_size[0], key_size[1])

    binary_list_crypted = rgb_to_binary(rgb_list_crypted)
    binary_list_key = rgb_to_binary(rgb_list_key)

    binary_unxored_list = get_xor(binary_list_crypted, binary_list_key)

    rgb_list = binary_to_rgb(binary_unxored_list)

    rgb_list_chunked = split_into_chunks(rgb_list)

    uncrypted = Image.new(mode="RGB", size=(crypted_size[1], crypted_size[0]))
    uncrypted.putdata(rgb_list_chunked)

    uncrypted.save(get_path('uncrypted.png'))
    uncrypted.show()

    label.destroy()
    label = Label(window, text="Done. Your uncrypted image has been saved at " +
                  get_path('uncrypted.png'), font='Arial 10 bold')
    label.pack(pady=20)

    quit_btn = Button(window, text='Quit', bd='15', command=lambda: quit())
    quit_btn.place(x=490, y=250)


def destroy_main_menu():
    options.destroy()
    crypt_btn.destroy()
    uncrypt_btn.destroy()


background = Canvas(window, width=1000, height=700, background='black')
background.place(x=0, y=0)

title = Label(window, text="Image Encryption Tool",
              bg="black", font=("Arial", 30), fg="white")
title.pack(pady=10)

options = Label(window, text="Options :", bg="black",
                font=("Arial", 15), fg="white")
options.pack(pady=100)

crypt_btn = Button(window, text='Crypt an image', bd='20',
                   command=lambda: [destroy_main_menu(), crypt()])
uncrypt_btn = Button(window, text='Uncrypt an image', bd='20',
                     command=lambda: [destroy_main_menu(), uncrypt()])

crypt_btn.place(x=345, y=250)
uncrypt_btn.place(x=510, y=250)

window.title('Image Encryption Tool')
window.geometry('1000x700')
window.mainloop()
