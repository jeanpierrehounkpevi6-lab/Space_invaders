import tkinter as tk
from tkinter import * 
import random as rd
import tkinter.messagebox as tkMessagebox
from PIL import Image, ImageTk
import json
import _asyncio




class Alien(object):

    def __init__(self):
        self.id= None
        self.alive=True
        self.pim=None
        self.image_alien=None
        self.siz = 20

    def touched_by(self,canvas,projectile):
        coordBalle = canvas.coords(projectile)
        coordalien = canvas.bbox(self.id)
        colx = (coordBalle[2]>coordalien[0] and coordBalle[0]<coordalien[2])
        coly = (coordBalle[3]>coordalien[1] and coordBalle[1]<coordalien[3])
        if colx and coly:
            self.alive = False
    
    def install_in(self,canvas,x,y,image):
        self.image_alien=Image.open(image)
        self.image_alien = self.image_alien.resize((25,25))
        self.pim=ImageTk.PhotoImage(self.image_alien)
        self.id=canvas.create_image(x,y,image=self.pim,tags='alien')
        canvas.pim=self.pim


    def move_in(self,canvas,dx,dy,condition):             
        deltax = dx
        deltay = dy
        
        if condition%2 == 1:
            deltax = -deltax
        canvas.move(self.id, deltax,deltay)
                    

            
class fleet(object):
    condition = 0           #Elle représente notre condition de déplacement de fleet
    score = 0
    def __init__(self):
        self.alien_lignes = 5
        self.alien_colonnes = 10
        self.alien_gap_inter = 20
        self.alien_x_delta = 15
        self.alien_y_delta = 25
        self.alien_Obj=Alien()
        flotte_size= self.alien_lignes*self.alien_colonnes 
        self.flotte_alien = []

        
        
    def install_in(self,canvas):
        x,y=0,0
        for i in range (self.alien_lignes):
            for j in range (self.alien_colonnes):
                new_alien=Alien()
                new_alien.install_in(canvas,x,y,'alien.png')
                self.flotte_alien.append(new_alien)
                x+=30
            x=0
            y+=30

    def move_in(self,canvas):                                          #condition est utilisé pour changer le sens du déplacement des aliens
        x,y=self.alien_x_delta,0
        if(canvas.bbox('alien')[0]<=0 or canvas.bbox('alien')[2]>=500):
            y=self.alien_y_delta
        if(canvas.bbox('alien')[2]>500):
            self.condition+=1
        if(self.condition == 1 and canvas.bbox('alien')[0]<=0):                  #la valeur de la variable de classe va deteriner si le mouvement est à gauche ou à droite(%2)
            self.condition = 0                         
        for i in range (len(self.flotte_alien)):
            self.flotte_alien[i].move_in(canvas,x,y,self.condition)


    def reac_touché_aliens(self,canvas,defender):
        bullets_touched = []
        aliens_touched = []
        for i in range(0,len(self.flotte_alien)):
            alien = self.flotte_alien[i]
            for z in range(0,len(defender)):
                alien.touched_by(canvas,defender[z].id)
                if(alien.alive == False):
                    aliens_touched.append(alien)                #le break dans la boucle permet de ne pas ajouter les autres instances de bullet dans la liste de balles à supp
                    bullets_touched.append(defender[z])
                    break
        for A in aliens_touched:                                 #ça bug très fort si suppression dans boucle précédante
            canvas.delete(A.id)
            if A in self.flotte_alien:
                self.flotte_alien.remove(A)
                fleet.score = self.score +20
        for B in bullets_touched:
            canvas.delete(B.id)
            if B in defender:
                defender.remove(B)

        
class Bullet(object):                                   
    def __init__(self,shooter):
        self.speed = 8
        self.gap = 5
        self.color = 'red'
        self.id = None
        self.shooter = shooter
        
    
    def install_in(self,canva,x,y):                 #la balle se forme un peut devant le defender, creer une fonction animer pour avancer la balle et faire un compteur pour le nombre de balles max(8)
        self.id = canva.create_oval(x,y, x+self.gap, y-self.gap, fill=self.color, tags='bullet')

    def move_in(self,canvas):
        canvas.move(self.id,0,-self.speed)


class Defender(object):
    def __init__(self):
        self.rect = None 
        self.long = 20
        self.larg = 15
        self.ball = Bullet(self.rect)
        self.max_balles_tir = 8
        self.balles = []
    
    def install_in(self,canvas):
        x,y = 225, 565
        self.rect = canvas.create_rectangle(x,y,x+self.long,y+self.larg, fill='pink')


    def MovorBackdef(self,canvas):                       #apparition de l'autre côté de la fenetre
        coord = canvas.coords(self.rect)                 #mettre fonc dans appli et utiliser deux conditionnelles pour le + et 
        if(coord[0] < 0 ):
            canvas.move(self.rect, 450,0)
        elif(coord[2]>500):
            canvas.move(self.rect, -450,0)
            
    def Fire_ball(self,canvas):                                  #création et ajout d'un nouvel objet balle dans la liste.
        balls_remove = []
        if(len(self.balles) < self.max_balles_tir):
            coordrect = canvas.coords(self.rect)
            x = coordrect[0] + 5
            y = coordrect[1] - 5
            new_ball = Bullet(self.rect)
            new_ball.install_in(canvas,x,y)
            self.balles.append(new_ball)
        for e in self.balles:
            if(canvas.coords(e.id)[1]<0):
                balls_remove.append(e)
        for z in balls_remove:
            canvas.delete(z.id)
            self.balles.remove(z)

    def move_in(self,canvas,dx):
        canvas.move(self.rect, dx, 0)
        self.MovorBackdef(canvas)
    

class Score(object):
    def __init__(self,nom,score):
        self.nom = nom
        self.score = score

    def scoretofile(self,file):
        try: 
            with open(file,'r') as f:
                scores = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):     #lit quand même si fichier vide ou erreur
            scores = []
        d = self.__dict__
        scores.append(d)
        f.close()
        f = open(file,'w')    #prend ancient scores pour ajouter à ceux-ci le nouveau avant de l'envoyer dans le fichier
        json.dump(scores,f)
        f.close()

    @classmethod
    def scorefromfile(cls,file):
        f=open(file,"r")
        lscores = json.load(f)
        f.close()
        return lscores
    

class Game(object):
    continue_game = True
    def __init__(self,fenetre):
        self.fenetre = fenetre
        self.width = 500
        self.heigth = 600
        self.defender = Defender()
        self.flotte = fleet()
        self.score = Score(None,None)
        self.canvas = tk.Canvas(self.fenetre, width=self.width, height=self.heigth,background="black")
        self.canvas.pack()
        self.defender.install_in(self.canvas)
        self.flotte.install_in(self.canvas)
        
        
    
    def animation(self):                                                                       
        self.flotte.reac_touché_aliens(self.canvas,self.defender.balles)        #la condition ici va permettre d'arreter directement l'animation des élements
        if(Game.continue_game == True):                                     #les scores et noms vont être affichés et demandés si l'utilisateur le veut
            if(len(self.flotte.flotte_alien) == 0):                          #si non renseignés, le jeu affiche l'encient score enregistré(erreur si aucun score par contre)
                Game.continue_game = False
                tkMessagebox.showinfo("Gagné !!!","vous avez sauvé la planète !" )
                ask = tkMessagebox.askquestion(title='fin de jeu', message='voulez vous enregistrer votre score ?')  
                if(ask=='yes'):
                    self.registerScore()
                else:
                  self.affichfin()          
                    
            elif (self.canvas.bbox('alien')[3]>= 565 ): 
                Game.continue_game = False
                tkMessagebox.showinfo("Game Over", "Les aliens vous ont eue ! :(")
                ask = tkMessagebox.askquestion(title='fin de jeu', message='voulez vous enregistrer votre score ?')
                if(ask=='yes'):
                    self.registerScore()
                    
                else:
                    self.affichfin()
            
            self.canvas.after(100, self.animation)

    def registerScore(self):
        self.entry_1 = Entry(self.canvas) #html input type text :()
        self.canvas.create_window(200,125, window=self.entry_1)
        lab = tk.Label(self.canvas, text='entrez votre nom : ')
        self.canvas.create_window(200,100, window=lab)
        self.bout = Button(text='valider !',command=self.validatedregister)
        self.windbout = self.canvas.create_window(225,150, window=self.bout)
        #await _asyncio.sleep(0.5) en utilisant async ça bug :(
        #self.affichfin()         faire en sorte que l'execution de la fonction se fasse après avoir appuié sur le bouton
    
    def affichfin(self):    #affiche ancient score si renseigné 
        lab1 = tk.Label(self.canvas,text="merci d'avoir joué, votre score : "+str(fleet.score)+ ". Dernier score enregistré:")
        self.canvas.create_window(225,300,window=lab1)
        try : 
            anciensc = Score.scorefromfile('scores.json')[0] #bug avec with car renvoie un dic
            txt = tk.Label(self.canvas,text=str(anciensc))
            self.canvas.create_window(225,320,window=txt)
        except (FileNotFoundError, json.JSONDecodeError):
            txt = tk.Label(self.canvas,text="aucun score precedemment enregistré.")
            self.canvas.create_window(225,320,window=txt)

    def validatedregister(self):
        nom = self.entry_1.get()
        self.canvas.delete(self.windbout)
        txt = tk.Label(self.canvas,text="votre score a été enregistré !")
        self.canvas.create_window(225,320,window=txt)
        new_score = fleet.score
        next_score = Score(nom,new_score)
        next_score.scoretofile('scores.json')

    #def restart ?

    
    #def affichScore(self,) devra afficher le meilleur score avec le score obtenu dans la partie en question.

    def move_bullets(self):
        if(Game.continue_game == True):
            for ball in self.defender.balles :
                ball.move_in(self.canvas)

            self.canvas.after(40,self.move_bullets)
        
    def start_animation(self):
        self.canvas.after(100,self.animation)


    def move_aliens_fleet(self):
        if(Game.continue_game==True):         
            self.flotte.move_in(self.canvas)
            self.canvas.after(180,self.move_aliens_fleet)


    def left_right(self,event):
        if(Game.continue_game):
            gap = 10 
            if event.keysym == 'space':                     #ajouter une autre maniere de tirer balle ? quand 'x' tirer 3 balles dans 3 directions différentes
                self.defender.Fire_ball(self.canvas)
            if event.keysym == 'Left':
                self.defender.move_in(self.canvas,-gap)
            elif event.keysym == 'Right':
                self.defender.move_in(self.canvas,gap)

    def start(self):
        self.start_animation()
        self.move_aliens_fleet()
        self.move_bullets()
        self.canvas.focus_set()
        self.canvas.bind("<Key>", self.left_right)
        self.animation()


class SpaceInvaders(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Space Invaders")
        self.fenetre = tk.Frame(self.root)
        self.fenetre.pack(side="top", fill="both")
        self.game = Game(self.fenetre)

    def play(self):
        self.game.start()
        self.root.mainloop()
    


SpaceInvaders().play()