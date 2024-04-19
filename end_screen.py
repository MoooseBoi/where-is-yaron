from tkinter import *
from tkvideo import tkvideo


def main():
	root = Tk()
	root.geometry("1280x720")
	root.title("final screen")
	txt = Label(root, text="You lost, LOSER!", bg = "red", bd=100, fg="white", font=("Castellar", 30, 'bold'))
	txt.pack()
	my_label = Label(root)
	my_label.pack()
	player = tkvideo("assets/yaron-vid.mp4", my_label, loop = 1, size = (900, 720))
	player.play()
	root.configure(bg="red")
	root.mainloop()

if __name__ == "__main__":
    main()
