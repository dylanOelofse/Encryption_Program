#All the imports needed for this program
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib
import random


class FileEncryptor:

    def __init__(self, master):
        #GUI of the program using tkinter import
        self.master = master
        master.title("File Encryption")
        master.configure(background='#F0F0F0')
        self.label = tk.Label(master, text="Choose a file to encrypt or decrypt:", font=('Helvetica', 14), background='#F0F0F0')
        self.label.pack(pady=(20,10))
        self.file_path = tk.StringVar()
        self.file_label = tk.Label(master, text="No file chosen", font=('Helvetica', 12), background='#F0F0F0')
        self.file_label.pack()
        self.choose_file_button = tk.Button(master, text="Choose File", font=('Helvetica', 12), background='#7FDBFF', command=self.choose_file)
        self.choose_file_button.pack(pady=(0,10))
        self.password_label = tk.Label(master, text="Enter a password for the file:", font=('Helvetica', 14), background='#F0F0F0')
        self.password_label.pack()
        self.password_entry = tk.Entry(master, show="*", font=('Helvetica', 12))
        self.password_entry.pack()
        self.encrypt_button = tk.Button(master, text="Encrypt File", font=('Helvetica', 12), background='#FF4136', foreground='#FFFFFF', command=self.encrypt_file)
        self.encrypt_button.pack(pady=(20,10))
        self.decrypt_button = tk.Button(master, text="Decrypt File", font=('Helvetica', 12), background='#2ECC40', foreground='#FFFFFF', command=self.decrypt_file)
        self.decrypt_button.pack()

    #Choose a file using the button
    def choose_file(self):
        self.file_path.set(filedialog.askopenfilename())
        self.file_label.configure(text=self.file_path.get())

    #Built in function to hash the password
    def sha256_hash(self, data):
        return hashlib.sha256(data).digest()

    #Encrypt function
    def O_encrypt(self, data, key, random_bytes):
        #Getting length of key
        key_length = len(key)
        #Turn the data into bytes
        encrypted = bytearray(data)
        #Cycle through all the bytes
        for i in range(len(data)):
            #Encrypt every byte using a XOR based algorithm with a random byte added
            encrypted[i] ^= key[i % key_length] ^ random_bytes[i % 16]
        return encrypted

    #Encrypt 
    def encrypt_file(self):
        #Getting the file
        filename = self.file_path.get()
        #Setting the password
        password = self.password_entry.get()
        global password_ENC 
        password_ENC = password
        #Makes sure a password is entered
        if len(password)== 0:
            messagebox.showerror("Error", "Please enter pasword.")
            return
        #Generating a key
        key = self.sha256_hash(bytes(password, "utf-8"))
        #Open file
        with open(filename, "rb") as file:
            file_data = file.read()
            random_bytes = os.urandom(16) # generate 16 random bytes
            encrypted_data = self.O_encrypt(file_data, key, random_bytes)
        encrypted_filename = filename.replace("&", "") + ".enc"
        with open(encrypted_filename, "wb") as file:
            file.write(random_bytes) # write the random bytes to the file
            file.write(encrypted_data)
        3#Delete old file
        os.remove(filename)
        self.password_entry.delete(0, tk.END)
        self.file_path.set("")
        messagebox.showinfo("File Encrypted", "The file has been encrypted and the original file has been deleted.") 

    #Decrypt function
    def decrypt_file(self):
        filename = self.file_path.get()
        password = self.password_entry.get()
        key = self.sha256_hash(bytes(password, "utf-8"))
        #Makes sure the correct password is entered
        if not password == password_ENC:
            messagebox.showerror("Error", "Please enter correct pasword.")
            return
        #Makes sure the file selected is encrypted denoted with .enc at the end
        if not filename.endswith('.enc'):
            messagebox.showerror("Error", "This is not an encrypted file.")
            return
        with open(filename, "rb") as file:
            file_data = file.read()
            random_bytes = file_data[:16] # extract the first 16 bytes for the random bytes
            decrypted_data = self.O_encrypt(file_data[16:], key, random_bytes) # Use O_encrypt with three arguments
        original_filename = os.path.splitext(filename)[0] # get the original filename
        with open(original_filename, "wb") as file:
            file.write(decrypted_data)
        os.remove(filename)
        self.password_entry.delete(0, tk.END)
        self.file_path.set("")
        messagebox.showinfo("File Decrypted", "The file has been decrypted and the encrypted file has been deleted.")


#Run the tkinter UI 
root = tk.Tk()
my_gui = FileEncryptor(root)
root.mainloop()