from menu import *

menu = Menu()
while (True):

    print("O que deseja procurar? ")
    print("Para sair do programa digite -1")
    tag = input()
    if (tag == '-1'):
        break
    menu.show_menu(tag)
