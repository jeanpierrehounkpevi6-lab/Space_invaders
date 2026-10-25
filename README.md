# Space_invaders
Jeu video  où il defender cherche à se débarraser des aliens.

COMPTE RENDU PROJET SPACE INVADERS

Documentation des classes :
1)	La classe Alien
Cibles du jeu, self.alive définit si l’alien est en vie ou non.
Méthodes de classe :
-touched_by : prends en paramètre la balle (projectile) et le canvas. La méthode permet de savoir si l’alien est touché par le projectile via comparaison des coordonnées via la methode canva.coords et canvas.bbox (sur l’id de la balle) (collision x et collision y ).
Canvas.coords n’a pas été utilisé sur la l’alien car lors de l’implémentation de l’image, il renvoie seulement les cordonnées du point d’ancrage (le point au centre de l’image) alors que bbox renvoie la la boite de place prise par l’alien, donc les coordonnées des deux points haut-gauche et bas-droite.
Si les deux conditions sont remplies alors self.alien sera changé et vaudra false pour l’alien en question.

-install_in : nous permet d’ajouter l’alien sur notre canvas et prend en paramètre la position x,y et l’image. 

-move_in : prend en paramètre le déplacement x et y mais aussi une condition, qui va déterminer la direction de ce déplacement ( une fois sur deux sera à droite gauche grâce au if condition%2==1)


2)	La classe fleet
Ensemble d’aliens qui bougent ensemble avec des méthodes appelant tous les aliens de la classe.

	Variables de classe :
		-Condition : initialisée à 0, va déterminer la direction du déplacement des aliens.
		-Score : initialisé à 0, s’incrémente à chaque alien touché
Méthodes de classe : 

-install_in : va installer une flotte d’aliens sur notre canvas grâce à l’appel de la méthode install_in de la classe Alien dans une double boucle (pour les lignes et colonnes) le x est augmenté de 30 à chaque création d’un alien (on aurait pu utiliser le self.alien_gap) et est réinitialisé à 0 pour chaque lignes. Le y est augmenté de 30 aussi pour chaque ligne d’aliens.

-move_in : va définir le déplacement des aliens selon plusieurs conditions (si les aliens sont aux bords du canvas, si ils doivent se déplacer verticalement…)
Move_in appelle la méthode des aliens avec comme condition la variable de classe self.condition (qui vaudra donc 1 ou 0).

-react_touché_aliens : prend en paramètre le canva et le defender.
Une liste d’aliens et de balles à supprimer du canva sera crée et les aliens touchés seront ajoutés aux boucles grâce à une double boucle qui prend tous les aliens et balles en compte et exécute la fonction touched_by pour chacun d’entre eux.
Pour un alien touché (self.alive ==false) la boucle est arretée et il est ajouté dans la boucle d’aliens à supprimer et la balle correspondante aussi. Ils vont être supprimés de leurs listes de classe (flotte et self.balles ) via deux autres boucles et supprimés du canvas en même temps.


3)	La classe Bullet
Projectile qui détermine si un alien est vivant en fonction des coordonnées.
Les méthodes de classe :
Install_in et move_in : permettent de placer une balle et de la déplacer dans le canvas.

4)	La classe Defender
Va permettre d’ajouter et de tirer les balles en direction des aliens.
Méthodes de classe :
-install_in : ajoute le defender au centre du canvas
-moveorBackdef : va faire déplacer le defender à l’autre côté du canvas si il touche une des bordures.
-Fire_ball : crée une balle devant le defender si le nombre de balles maximum n’est pas dépassé (8 balles). Cette fonction va aussi enlever les balles qui dépassent la hauteur du canvas de la liste de balles grâce à une liste intermédiaire de balles à supprimer (balls_remove).
-move_in : permet de déplacer horizontalement le defender via le paramètre dx.

5)	La classe Score
Va contenir les méthodes qui permettent d’enregistrer et de lire les scores dans le fichier scores.json.
Méthodes de classe :
-scoretofile : prends en paramètre le nom d’un fichier et s’il est bien trouvé, va d’abord lire les données du fichier pour les mettre dans une liste (si les données sont déjà enregistrées sous forme de liste) puis ajoute le score de la partie dans la le score (grâce à la méthode .dict qui va retourner l’objet sous forme de dictionnaire) précédemment lue pour ne pas écraser les données des précédentes parties.
Après ça, le score est ajouté dans le fichier et celui-ci va être définitivement fermé.
-scorefromfile methode de classe : va retourner la liste de scores enregistrée dans le fichier score.json

6)	La classe Game
Elle contient le canvas, les classes fleet, Defender Score. Elle gère les différentes animations de ces classes.

Variable de classe, continue_game : initialisée à True, permet de déterminer si les animations du jeu vont se poursuivre ou non.

Les méthodes de classe :
-animation : va être appelée toutes les 100ms et appelle react_touché_aliens. Elle va aussi permettre de vérifier les conditions de fin de jeu : si tous les aliens sont morts (len(flotte_alien)==0) ou si les aliens ont atteints le defender (canvas.bbox(‘alien’)[3]>= 565). 
Elle va changer la variable de classe continue_game à False et va faire afficher un message en fonction de si l’utilisateur a gagné ou perdu. Il sera ensuite demandé s’il veut enregistrer son score et en fonction de la réponse va appeler registerscore ou affichfin.
-registerScore : crée un attribut self.entry_1 qui va permettre de prendre le nom de l’utilisateur, puis, avec le boutton ‘valider’(self.bout) va appeler la fonction validatedregister.
-affichfin : permet d’afficher le dernier score enregistré dans scores.json via deux labels. Si aucun score n’est renseigné/le fichier n’est pas trouvé, on afficherera qu’aucun score n’à été renseigné.
-validatedregister : va enregistrer le nom précédemment renseigné par l’utilisateur grâce au entry_1.get et crée un nouveau score avec le nom de l’utilisateur et son score pendant la partie.
Ce score va être enregistré dans le scores.json avec l’appel de scoretofile.
-move_bullets : si le jeu n’est pas fini, appelle balle move_in chaque 20 ms.
-move_aliens_fleet : chaque 300 ms move_in  de la flotte est appelé si le jeu n’est pas fini.
-left_right : permet de faire bouger notre defender et aussi de tirer la balle en appuyant sur espace.
-start : appelle toutes les fonctions d’animation nécessaires pour commencer le jeu et permet d’assigner les boutons à notre canvas et à la fonction left_right.

7)	La classe SpaceInvaders
Contient le jeu et donc permet de faire appel aux autres classes contenues dans game.
La seule méthode contenue est play et permet de commencer la partie en appelant start et le mainloop de notre Tk.


Points critiques / améliorations :
-	Suppression de balles dans Fire_ball : les deux boucles de suppression devraient être au début de la fonction car si on a déjà atteint la limite de balles, les commandes pour tirer ne seront pas excécutées et la balle qui dépasse le canvas sera suprimée sans création d’une autre balle (obligé d’appuyer 2 fois sur space pour qu’une autre balle soit fired).
-	Pas de fonction pour restart, pas de menu de début, pas d’affichage de meilleur score.
-	Potentiel rajout de fonctions de customisation (self.couleur pour les balles ou la couleur des defenders)

