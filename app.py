import tkinter as tk
from chat_window import ChatWindow

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatWindow(root)
    root.mainloop()