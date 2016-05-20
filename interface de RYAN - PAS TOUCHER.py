from tkinter import *
import webbrowser

class MyApp():
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
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
        """"""
        self.root.withdraw()
        
    def aide(self):
        webbrowser.open('http://fanorona.16mb.com/regles.html')
       
    #----------------------------------------------------------------------
    def openjouer(self):
        """"""
        self.hide()
        fenjeu = Toplevel()
        w=800
        h=600
        ws = fenjeu.winfo_screenwidth()
        hs = fenjeu.winfo_screenheight() 
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        fenjeu.geometry('%dx%d+%d+%d' % (w, h, x, y))
        fenjeu.title("Fanorona | Jouer")
        
        handler = lambda: self.onClosefenjeu(fenjeu)
        btn = Button(fenjeu, text="Retour", command=handler, width=15)
        btn.pack(pady=5)
    
    def openpropos(self):
        """"""
        fenpropos = Toplevel()
        w=400
        h=200
        ws = fenpropos.winfo_screenwidth()
        hs = fenpropos.winfo_screenheight() 
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        fenpropos.geometry('%dx%d+%d+%d' % (w, h, x, y))
        fenpropos.title("Fanorona | A propos")
        
        label = Label(fenpropos, text="Fanorona a été crée par Ryan, Yoan et Mathieu \n pour le projet ISN 2016")
        label.pack(pady=50)
        
        handler = lambda: self.onClosefenpropos(fenpropos)
        btn = Button(fenpropos, text="Fermer", command=handler, width=15)
        btn.pack(pady=10)
                
     
    #----------------------------------------------------------------------
    def onClosefenjeu(self, fenjeu):
        """"""
        fenjeu.destroy()
        self.show()
        
    def onClosefenpropos(self, fenpropos):
        fenpropos.destroy()
        
    def quitter(self):
        self.root.destroy()
            
    #----------------------------------------------------------------------
    def show(self):
        """"""
        self.root.deiconify()    
    
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
    
    background_image = PhotoImage(file="background.png")
    background_label = Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    can=Canvas(root,width=295,height=140, bd=0, highlightthickness=0)
    photo = PhotoImage(file="fanorona.png")
    can.create_image(150,70,image=photo)
    can.pack()  
    
    app = MyApp(root)
    root.mainloop()
