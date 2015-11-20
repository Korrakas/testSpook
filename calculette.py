__author__ = 'liliandelaveau'
import  abc #elle va nous permettre de gerer les classes abstraites
# coding: utf8

#classe observable, elle contient surtout une liste avec ses observers
# Ses methodes permettent de gerer cette liste
#elle contient la methode notify qui va appeler la methode update de chaque
# observer

class Observable: #pas besoin de constructeur dans ces classes

    observers=[]

    def addObserver(self, observer):
        self.observers.append(observer)

    def removeObserver(self, observer):
        self.observers.remove(observer)

    #appel de la methode update pour chaque observer
    def notify(self, datas):
        for o in self.observers:
            o.update(datas)

class Observer :
    __metaclass__=abc.ABCMeta #en python, chaque classe est un objet, des qu'on cree une classe, elle est en fait instanciee en memoire !
                             # la metaclass est la classe d'une classe. La classe observer est donc abstraite (ABC= abstract base class), elle devra etre "implementee" par d'autres classes

    #methode abstraite : chaque classe qui herite de Observer devra reimplementer cette methode
    @abc.abstractmethod
    def update(self,datas):
        return



#essai avec le pattern : la calculette. Cest une observable, on peut simuler les differentes operations + - * / et taper un entier
class Calculette(Observable):

    state=''#variable qui contient loperation, le nombre

    def getState(self):#useless
        return self.state

    def OpePlus(self):
        self.state='+'
        self.notify(self.state) #on change letat de loperateur et on le notifie à  tous les observeurs avec la methode notify dans la classe mère
    def OpeMoins(self):
        self.state='-'
        self.notify(self.state)

    def OpeFois(self):
        self.state='*'
        self.notify(self.state)

    def OpeDiv(self):
        self.state='/'
        self.notify(self.state)

    def OpeSaisirInt(self, unEntier):
        self.state=unEntier
        self.notify(self.state)

    #methode =, un peu speciale car elle annonce la fin
    def OpeEgal(self):
        self.state='='
        self.notify(self.state)#on envoie dabord le égal
        self.calcul_resultat()#on lance une méthode dans la classe calculette "car c'est elle qui contient le microprocesseur" donc elle peut réaliser des calculs plus complexes


    #methode un peu moche pour calculer le résultat du calcul, avec tous les éléments stockés dans chaque case du tableau journal
    def calcul_resultat(self):

        recuperation_journal = Journal.journal #"acces à la mémoire" de la calculette : récupération du tableau
        mon_calcul=recuperation_journal[0]#en supposant que le premier élément est forcément un chiffre/nombre

        for i in range (1,len(recuperation_journal)): #bon calcul vite fait pour calculer un truc du style 3 + 4 - 1 * 2 stocké dans le tableau

            contenu_case=recuperation_journal[i]
            if isinstance(contenu_case, str): #si la case contient un string, donc cest forcément un opérateur, on fait +=, -= etc avec le contenu de la case d'après... normalement un nombre ,(jai pas traité les cas derreurs, osef

                if contenu_case=='+':
                    mon_calcul+=recuperation_journal[i+1]
                if contenu_case=='-':
                    mon_calcul-=recuperation_journal[i+1]
                if contenu_case=='*':
                    mon_calcul*=recuperation_journal[i+1]
                if contenu_case=='/':
                    mon_calcul/=recuperation_journal[i+1]
                if contenu_case=='=':
                    break

        Journal.journal=[]# "on vide la mémoire" --> tableau remis à zéro
        self.notify(mon_calcul) #et on crie le résultat du calcul aux observers (notify revient à la classe mère Observable qui utilise la méthode update d' observers..)



class Ecran(Observer):

    #implementation de la classe abstraite update, lecran va faire des prints
    def update(self,datas):
        print('Sur l\'ecran :' , datas)




class Journal(Observer):

    journal=[]

    #idem, mais cette fois le journal est la "mémoire" et doit stocker les notifications de l'observable Calculette
    def update(self,datas):
        self.journal.append(datas) #on rajoute l'element crié par l'observable

        #petit affichage qui permet juste de suivre le remplissage du journal mais pas necessaire
        print('Contenu du journal:', end='' )
        for n in self.journal:
            print(n , end='') # mise en forme du print, normalement la valeur par défaut de end est \n pour aller à la ligne après chaque print,
                                #là en mettant null on force les éléments à rester sur la meme ligne
        print('\n')#saut à la fin de laffichage du journal





#main :-)

#instanciation des observables, des observers
maCalculette = Calculette()
monEcran = Ecran()
monJournal = Journal()

# attachement de l'observable aux observeurs
maCalculette.addObserver(monEcran)
maCalculette.addObserver(monJournal)



#on tape l'opération 3+4-1*2 =
maCalculette.OpeSaisirInt(3)
maCalculette.OpePlus()
maCalculette.OpeSaisirInt(4)
maCalculette.OpeMoins()
maCalculette.OpeSaisirInt(1)
maCalculette.OpeFois()
maCalculette.OpeSaisirInt(2)
maCalculette.OpeEgal()


