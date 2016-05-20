# !/usr/bin/env python
# coding: utf-8
'''Jeu de Fanorona (Ou Echecs Malgaches) développé sous python dans le cadre d'un projet pour la spécialité ISN en Terminale S'''

from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import os
import webbrowser

__authors__ = ["Bengoufa Ryan", "Galas Yoan", "Servière Mathieu"]
__license__ = "Open Source"
__version__ = "1.0"
__date__ = "17 Mai 2016"
    
class MyApp():
    '''Boucle principale du jeu'''
    #----------------------------------------------------------------------
    def __init__(self, parent):
        '''Constructor'''
        self.root = parent
        parent.title("Fanorona")
        
        btn = Button(parent, text="Jouer", command=self.openjouer , width=15, bd=0)
        btn.pack(pady=20)
    
        btn2 = Button(parent, text="Aide", command=self.aide, width= 15, bd=0)
        btn2.pack(pady=10)
        
        btn3 = Button(parent, text="A propos", command=self.openpropos, width= 15, bd=0)
        btn3.pack(pady=20)
        
        btn4 = Button(parent, text="Quitter", command=self.quitter, width= 15, bd=0)
        btn4.pack(pady=10)
        
    #----------------------------------------------------------------------
    def hide(self):
        '''Cache le menu'''
        self.root.withdraw()

    def show(self):
        '''Affiche le menu'''
        self.root.deiconify()

    def aide(self):
        '''Affiche la page web d'aide contenant les règles du jeu'''
        webbrowser.open('file://' + os.path.realpath('helppage/regles.html'))      

    def openpropos(self):
        '''Affiche la boite de dialogue contenant les informations relatives aux auteurs et à la license'''
        fenpropos = Toplevel()
        w=570
        h=150
        ws = fenpropos.winfo_screenwidth()
        hs = fenpropos.winfo_screenheight() 
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        fenpropos.geometry('%dx%d+%d+%d' % (w, h, x, y))
        fenpropos.title("Fanorona | A propos")
        fenpropos.resizable(0,0)
        
        icon = PhotoImage(file='media/logo.gif')
        fenpropos.tk.call('wm', 'iconphoto', fenpropos._w, icon)
        
        label = Label(fenpropos, text="Ce jeu de Fanorona a été créé dans le cadre d'un projet de spécialité ISN pour le Bac.\n\n Ryan Bengoufa : Création de l'interface graphique et codage du menu.\n Yoan Galas : Idée originale du projet.\n Mathieu Servière : Codage du jeu lui même.")
        label.pack(pady=10)
        
        handler = lambda: self.onClosefenpropos(fenpropos)
        btn = Button(fenpropos, text="Fermer", command=handler, width=15)
        btn.pack(pady=10)
    
    def onClosefenpropos(self, fenpropos):
        '''
        Ferme la fenêtre "A propos"
        Paramètre : fenpropos (Fenêtre Tkinter)
        '''
        fenpropos.destroy()
    
    def quitter(self):
        """Quitte le jeu"""
        self.root.destroy()
    #----------------------------------------------------------------------
    def openjouer(self):
        '''Démarre le jeu'''
        
        def askClosefenjeu():
            '''Demande à l'utilisateur si il est sur de vouloir quitter, si oui ferme le jeu'''
            if askyesno("Fanorona | Quitter","Êtes vous sur de vouloir quitter ? Toute progression non-sauvegardée sera perdue."): #Si la personne confirme
                onClosefenjeu()

        def askrestart():
            '''Demande à l'utilisateur si il est sur de vouloir recommencer, si oui redémarre le jeu'''
            if askyesno("Fanorona | Nouvelle partie","Êtes vous sur de vouloir recommencer? Toute progression non-sauvegardée sera perdue."): #Si la personne confirme
                restart()            

        def charger():
            '''
            Procédure de chargement d'une sauvegarde
            Variables : fichier (Lien vers fichier), joueur (Int), pions_j1 (List), pions_j2 (List), selected (Int), libre (List), banned_spots (List), pos(List), spots (List), game (Canvas Tkinter), couleur_banned (Str), couleur_select (Str)
            '''
            global joueur, pions_j1, pions_j2, selected, libre, banned_spots, pos, spots
            
            def unlist(entree):
                """Convertit une liste au format str en vraie liste"""
                temp = (entree[1:-1]).split(', ') #On retire les deux crochets (Début et fin) et on sépare les éléments
                sortie = []
                for i in range(len(temp)):
                    if temp[i]!='':
                        sortie.append(int(temp[i]))
                return(sortie)
            
            mask = \
            [("Sauvegardes","*.sav")]        
            fichier = askopenfile(filetypes=mask, mode='r')
            if fichier: #Si il y a chargement (Pas clic sur Cancel)
                document=fichier.readlines()
                liste=[]

                for rang in document:
                    ligne=rang.split('\n')
                    liste=liste+ligne

                joueur=int(liste[2])
                pions_j1=unlist(liste[6])
                pions_j2=unlist(liste[10])
                selected=int(liste[14])
                libre=unlist(liste[18])
                banned_spots=unlist(liste[22])
                pos=unlist(liste[26])
                spots=unlist(liste[30])

                game.delete(ALL)            
                grille()
                place_pions()
                
                if selected!=-1:
                    x_pion = (selected%9)*taille_case+marge_interne
                    y_pion = (selected//9)*taille_case+marge_interne
                    game.create_oval(x_pion-rayon, y_pion-rayon, x_pion+rayon, y_pion+rayon, fill=couleur_select)
                for i in range(len(banned_spots)):
                    x = (banned_spots[i]%9)*taille_case+marge_interne
                    y = (banned_spots[i]//9)*taille_case+marge_interne
                    game.create_rectangle(x-rayon, y-rayon, x+rayon, y+rayon, fill=couleur_banned)
                for i in range(len(spots)):
                    ColorCase(spots[i])

        def choix_approche():
            '''
            Referme la boite de dialogue demandant à l'utilisateur de choisir une prise et et lance la prise de pion par approche
            Variables : choix (Fenêtre Tkinter)
            '''
            choix.grab_release()
            choix.destroy()
            prise_pion_approche()
            fin_tour()

        def choix_eloignement():
            '''
            Referme la boite de dialogue demandant à l'utilisateur de choisir une prise et et lance la prise de pion par éloignement
            Variables : choix (Fenêtre Tkinter)
            '''
            choix.grab_release()
            choix.destroy()
            prise_pion_eloignement()
            fin_tour()

        def ColorCase(num):
            '''
            Met un point de couleur sur les emplacements où on peut se déplacer
            Paramètre : num (Int)
            Variables : x_pion (Int), y_pion (Int), game (Canvas Tkinter), rayon (Int), couleur_select (Str)
            '''
            x_pion = (num%9)*taille_case+marge_interne
            y_pion = (num//9)*taille_case+marge_interne
            game.create_oval(x_pion-(rayon/2), y_pion-(rayon/2), x_pion+(rayon/2), y_pion+(rayon/2), fill=couleur_select)

        def deplacement(dest):
            '''
            Déplace le pion sélectionné initialement vers l'emplacement sélectionné ensuite
            Paramètre : dest (Int)
            Variables : xs (Int), ys (Int), xd (Int), yd (Int), dx (Int), dy (Int), selected (Int), dest (Int), pions_j1 (List), pions_j2 (List), autorise (List)
            Retourne le type de déplacement effectué (Haut, Bas, Gauche, Droite, ...)
            '''
            if dest in libre:
                xs = (selected%9)
                ys = (selected//9)
                xd = (dest%9)
                yd = (dest//9)
                dx = xd-xs
                dy = yd-ys
                
                #Déplacement haut
                if dx==0 and dy<0 and (dest-selected)==(-9):
                    if joueur == 0:
                        pions_j1.remove(selected)
                        pions_j1.append(dest)
                    else:
                        pions_j2.remove(selected)
                        pions_j2.append(dest)
                    return "haut"

                #Déplacement bas
                elif dx==0 and dy>0 and (dest-selected)==9:
                    if joueur == 0:
                        pions_j1.remove(selected)
                        pions_j1.append(dest)
                    else:
                        pions_j2.remove(selected)
                        pions_j2.append(dest)                
                    return "bas"

                #Déplacement gauche
                elif dx<0 and dy==0 and (dest-selected)==(-1):
                    if joueur == 0:
                        pions_j1.remove(selected)
                        pions_j1.append(dest)
                    else:
                        pions_j2.remove(selected)
                        pions_j2.append(dest)
                    return "gauche"
    
                #Déplacement droite
                elif dx>0 and dy==0 and (dest-selected)==1:
                    if joueur == 0:
                        pions_j1.remove(selected)
                        pions_j1.append(dest)
                    else:
                        pions_j2.remove(selected)
                        pions_j2.append(dest)
                    return "droite"

                #Déplacement haut-gauche
                elif dx==dy and dx<0 and (dest-selected)==(-10):
                    autorise = [10, 12, 14, 16, 20, 22, 24, 26, 28, 30, 32, 34, 38, 40, 42, 44]
                    if selected in autorise:
                        if joueur == 0:
                            pions_j1.remove(selected)
                            pions_j1.append(dest)
                        else:
                            pions_j2.remove(selected)
                            pions_j2.append(dest)
                        return "haut-gauche"
                        
                #Déplacement haut-droite
                elif dx==(-1)*dy and dx>0 and (dest-selected)==(-8):
                    autorise = [10, 12, 14, 16, 18, 20, 22, 24, 28, 30, 32, 34, 36, 38, 40, 42]
                    if selected in autorise:
                        if joueur == 0:
                            pions_j1.remove(selected)
                            pions_j1.append(dest)
                        else:
                            pions_j2.remove(selected)
                            pions_j2.append(dest)
                        return "haut-droite"

                #Déplacement bas-gauche
                elif dx==(-1)*dy and dx<0 and (dest-selected)==8:
                    autorise = [0, 2, 4, 6, 8, 10, 12, 14, 18, 20, 22, 24, 26, 28, 30, 32]
                    if selected in autorise:
                        if joueur == 0:
                            pions_j1.remove(selected)
                            pions_j1.append(dest)
                        else:
                            pions_j2.remove(selected)
                            pions_j2.append(dest)
                        return "bas-gauche"

                #Déplacement bas-droite
                elif dx==dy and dx>0 and (dest-selected)==10:
                    autorise = [0, 2, 4, 6, 10, 12, 14, 16, 18, 20, 22, 24, 28, 30, 32, 34]
                    if selected in autorise:
                        if joueur == 0:
                            pions_j1.remove(selected)
                            pions_j1.append(dest)
                        else:
                            pions_j2.remove(selected)
                            pions_j2.append(dest)
                        return "bas-droite"

        def evaluation_prise_pion():
            '''
            On évalue quel type de prise va être effectuée (Par approche ? Par éloignement ? Les deux ?)
            Variables : x_pion (Int), y_pion (Int), joueur (Int), liste (List), type_move (Str), selected (Int), dest (Int)
            Retourne le type de prise qui va se faire (Approche, Eloignement, Double)
            '''
            x_pion = (dest%9)
            y_pion = (dest//9)
            if joueur == 0:
                liste = pions_j2
            else:
                liste = pions_j1
            
            #Déplacement haut
            if type_move == "haut":
                if (dest-9) in liste and (selected+9) in liste:
                    return "Double"
                elif (dest-9) in liste:
                    return "Approche"

            #Déplacement bas
            elif type_move == "bas":
                if (dest+9) in liste and (selected-9) in liste:
                    return "Double"
                elif (dest+9) in liste:
                    return "Approche"

            #Déplacement gauche
            elif type_move == "gauche":
                if (dest-1) in liste and (selected+1) in liste:
                    return "Double"
                elif (dest-1) in liste:
                    return "Approche"

            #Déplacement droite
            elif type_move == "droite":
                if (dest+1) in liste and (selected-1) in liste:
                    return "Double"
                elif (dest+1) in liste:
                    return "Approche"
                        
            #Déplacement haut-gauche
            elif type_move == "haut-gauche":
                if (dest-10) in liste and (selected+10) in liste:
                    return "Double"
                elif (dest-10) in liste:
                    return "Approche"

            #Déplacement haut-droite
            elif type_move == "haut-droite":
                if (dest-8) in liste and (selected+8) in liste:
                    return "Double"
                elif (dest-8) in liste:
                    return "Approche"

            #Déplacement bas-gauche
            elif type_move == "bas-gauche":
                if (dest+8) in liste and (selected-8) in liste:
                    return "Double"
                elif (dest+8) in liste:
                    return "Approche"
                
            #Déplacement bas-droite
            elif type_move == "bas-droite":
                if (dest+10) in liste and (selected-10) in liste:
                    return "Double"
                elif (dest+10) in liste:
                    return "Approche"

        def fin_tour():
            '''
            Evalue si la main passe ou non
            Variables : game (Canvas Tkinter), selected (Int), dest (Int), banned_spots (List), result (Str), xd (Int), yd (Int), taille_case (Int), marge_interne (Int)
            '''
            global selected, dest, banned_spots
            result = possibilitees(dest)
            if result:
                xd = (dest%9)*taille_case+marge_interne
                yd = (dest//9)*taille_case+marge_interne
                selected=dest
                game.delete(ALL)
                grille()
                place_pions()
                game.create_oval(xd-rayon, yd-rayon, xd+rayon, yd+rayon, fill=couleur_select)
                for i in range(len(banned_spots)):
                    x = (banned_spots[i]%9)*taille_case+marge_interne
                    y = (banned_spots[i]//9)*taille_case+marge_interne
                    game.create_rectangle(x-rayon, y-rayon, x+rayon, y+rayon, fill=couleur_banned)
                for i in range(len(spots)):
                    ColorCase(spots[i])
            else:
                banned_spots = []
                joueur_suivant()
                selected = -1
                game.delete(ALL)
                grille()
                place_pions()

        def grille():
            '''
            Dessine la grille
            Variables : game (Canvas Tkinter), i (Int), marge_interne (Int), taille_case (Int)
            '''
                                   
            #Lignes horizontales
            for i in range(5):
                game.create_line(marge_interne, marge_interne+i*taille_case, wcan_jeu-marge_interne, marge_interne+i*taille_case)

            #Lignes verticales
            for i in range(9):
                game.create_line(marge_interne+i*taille_case, marge_interne, marge_interne+i*taille_case, hcan_jeu-marge_interne)
            
            #Lignes obliques montantes
            game.create_line(marge_interne, marge_interne+2*taille_case, marge_interne+2*taille_case, marge_interne)
            for i in range(3):
                game.create_line(marge_interne+2*i*taille_case, hcan_jeu-marge_interne, marge_interne+2*i*taille_case+4*taille_case, marge_interne)
            game.create_line(wcan_jeu-marge_interne-2*taille_case, hcan_jeu-marge_interne, wcan_jeu-marge_interne, hcan_jeu-marge_interne-2*taille_case)

            #Lignes obliques descendantes
            game.create_line(marge_interne, marge_interne+2*taille_case, marge_interne+2*taille_case, hcan_jeu-marge_interne)
            for i in range(3):
                game.create_line(marge_interne+2*i*taille_case, marge_interne, marge_interne+2*i*taille_case+4*taille_case, hcan_jeu-marge_interne)
            game.create_line(wcan_jeu-marge_interne-2*taille_case, marge_interne, wcan_jeu-marge_interne, marge_interne+2*taille_case)

        def interface():
            '''
            Dessine la GUI
            Variables : fenjeu (Fenêtre Tkinter), game (Canvas Tkinter), icon (Image), background_jeu (Image), background_label (Label Tkinter), wcan_jeu (Int), hcan_jeu (Int), couleur_jeu (Str), mainmenu (Menu Tkinter), menuFichier (Sous-menu Tkinter), menuHelp (Sous-menu Tkinter)
            '''
            global fenjeu, game
            self.hide()
            fenjeu = Toplevel()

            #Création fenêtre
            fenjeu.geometry('%dx%d+%d+%d' % (w, h, x, y))
            fenjeu.title("Fanorona | Jouer")
            fenjeu.resizable(0,0) #Non-redimmensionnable
            fenjeu.protocol("WM_DELETE_WINDOW", askClosefenjeu) #Action si clic sur le [X] de la fenêtre
            
            icon = PhotoImage(file='media/logo.gif')
            fenjeu.tk.call('wm', 'iconphoto', fenjeu._w, icon)

            background_jeu = PhotoImage(file="media/background_jeu.png")
            background_label = Label(fenjeu, image=background_jeu)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)

            game = Canvas(fenjeu, width=wcan_jeu, height=hcan_jeu, highlightthickness=0, bg=couleur_jeu)           
            game.bind("<Button-1>", select)
            game.pack(pady=(y0,0))

            #Barre de menu
            mainmenu = Menu(fenjeu)
            
            menuFichier = Menu(mainmenu, tearoff = 0)
            menuFichier.add_command(label="Nouvelle partie", command=askrestart)
            menuFichier.add_command(label="Sauvegarder...", command=sauvegarde)
            menuFichier.add_command(label="Charger...", command=charger)
            menuFichier.add_command(label="Quitter", command=askClosefenjeu)
            
            menuHelp = Menu(mainmenu, tearoff = 0)
            menuHelp.add_command(label="A propos", command=self.openpropos)
            menuHelp.add_command(label="Règles", command=self.aide)
            
            mainmenu.add_cascade(label = "Fichier", menu=menuFichier)
            mainmenu.add_cascade(label = "Aide", menu=menuHelp)
            fenjeu.config(menu = mainmenu)

            restart()
            
            handler = lambda: self.onClosefenjeu(fenjeu)
            fenjeu.mainloop()
        
        def joueur_suivant():
            '''
            On passe au joueur suivant
            Variables : joueur (Int)
            '''
            global joueur
            if joueur == 0:
                joueur = 1
            else:
                joueur = 0

        def onClosefenjeu():
            '''
            Ferme la fenêtre de jeu
            Variables : fenjeu (Fenêtre Tkinter)
            '''
            fenjeu.destroy()
            self.show()

        def open_choix():
            '''
            Ouvre une boite de dialogue pour demander à l'utilisateur quelle prise faire (Dans le cas d'une double possibilité)
            Variables : choix (Fenêtre Tkinter), w (Int), h (Int), ws (Int), hs (Int), x (Int), y (Int), can_texte (Canvas Tkinter), can_btns (Canvas Tkinter)
            '''
            global choix
            choix = Toplevel()

            w=570
            h=100

            #Récup dimensions écran
            ws = fenjeu.winfo_screenwidth()
            hs = fenjeu.winfo_screenheight()

            #Calcul pt haut-gauche fenêtre 
            x = (ws/2) - (w/2)
            y = (hs/2) - (h/2)

            #Création fenêtre
            choix.geometry('%dx%d+%d+%d' % (w, h, x, y))
            choix.title("Fanorona | Information")
            choix.resizable(0,0) #Non-redimmensionnable
            choix.overrideredirect(1)
            choix.protocol("WM_DELETE_WINDOW", open_choix) #Action si clic sur le [X] de la fenêtre

            can_texte = Canvas(choix, highlightthickness=0)
            can_texte.pack(side='top',pady=(10,10))
            Label(can_texte,text="Le déplacement que vous venez d'effectuer peut conduire à deux types de prises de pions.\nLequel choisissez vous ?").pack()
            can_btns = Canvas(choix, highlightthickness=0)
            can_btns.pack(side='bottom',pady=(10,10))
            Button(can_btns,text="Par approche", command=choix_approche, width=15, bd=0).grid(row=0,column=0, padx=30)
            Button(can_btns,text="Par éloignement", command=choix_eloignement, width=15, bd=0).grid(row=0,column=1, padx=30)
            choix.grab_set()
        
        def place_pions():
            '''
            On place les pions
            Variables : x_pion (Int), y_pion (Int), game (Canvas Tkinter), pions_j1 (List), pions_j2 (List), couleur_j1 (Str), couleur_j2 (Str)
            '''
            #On crée les pions du J1
            for i in range(len(pions_j1)):
                x_pion = (pions_j1[i]%9)*taille_case+marge_interne
                y_pion = (pions_j1[i]//9)*taille_case+marge_interne
                game.create_oval(x_pion-rayon, y_pion-rayon, x_pion+rayon, y_pion+rayon, fill=couleur_j1, outline="white")

            #On crée les pions du J2
            for i in range(len(pions_j2)):
                x_pion = (pions_j2[i]%9)*taille_case+marge_interne
                y_pion = (pions_j2[i]//9)*taille_case+marge_interne
                game.create_oval(x_pion-rayon, y_pion-rayon, x_pion+rayon, y_pion+rayon, fill=couleur_j2, outline="black")            

        def possibilitees(num_case):
            '''
            Procédure évaluant les possibilitées de coup en fonction de la case selectionnées
            Paramètre : num_case (Int)
            Variables : libre (List), pos (List), spots (List), i (Int), xs (Int), ys (Int), xd (Int), yd (Int), dx (Int), dy (Int), joueur (Int), liste (List)
            Retourne si il y a encore des possibilitées de coups (Par défaut retourne False)
            '''
            global libre, pos, spots
            libre = []
            pos = []
            #On évalue les positions autorisées
            for i in range(45):
                if not (i in pions_j1 or i in pions_j2):
                    libre.append(i)
            #On retire les spots bannis
            for i in range(len(banned_spots)):
                libre.remove(banned_spots[i])

            #On évalue les trajets autorisés
            #Déplacement haut
            if(num_case-9) in libre:
                pos.append(num_case-9)

            #Déplacement bas
            if(num_case+9) in libre:
                pos.append(num_case+9)

            #Déplacement gauche
            if(num_case-1) in libre:
                pos.append(num_case-1)

            #Déplacement droite
            if(num_case+1) in libre:
                pos.append(num_case+1)

            #Déplacement haut-gauche
            autorise = [10, 12, 14, 16, 20, 22, 24, 26, 28, 30, 32, 34, 38, 40, 42, 44]
            if(num_case-10) in libre and num_case in autorise:
                pos.append(num_case-10)

            #Déplacement haut-droite
            autorise = [10, 12, 14, 16, 18, 20, 22, 24, 28, 30, 32, 34, 36, 38, 40, 42]
            if(num_case-8) in libre and num_case in autorise:
                pos.append(num_case-8)

            #Déplacement bas-gauche
            autorise = [0, 2, 4, 6, 8, 10, 12, 14, 18, 20, 22, 24, 26, 28, 30, 32]
            if(num_case+8) in libre and num_case in autorise:
                pos.append(num_case+8)

            #Déplacement bas-droite
            autorise = [0, 2, 4, 6, 10, 12, 14, 16, 18, 20, 22, 24, 28, 30, 32, 34]
            if(num_case+10) in libre and num_case in autorise:
                pos.append(num_case+10)
            
            #Test prise pion
            spots = []
            for i in range(len(pos)):
                xs = (num_case%9)
                ys = (num_case//9)
                xd = (pos[i]%9)
                yd = (pos[i]//9)
                dx = xd-xs
                dy = yd-ys

                if joueur == 0:
                    liste = pions_j2
                else:
                    liste = pions_j1
                
                #Déplacement haut
                if dx==0 and dy<0 and (pos[i]-num_case)==(-9) and ((pos[i]-9) in liste or (num_case+9) in liste):
                    spots.append(pos[i])

                #Déplacement bas
                if dx==0 and dy>0 and (pos[i]-num_case)==9 and ((pos[i]+9) in liste or (num_case-9) in liste):
                    spots.append(pos[i])

                #Déplacement gauche
                if dx<0 and dy==0 and (pos[i]-num_case)==(-1) and ((pos[i]-1) in liste or (num_case+1) in liste):
                    spots.append(pos[i])

                #Déplacement droite
                if dx>0 and dy==0 and (pos[i]-num_case)==1 and ((pos[i]+1) in liste or (num_case-1) in liste):
                    spots.append(pos[i])
                
                #Déplacement haut-gauche
                if dx==dy and dx<0 and (pos[i]-num_case)==(-10) and ((pos[i]-10) in liste or (num_case+10) in liste):
                    spots.append(pos[i])

                #Déplacement haut-droite
                if dx==(-1)*dy and dx>0 and (pos[i]-num_case)==(-8) and ((pos[i]-8) in liste or (num_case+8) in liste):
                    spots.append(pos[i])    

                #Déplacement bas-gauche
                if dx==(-1)*dy and dx<0 and (pos[i]-num_case)==8 and ((pos[i]+8) in liste or (num_case-8) in liste):
                    spots.append(pos[i])

                #Déplacement bas-droite
                if dx==dy and dx>0 and (pos[i]-num_case)==10 and ((pos[i]+10) in liste or (num_case-10) in liste):
                    spots.append(pos[i])

            #Résultat
            if len(spots)!=0:
                return True

        def prise_pion_approche():
            '''
            On supprime les pions capturés par une prise par approche
            Variables : dest (Int), x_pion (Int), y_pion (Int), type_move (Str), pions_j1 (List), pions_j2 (List), joueur (Int), limit (Int)
            '''
            global dest
            x_pion = (dest%9)
            y_pion = (dest//9)
            
            #Déplacement haut
            if type_move == "haut":
                for i in range(1,y_pion+1):
                    if (dest-9*i) in pions_j2 and joueur == 0:
                        pions_j2.remove(dest-9*i)
                    elif (dest-9*i) in pions_j1 and joueur == 1:
                        pions_j1.remove(dest-9*i)
                    else:
                        break                   

            #Déplacement bas
            elif type_move == "bas":
                for i in range(1,(5-y_pion)):
                    if (dest+9*i) in pions_j2 and joueur == 0:
                        pions_j2.remove(dest+9*i)
                    elif (dest+9*i) in pions_j1 and joueur == 1:
                        pions_j1.remove(dest+9*i)
                    else:
                        break

            #Déplacement gauche
            elif type_move == "gauche":
                for i in range(1,x_pion+1):
                    if (dest-i) in pions_j2 and joueur == 0:
                        pions_j2.remove(dest-i)
                    elif (dest-i) in pions_j1 and joueur == 1:
                        pions_j1.remove(dest-i)
                    else:
                        break

            #Déplacement droite
            elif type_move == "droite":
                for i in range(1, 9-x_pion):
                    if (dest+i) in pions_j2 and joueur == 0:
                        pions_j2.remove(dest+i)
                    elif (dest+i) in pions_j1 and joueur == 1:
                        pions_j1.remove(dest+i)
                    else:
                        break

            #Déplacement haut-gauche
            elif type_move == "haut-gauche":
                limit = min(5-y_pion,x_pion+1)
                for i in range(1,limit):
                    if (dest-10*i) in pions_j2 and joueur == 0:
                        pions_j2.remove(dest-10*i)
                    elif (dest-10*i) in pions_j1 and joueur == 1:
                        pions_j1.remove(dest-10*i)
                    else:
                        break

            #Déplacement haut-droite
            elif type_move == "haut-droite":
                limit = min(5-y_pion,9-x_pion)
                for i in range(1,limit):
                    if (dest-8*i) in pions_j2 and joueur == 0:
                        pions_j2.remove(dest-8*i)
                    elif (dest-8*i) in pions_j1 and joueur == 1:
                        pions_j1.remove(dest-8*i)
                    else:
                        break

            #Déplacement bas-gauche
            elif type_move == "bas-gauche":
                limit = min(y_pion+1,x_pion+1)
                for i in range(1,limit):
                    if (dest+8*i) in pions_j2 and joueur == 0:
                        pions_j2.remove(dest+8*i)
                    elif (dest+8*i) in pions_j1 and joueur == 1:
                        pions_j1.remove(dest+8*i)
                    else:
                        break

            #Déplacement bas-droite
            elif type_move == "bas-droite":
                limit = min(y_pion+1,9-x_pion)
                for i in range(1,limit):
                    if (dest+10*i) in pions_j2 and joueur == 0:
                        pions_j2.remove(dest+10*i)
                    elif (dest+10*i) in pions_j1 and joueur == 1:
                        pions_j1.remove(dest+10*i)
                    else:
                        break
        
        def prise_pion_eloignement():
            '''
            On supprime les pions capturés par une prise par éloignement
            Variables : selected (Int), x_pion (Int), y_pion (Int), i (Int), joueur (Int), pions_j1 (List), pions_j2 (List), 
            '''
            global selected
            x_pion = (selected%9)
            y_pion = (selected//9)
            
            #Déplacement haut
            if type_move == "haut":
                for i in range(1,(5-y_pion)):
                    if (selected+9*i) in pions_j2 and joueur == 0:
                        pions_j2.remove(selected+9*i)
                    elif (selected+9*i) in pions_j1 and joueur == 1:
                        pions_j1.remove(selected+9*i)
                    else:
                        break

            #Déplacement bas
            elif type_move == "bas":
                for i in range(1,y_pion+1):
                    if (selected-9*i) in pions_j2 and joueur == 0:
                        pions_j2.remove(selected-9*i)
                    elif (selected-9*i) in pions_j1 and joueur == 1:
                        pions_j1.remove(selected-9*i)
                    else:
                        break

            #Déplacement gauche
            elif type_move == "gauche":
                for i in range(1, 9-x_pion):
                    if (selected+i) in pions_j2 and joueur == 0:
                        pions_j2.remove(selected+i)
                    elif (selected+i) in pions_j1 and joueur == 1:
                        pions_j1.remove(selected+i)
                    else:
                        break

            #Déplacement droite
            elif type_move == "droite":
                for i in range(1,x_pion+1):
                    if (selected-i) in pions_j2 and joueur == 0:
                        pions_j2.remove(selected-i)
                    elif (selected-i) in pions_j1 and joueur == 1:
                        pions_j1.remove(selected-i)
                    else:
                        break

            #Déplacement haut-gauche
            elif type_move == "haut-gauche":
                limit = min(5-y_pion,9-x_pion)
                for i in range(1,limit):
                    if (selected+10*i) in pions_j2 and joueur == 0:
                        pions_j2.remove(selected+10*i)
                    elif (selected+10*i) in pions_j1 and joueur == 1:
                        pions_j1.remove(selected+10*i)
                    else:
                        break

            #Déplacement haut-droite
            elif type_move == "haut-droite":
                limit = min(5-y_pion,x_pion+1)
                for i in range(1,limit):
                    if (selected+8*i) in pions_j2 and joueur == 0:
                        pions_j2.remove(selected+8*i)
                    elif (selected+8*i) in pions_j1 and joueur == 1:
                        pions_j1.remove(selected+8*i)
                    else:
                        break

            #Déplacement bas-gauche
            elif type_move == "bas-gauche":
                limit = min(y_pion+1,9-x_pion)
                for i in range(1,limit):
                    if (selected-8*i) in pions_j2 and joueur == 0:
                        pions_j2.remove(selected-8*i)
                    elif (selected-8*i) in pions_j1 and joueur == 1:
                        pions_j1.remove(selected-8*i)
                    else:
                        break

            #Déplacement bas-droite
            elif type_move == "bas-droite":
                limit = min(y_pion+1,x_pion+1)
                for i in range(1,limit):
                    if (selected-10*i) in pions_j2 and joueur == 0:
                        pions_j2.remove(selected-10*i)
                    elif (selected-10*i) in pions_j1 and joueur == 1:
                        pions_j1.remove(selected-10*i)
                    else:
                        break
        
        def restart():
            '''
            Redémarre la partie
            Variables : pions_j1 (List), pions_j2 (List), joueur (Int), libre (List), spots (List), banned_spots (List), selected (Int)
            '''
            global pions_j1, pions_j2, joueur, libre, pos, spots, banned_spots, selected
            pions_j1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 23, 25]
            pions_j2 = [19, 21, 24, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44]
            libre = []
            pos = []
            spots = []
            banned_spots = []
            selected = -1
            joueur = 1
            game.delete(ALL)
            grille()
            place_pions()

        def sauvegarde():
            '''
            Procédure de création d'une sauvegarde
            Variables : fichier (Lien vers un fichier), joueur (Int), pions_j1 (List), pions_j2 (List), selected (Int), libre (Lis), banned_spots (List), pos (List), spots (List)
            '''
            mask = \
            [("Sauvegardes","*.sav")]
            fichier = asksaveasfile(mode='w', filetypes=mask, defaultextension=".sav")
            if fichier: #Si il y a sauvegarde (Pas clic sur Cancel)
                fichier.write("#Joueur actuel\n")
                fichier.write(str(joueur))
                fichier.write("\n#Pions J1\n")
                fichier.write(str(pions_j1))
                fichier.write("\n#Pions J2\n")
                fichier.write(str(pions_j2))
                fichier.write("\n#Pion sélectionné\n")
                fichier.write(str(selected))
                fichier.write("\n#Spots libres\n")
                fichier.write(str(libre))
                fichier.write("\n#Spots bannis\n")
                fichier.write(str(banned_spots))
                fichier.write("\n#Spots libres non-bannis\n")
                fichier.write(str(pos))
                fichier.write("\nSpots possibles\n")
                fichier.write(str(spots))

        def select(event):
            '''
            Traite les clics sur la souris
            Variables : event (Evenement Tkinter), type_move (Str), selected (Int), dest (Int), rayon (Int), taille_case (Int), ligne (Int), colonne (Int), num_case (Int), x_pion (Int), y_pion (Int), pions_j1 (List), pions_j2 (List), joueur (Int), result (Str), game (Canvas Tkinter), couleur_select (Str), spots (List), evalue (Str)
            '''
            global type_move, selected, dest
            
            #On détermine la case ou s'est passé la selection
            #Récupération des x
            if(0<=((event.y-30+rayon)%taille_case)<=40): #On vérifie que le clic n'était pas hors d'un pion
                ligne = round((event.y-30)/taille_case)
            else:
                ligne = -1
            #Récupération des y
            if(0<=(event.x-30+rayon)%taille_case)<=40: #On vérifie que le clic n'était pas hors d'un pion
                colonne = round((event.x-30)/taille_case)
            else:
                colonne = -1
            #Calcul du n° de case
            if(ligne>=0 and colonne>=0):
                num_case = ligne*9+colonne
            else:
                num_case = -1

            x_pion = (num_case%9)*taille_case+marge_interne
            y_pion = (num_case//9)*taille_case+marge_interne

            if selected == -1: #Sélection simple
                if (num_case in pions_j1 and joueur == 0) or (num_case in pions_j2 and joueur == 1): #Si le pion sélectionné appartient au joueur actuel
                    result = possibilitees(num_case)
                    if result:
                        game.create_oval(x_pion-rayon, y_pion-rayon, x_pion+rayon, y_pion+rayon, fill=couleur_select)
                        selected = num_case
                        for i in range(len(spots)):
                            ColorCase(spots[i])

            elif selected==num_case: #Re-clic sur le pion -> Désélection
                selected = -1
                game.delete(ALL)
                grille()
                place_pions()

            elif selected!=num_case and num_case not in banned_spots: #Clic sur un autre pion
                if (num_case in pions_j1 and joueur == 0) or (num_case in pions_j2 and joueur == 1): #Si le pion sélectionné appartient au joueur actuel -> Transfert de la sélection
                    selected = num_case
                    game.delete(ALL)
                    grille()
                    place_pions()
                    game.create_oval(x_pion-rayon, y_pion-rayon, x_pion+rayon, y_pion+rayon, fill=couleur_select)
                    for i in range(len(spots)):
                        ColorCase(spots[i])
                elif num_case in spots: #Clic sur un spot libre et autorisé -> Déplacement
                    banned_spots.append(selected)
                    dest = num_case
                    type_move = deplacement(dest)
                    evalue = evaluation_prise_pion()
                    if evalue == "Double":
                        open_choix()
                    elif evalue == "Approche":
                        prise_pion_approche()
                        fin_tour()
                    else:
                        prise_pion_eloignement()
                        fin_tour()
    
        interface() 
    #----------------------------------------------------------------------
if __name__ == "__main__":
    root = Tk()
    w=800
    h=600
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight() 
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.resizable(0,0)
    
    icon = PhotoImage(file='media/logo.gif')
    root.tk.call('wm', 'iconphoto', root._w, icon)
    
    background_menu = PhotoImage(file="media/background_menu.png")
    background_label = Label(root, image=background_menu)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    can=Canvas(root,width=295,height=140, bd=0, highlightthickness=0)
    photo = PhotoImage(file="media/fanorona.png")
    can.create_image(150,70,image=photo)
    can.pack()

    rayon = 20
    marge_interne = 10 + rayon

    x0 = 50-marge_interne
    xf = w - x0
    taille_case=(xf-x0-2*marge_interne)/8
    y0 = (h-4*taille_case)/2 - marge_interne
    yf = h - y0

    wcan_jeu = xf-x0
    hcan_jeu = yf-y0

    couleur_fond = 'lightgrey'
    couleur_jeu = '#D6B57B'
    couleur_j1 = 'black'
    couleur_j2 = 'white'
    couleur_select = 'orange'
    couleur_banned = 'red'
    
    app = MyApp(root)
    root.mainloop()