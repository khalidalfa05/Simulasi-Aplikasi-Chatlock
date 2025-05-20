import tkinter as tk
from tkinter import PhotoImage, Scrollbar
from playfair import encrypt, decrypt
import os
from datetime import datetime

class ChatWindow:
    def __init__(self, root):
        self.key = "SECURITY"
        self.root = root
        self.root.title("💬 ChatLock - Simulasi Chat")
        self.root.geometry("900x600")
        self.root.configure(bg="#ece5dd")
        self.root.resizable(False, False)

        # Tambahkan background (jika ada)
        bg_path = os.path.join("assets", "bg.png")
        if os.path.exists(bg_path):
            self.bg_image = PhotoImage(file=bg_path)
            bg_label = tk.Label(root, image=self.bg_image)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Header
        header = tk.Frame(root, bg="#075e54", height=60)
        header.pack(fill=tk.X)
        title = tk.Label(header, text="ChatLock", font=("Segoe UI", 20, "bold"),
                         bg="#075e54", fg="white", pady=10)
        title.pack(pady=5)

        # Frame utama untuk chat
        self.main_frame = tk.Frame(root, bg="#ece5dd")
        self.main_frame.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)

        # Area tampilan chat
        self.chat_display = tk.Text(self.main_frame, height=20, width=100, wrap='word',
                                    font=("Segoe UI", 12), bg="#dcf8c6", bd=0, padx=10, pady=10, state='disabled')
        self.chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = Scrollbar(self.main_frame, command=self.chat_display.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_display.config(yscrollcommand=scrollbar.set)

        # Frame input
        self.input_frame = tk.Frame(root, bg="#ece5dd")
        self.input_frame.pack(pady=10)

        # Entry & Button untuk User 1
        self.entry_user1 = tk.Entry(self.input_frame, width=40, font=("Segoe UI", 12))
        self.entry_user1.grid(row=0, column=0, padx=5, pady=5)
        self.send1_btn = tk.Button(self.input_frame, text="Kirim User 1", command=self.send_user1,
                                   bg="#25d366", fg="white", font=("Segoe UI", 12, "bold"), width=15)
        self.send1_btn.grid(row=0, column=1, padx=5)

        # Entry & Button untuk User 2
        self.entry_user2 = tk.Entry(self.input_frame, width=40, font=("Segoe UI", 12))
        self.entry_user2.grid(row=1, column=0, padx=5, pady=5)
        self.send2_btn = tk.Button(self.input_frame, text="Kirim User 2", command=self.send_user2,
                                   bg="#128c7e", fg="white", font=("Segoe UI", 12, "bold"), width=15)
        self.send2_btn.grid(row=1, column=1, padx=5)

    def display_message(self, sender, message, sender_color):
        time = datetime.now().strftime("%H:%M")
        bubble = f"{sender} ({time}):\n{message}\n\n"
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, bubble)
        self.chat_display.tag_add(sender, "end-3l", "end-1l")
        self.chat_display.tag_config(sender, background=sender_color, foreground="black", lmargin1=10, lmargin2=10)
        self.chat_display.see(tk.END)
        self.chat_display.config(state='disabled')

    def send_user1(self):
        text = self.entry_user1.get()
        if text.strip() == "":
            return
        encrypted = encrypt(text, self.key)
        decrypted = decrypt(encrypted, self.key)
        self.display_message("🟢 User 1 (Encrypted)", encrypted, "#cdeccd")
        self.display_message("🟢 User 1 (Decrypted)", decrypted, "#ffffff")
        self.log_message("User 1", text, encrypted)
        self.entry_user1.delete(0, tk.END)

    def send_user2(self):
        text = self.entry_user2.get()
        if text.strip() == "":
            return
        encrypted = encrypt(text, self.key)
        decrypted = decrypt(encrypted, self.key)
        self.display_message("🔵 User 2 (Encrypted)", encrypted, "#cbe9f7")
        self.display_message("🔵 User 2 (Decrypted)", decrypted, "#ffffff")
        self.log_message("User 2", text, encrypted)
        self.entry_user2.delete(0, tk.END)

    def log_message(self, user, original, encrypted):
        os.makedirs("data", exist_ok=True)
        with open("data/logs.txt", "a") as f:
            f.write(f"{user}: {original} -> {encrypted}\n")