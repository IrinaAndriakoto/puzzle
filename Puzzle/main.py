import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk
import random

from pieces import Piece

def obtenir_dimensions_puzzle():
    # Fonction pour obtenir les dimensions du puzzle depuis l'utilisateur
    largeur = simpledialog.askinteger("Dimensions du Puzzle", "Entrez la largeur du puzzle:")
    hauteur = simpledialog.askinteger("Dimensions du Puzzle", "Entrez la hauteur du puzzle:")
    return largeur, hauteur

def creer_puzzle(largeur, hauteur):
    # Fonction pour créer le puzzle en fonction des dimensions choisies 
    image = Image.open('golf.jpg')
    largeur_fenetre = 200 * largeur
    hauteur_fenetre = 100 * hauteur
    image = image.resize((largeur_fenetre, hauteur_fenetre))

    largeur_piece = largeur_fenetre // largeur
    hauteur_piece = hauteur_fenetre // hauteur

    pieces = [[None for _ in range(largeur)] for _ in range(hauteur)]
    for i in range(largeur):
        for j in range(hauteur):
            piece_image = image.crop((i * largeur_piece, j * hauteur_piece, (i + 1) * largeur_piece, (j + 1) * hauteur_piece))
            piece = Piece(piece_image, i * hauteur + j)
            pieces[i][j] = piece

    return pieces, largeur_piece, hauteur_piece

# Obtenir les dimensions du puzzle depuis l'utilisateur
largeur_puzzle, hauteur_puzzle = obtenir_dimensions_puzzle()

# Créer le puzzle en fonction des dimensions choisies
pieces, largeur_piece, hauteur_piece = creer_puzzle(largeur_puzzle, hauteur_puzzle)

fenetre = tk.Tk()
canvas = tk.Canvas(fenetre, width=largeur_piece * largeur_puzzle, height=hauteur_piece * hauteur_puzzle)
canvas.pack()

images_tk = [[None for _ in range(largeur_puzzle)] for _ in range(hauteur_puzzle)]
piece_tks = []  # Liste pour stocker les instances ImageTk.PhotoImage

for i in range(largeur_puzzle):
    for j in range(hauteur_puzzle):
        piece = pieces[i][j]
        piece_tk = ImageTk.PhotoImage(piece.get_image())
        images_tk[i][j] = piece_tk  # Ajouter l'objet PhotoImage à la liste
        piece_tks.append(piece_tk)  # Ajouter l'instance à la liste
        canvas.create_image(i * largeur_piece, j * hauteur_piece, image=piece_tk, anchor='nw')

# Initialiser le compteur
compteur = 0

# Ajouter un label pour le compteur
label_compteur = tk.Label(fenetre, text=f"Compteur: {compteur}")
label_compteur.pack()

# Ajouter un bouton pour mélanger les pièces
def melanger():
    pieces_flat = [piece for sublist in pieces for piece in sublist]
    random.shuffle(pieces_flat)
    for i in range(largeur_puzzle):
        for j in range(hauteur_puzzle):
            pieces[i][j] = pieces_flat[i * largeur_puzzle + j]
            piece_tk = ImageTk.PhotoImage(pieces[i][j].get_image())
            images_tk[i][j] = piece_tk 
            canvas.create_image(i * largeur_piece, j * hauteur_piece, image=piece_tk, anchor='nw')
            
bouton_melanger = tk.Button(fenetre, text="Mélanger", command=melanger)
bouton_melanger.pack()

# Ajouter un bouton pour faire pivoter les pièces de 90 degrés
def pivoter_90():
    pieces_rotated = [list(reversed(col)) for col in zip(*pieces)]
    for i in range(largeur_puzzle):
        for j in range(hauteur_puzzle):
            pieces[j][largeur_puzzle - 1 - i] = pieces_rotated[i][j]
            piece_tk = ImageTk.PhotoImage(pieces[j][largeur_puzzle - 1 - i].get_image())
            images_tk[j][largeur_puzzle - 1 - i] = piece_tk 
            canvas.create_image(j * largeur_piece, (largeur_puzzle - 1 - i) * hauteur_piece, image=piece_tk, anchor='nw')

bouton_pivoter_90 = tk.Button(fenetre, text="Pivoter -90°", command=pivoter_90)
bouton_pivoter_90.pack()


def pivoter_moins_90():
    pieces_rotated = [list(col) for col in reversed(list(zip(*pieces)))]
    for i in range(largeur_puzzle):
        for j in range(hauteur_puzzle):
            pieces[hauteur_puzzle - 1 - j][i] = pieces_rotated[i][j]
            piece_tk = ImageTk.PhotoImage(pieces[hauteur_puzzle - 1 - j][i].get_image())
            images_tk[hauteur_puzzle - 1 - j][i] = piece_tk 
            canvas.create_image((hauteur_puzzle - 1 - j) * largeur_piece, i * hauteur_piece, image=piece_tk, anchor='nw')

bouton_pivoter_moins_90 = tk.Button(fenetre, text="Pivoter 90°", command=pivoter_moins_90)
bouton_pivoter_moins_90.pack()

premiere_piece = None

def echanger_pieces(event):
    global premiere_piece, compteur
    i = event.x // largeur_piece
    j = event.y // hauteur_piece

    # Check if indices are within valid range
    if i < 0 or i >= largeur_puzzle or j < 0 or j >= hauteur_puzzle:
        return

    if premiere_piece is None:
        premiere_piece = (i, j)
    else:

        i1, j1 = premiere_piece
        pieces[i][j], pieces[i1][j1] = pieces[i1][j1], pieces[i][j]
        premiere_piece = None  # Réinitialiser la première pièce

        # Incrémenter le compteur
        compteur += 1
        label_compteur['text'] = f"Compteur: {compteur}"

        # Vérifier si les images sont en ordre
        if est_en_ordre():
            messagebox.showinfo("Félicitations", f"Vous avez réussi en {compteur} mouvements!")
            compteur = 0  # Réinitialiser le compteur pour le prochain jeu
            label_compteur['text'] = f"Compteur: {compteur}"  # Mettre à jour le label du compteur

    for i in range(largeur_puzzle):  # and here
        for j in range(hauteur_puzzle):  # change here
                piece = pieces[i][j]
                piece_tk = ImageTk.PhotoImage(piece.get_image())
                images_tk[i][j] = piece_tk  # Mettre à jour l'objet PhotoImage dans la liste
                canvas.create_image(i * largeur_piece, j * hauteur_piece, image=piece_tk, anchor='nw')

canvas.bind("<Button-1>", echanger_pieces)

# Fonction pour vérifier si les images sont dans l'ordre
def est_en_ordre():
    flat = [piece.get_id() for sublist in pieces for piece in sublist]
    return flat == sorted(flat)

fenetre.mainloop()
