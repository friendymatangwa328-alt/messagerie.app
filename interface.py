from tkinter import *
from tkinter import messagebox
# ----- Base de données -----
fichier = "users.txt"
def lire_users():
    users = {}
    try:
        with open(fichier, "r") as f:
            for ligne in f:
                u, p = ligne.strip().split(";")
                users[u] = p
    except:
        pass
    return users
def ecrire_users(users):
    with open(fichier, "w") as f:
        for u, p in users.items():
            f.write(u + ";" + p + "\n")
def sauvegarder(user, pwd):
    with open(fichier, "a") as f:
        f.write(user + ";" + pwd + "\n")
# ----- CHAT -----
def ouvrir_chat(user1, user2):
    chat = Toplevel()
    chat.title(f"Chat : {user1} → {user2}")
    chat.geometry("400x500")
    chat.config(bg="#1e1e2f")
    Label(chat, text=f"Discussion avec {user2}",
          font=("Arial", 14, "bold"),
          bg="#1e1e2f", fg="white").pack(pady=10)
    zone = Text(chat, height=20, bg="#2c2c3e", fg="white")
    zone.pack(padx=10, pady=10)
    frame_msg = Frame(chat, bg="#1e1e2f")
    frame_msg.pack(pady=5)
    entree = Entry(frame_msg, width=25)
    entree.pack(side=LEFT, padx=5)
    def envoyer():
        msg = entree.get()
        if msg != "":
            zone.insert(END, f"{user1} → {user2} : {msg}\n")
            entree.delete(0, END)
    Button(frame_msg, text="Envoyer", bg="#4CAF50", fg="white",
           command=envoyer).pack(side=LEFT)
# ----- LISTE DES AMIS -----
def ouvrir_liste_amis(user):
    amis = Toplevel()
    amis.title("Liste des amis")
    amis.geometry("300x400")
    amis.config(bg="#1e1e2f")
    Label(amis, text="👥 Utilisateurs",
          font=("Arial", 14, "bold"),
          bg="#1e1e2f", fg="white").pack(pady=10)
    users = lire_users()
    for u in users:
        if u != user:
            Button(amis, text=u, bg="#2c2c3e", fg="white",
                   command=lambda u=u: ouvrir_chat(user, u)
                   ).pack(pady=5, fill="x", padx=10)
# ----- Fonctions -----
def inscription():
    user = entry_user.get()
    pwd = entry_pwd.get()
    if user == "" or pwd == "":
        messagebox.showerror("Erreur", "Remplis tous les champs")
        return
    users = lire_users()
    if user in users:
        messagebox.showerror("Erreur", "Utilisateur existe déjà")
    else:
        sauvegarder(user, pwd)
        messagebox.showinfo("Succès", "Inscription réussie")
def connexion():
    user = entry_user.get()
    pwd = entry_pwd.get()
    users = lire_users()
    if user in users and users[user] == pwd:
        messagebox.showinfo("Succès", "Connexion réussie")
        ouvrir_liste_amis(user)  # 👈 liste des amis
    else:
        messagebox.showerror("Erreur", "Identifiants incorrects")
def supprimer():
    user = entry_user.get()
    users = lire_users()
    if user in users:
        del users[user]
        ecrire_users(users)
        messagebox.showinfo("OK", "Compte supprimé")
    else:
        messagebox.showerror("Erreur", "Utilisateur introuvable")
def modifier():
    user = entry_user.get()
    new_pwd = entry_pwd.get()
    users = lire_users()
    if user in users:
        users[user] = new_pwd
        ecrire_users(users)
        messagebox.showinfo("OK", "Mot de passe modifié")
    else:
        messagebox.showerror("Erreur", "Utilisateur introuvable")
# ----- Interface principale -----
fenetre = Tk()
fenetre.title("Messagerie")
fenetre.geometry("400x350")
fenetre.config(bg="#1e1e2f")
Label(fenetre, text="🔐 Connexion", font=("Arial", 20, "bold"),
      bg="#1e1e2f", fg="white").pack(pady=10)
frame = Frame(fenetre, bg="#2c2c3e")
frame.pack(pady=20, padx=20, fill="both", expand=True)
Label(frame, text="Nom utilisateur", bg="#2c2c3e", fg="white").pack(pady=5)
entry_user = Entry(frame)
entry_user.pack(pady=5)
Label(frame, text="Mot de passe", bg="#2c2c3e", fg="white").pack(pady=5)
entry_pwd = Entry(frame, show="*")
entry_pwd.pack(pady=5)
Button(frame, text="Inscription", bg="#4CAF50", fg="white",
       command=inscription).pack(pady=5, fill="x")
Button(frame, text="Connexion", bg="#2196F3", fg="white",
       command=connexion).pack(pady=5, fill="x")
Button(frame, text="Modifier", bg="#FFC107", fg="black",
       command=modifier).pack(pady=5, fill="x")
Button(frame, text="Supprimer", bg="#F44336", fg="white",
       command=supprimer).pack(pady=5, fill="x")
fenetre.mainloop()