#importation des bibliothèques permettant d'acceder à une base de données, et de faire des diagrammes
import pyodbc as pc
import matplotlib as plt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#connection à la base de donnée
conn=pc.connect("DSN=bd_edumai")
#Défintion du curseur
cursor = conn.cursor()
#Définition de la fonction principale
def appli():
    #boucle permettant d'enchainer les requete comme l'user le veut
    while True:
        #entrer a faire par l'user pour choisir la requete qu'il veut faire
        reponse=int(input("""\n\nQuelle requete voulez vous choisir ?\n1-Pourcentage de logement par type de logements\n2-Moyenne de prix par type de logement\n3-Nombre de logements détenus par les hotes et les superhotes\n4-Pourcentage d'hotes et de super hotes\n999-Sortir\n"""))
        if reponse == 1 :
            requete1()
        elif reponse == 2 :
            requete2()
        elif reponse == 3 :
            requete3()
        elif reponse == 4 :
            requete4()
        #numéro permettant d'arreter le programme quand l'utilisateur le veux
        elif reponse == 999 :
            break
        #message d'erreur si l'utilisateur entre un numéro non pris en compte
        else:
            print("\nVeuillez entrer un numéro valide\n")
appli()
#requete numéro 1 : Pourcentage de logement par type de logement 
def requete1():
    while True:
    
        #entrée a faire par l'user pour choisir la requete qu'il veut faire diagramme ou une valeur précise
        reponse = int(input("\nVoulez-vous un diagramme ou le pourcentage du nombre de logement par type ?\n1-Diagramme \n2-Valeur en particulier\n"))
        if reponse == 1:
            #requete SQL pour créer le diagramme
            SQLCommand = ("""SELECT TP.logt_room_type As TypeDeLogement, 
               ROUND((count(TP.log_room_idtype)*100)/ (SELECT COUNT(*) FROM logements), 2) AS Pourcentage
        FROM logements L
        INNER JOIN types_logements TP ON L.log_room_idtype = TP.log_room_idtype 
        INNER JOIN nodenot_bd.agglo_paysbasque AP ON L.logt_codeINSEE = nodenot_bd.AP.code_insee
        GROUP BY TP.logt_room_type
        ORDER BY Pourcentage DESC;""")
            #éxécution de la requete
            cursor.execute(SQLCommand)
            #stockage du résultat de la requete dans une variable
            result = cursor.fetchall()
            #Définition des noms des barres du diagramme
            labels = ['Entire home/apt','Private room', 'Shared room','Hotel room']
            #Définition des valeurs de chaque barres
            sizes = [result[0][1], result[1][1],result[2][1],result[3][1]] 
            #Définition de la taille du diagramme
            plt.figure(figsize=(10, 6))
            #Définition du diagramme en barres
            plt.bar(labels, sizes, color='purple')
            #Définition du nom de l'axe des abscisses
            plt.xlabel('Type de Logement')
            #définition du nom de l'axe des ordonnées
            plt.ylabel('Pourcentage de logement')
            #Définition du titre du diagramme
            plt.title('pourcentage de chaque type de logements')
            #Affichage de la valeur de chaque barre à coté du nom de la barre
            plt.xticks(labels, [f'{l}\n({s}%)' for l, s in zip(labels, sizes)],rotation=45)
            #affichage du diagramme
            plt.show()
            break
        
        if reponse == 2:
            #boucle pour que la requete s'éxécute que quand une valeur correcte est entrée
            while True:
                #saisie de l'user de la valeur précise qu'il veut connaitre
                valeur = int(input("Quel type de logement en particulier voulez-vous connaitre pourcentage ?\n1-Entire home/apt \n2-Hotel room\n3-Private room\n4-Shared room\n"))
                #Définition du paramètre de la requete SQL
                if valeur == 1 :
                    filtre = "Entire home/apt"
                    break
                elif valeur == 2:
                    filtre = "Hotel room"
                    break
                elif valeur == 3:
                    filtre = "Private room"
                    break
                elif valeur == 4:
                    filtre = "Shared room"
                    break
                #Gestion de l'erreur si l'user rentre une valeur autre que celles attendues
                else:
                    print("Veuillez entrer un réponse valide")
            #Définition de la requete SQL paramétrée
            SQLCommand = ("""SELECT TP.logt_room_type As TypeDeLogement, 
               ROUND((count(TP.log_room_idtype)*100)/ (SELECT COUNT(*) FROM logements), 2) AS Pourcentage
        FROM logements L
        INNER JOIN types_logements TP ON L.log_room_idtype = TP.log_room_idtype 
        INNER JOIN nodenot_bd.agglo_paysbasque AP ON L.logt_codeINSEE = nodenot_bd.AP.code_insee
        WHERE TP.logt_room_type = ?
        GROUP BY TP.logt_room_type
        ORDER BY Pourcentage DESC;""")
            #Définition du paramètre choisi par l'user
            param = (f'{filtre}')
            #éxécution de la requete avec la paramètre
            cursor.execute(SQLCommand,param)
            #affichage du résultat de la requete
            for row in cursor.fetchall():
                print(f"Type de logement : {row[0]} \nPourcentage du nombre de logement : {round(row[1], 2)} %")
            break
        else:
            print("\nVeuillez entrer une réponse correcte\n")
        
#requete numéro 2 : Moyenne de prix par type de logement 
def requete2():
    while True:

        #entrée a faire par l'user pour choisir la requete qu'il veut faire diagramme ou une valeur précise
        reponse = int(input("Voulez-vous un diagramme ou la moyenne de prix par type de logement pour un type de logement en particulier ?\n1-Diagramme \n2-Prix en particulier\n"))
        if reponse == 1 :
            #requete SQL pour créer le diagramme
            SQLCommand = """
            SELECT TP.logt_room_type AS TypeDeLogement, ROUND(AVG(logt_prix), 2) AS MoyennePrix
            FROM logements L
            INNER JOIN nodenot_bd.agglo_paysbasque AG ON L.logt_codeINSEE = nodenot_bd.AG.code_insee
            INNER JOIN types_logements TP ON L.log_room_idtype = TP.log_room_idtype
            GROUP BY TP.log_room_idtype
            ORDER BY MoyennePrix DESC;
            """
            #éxécution de la requete
            cursor.execute(SQLCommand)
            #stockage du résultat de la requete dans une variable
            result = cursor.fetchall()
            #définition des noms des partis du diagramme
            labels = ['Entire home/apt', 'Hotel room', 'Private room', 'Shared room']
            #définition des valeurs du diagramme
            sizes = [result[0][1], result[1][1],result[2][1],result[3][1]] 
            #définition de la taille du diagramme
            plt.figure(figsize=(10, 6))
            #définition du diagramme en barres
            plt.bar(labels, sizes, color='skyblue')
            #définition du nom de l'axe des abscisses
            plt.xlabel('Type de Logement')
            #définition du nom de l'axe des ordonnées
            plt.ylabel('Prix Moyen (€)')
            #définition du titre du diagramme
            plt.title('Prix Moyen par Type de Logement')
            #rotation des noms de chaque barres pour une meilleure lisibilité
            plt.xticks(rotation=45)
            #affichage du diaramme
            plt.show()
            break
        #Deuxieme possibilité de réponse une valeur précise
        elif reponse == 2 :
            #choix par l'user de la valeur précise qu'il veut
            valeur=int(input("Quel type de logement en particulier voulez-vous connaitre la moyenne de prix ?\n1-Entire home/apt \n2-Hotel room\n3-Private room\n4-Shared room\n"))
            #boucle pour avoir toujours une valeur correcte
            while True:
                #définition du filtre pour la requete paramétrée
                if valeur == 1 :
                    filtre = "Entire home/apt"
                    break
                elif valeur == 2:
                    filtre = "Hotel room"
                    break
                elif valeur == 3:
                    filtre = "Private room"
                    break
                elif valeur == 4:
                    filtre = "Shared room"
                    break
                else:
                    print("Veuillez entrer un réponse valide\n")
            #définition de la requete SQL paramétrée
            SQLCommand = """
            SELECT TP.logt_room_type AS TypeDeLogement, ROUND(AVG(logt_prix), 2) AS MoyennePrix
            FROM logements L
            INNER JOIN nodenot_bd.agglo_paysbasque AG ON L.logt_codeINSEE = nodenot_bd.AG.code_insee
            INNER JOIN types_logements TP ON L.log_room_idtype = TP.log_room_idtype
            WHERE TP.logt_room_type = ?
            GROUP BY TP.log_room_idtype
            ORDER BY MoyennePrix DESC;
            """
            #définition du paramètre
            param = (f'{filtre}')
            #écéution de la requete SQL avec un paramètre
            cursor.execute(SQLCommand,param)
            #affichage du résultat de la requete
            for row in cursor.fetchall():
                print(f"Type de logement : {row[0]} \nMoyenne de prix de ce type de logement : {round(row[1], 2)} ")
            break
        else:
            print("\nVeuillez entrer une réponse correcte\n")

#requete numéro 3 : Nombre de logement détenu par super hôtes
def requete3():
    while True:
        
        #entrée a faire par l'user pour choisir la requete qu'il veut faire diagramme ou une valeur précise
        reponse = int(input("Voulez-vous un diagramme ou le nombre de logement qui sont détenus par des hotes ou des superhotes ?\n1-Diagramme \n2-Valeur en particulier\n"))
        if reponse == 1 : 
            #requete SQL pour créer le diagramme
            SQLCommand = ("""SELECT COUNT(*) AS nombre_total_logements, (SELECT COUNT(*) 
    FROM logements AS l
    JOIN hosts AS h ON l.host_id = h.host_id
    WHERE h.host_is_superhost = 1) AS nombre_logements_superhosts
    FROM logements l;
    """)
            #éxécution de la requete
            cursor.execute(SQLCommand)
            #stockage des résultat de la requete dans une variable
            result = cursor.fetchone()
            #définition des noms des partis du diagramme
            labels = ['Hotes', 'SuperHotes']
            #definition des valeur du diagramme
            sizes = [result[0], result[1]]   
            #Définition du diagramme
            plt.pie(sizes, labels=labels, autopct=lambda p: f"{int(p/100.*sum(sizes))}", startangle=90)
            #rendre les axes égaux
            plt.axis('equal')
            #définition du titre
            plt.title('Nombre de logement répartit entre les hotes et les super hotes')
            #affichage du diagramme
            plt.show()
            break
        #Deuxieme possibilité de réponse une valeur précise
        elif reponse == 2:
            
            while True:
                #choix de la valeur précise
                valeur = int(input("Voulez-vous le nombre de logements détenus par : \n1- Les hotes\n2- Les SuperHotes\n"))
                #valeur précise : Nombre de logements détenus par des hotes       
                if valeur == 1 : 
                    #Définition de la commande SQL
                    SQLCommand = ("""SELECT COUNT(*) AS nombre_total_logements, (SELECT COUNT(*) 
            FROM logements AS l
            JOIN hosts AS h ON l.host_id = h.host_id
            WHERE h.host_is_superhost = 1) AS nombre_logements_superhosts
            FROM logements l;
            """)
                    #éxécution de la commande
                    cursor.execute(SQLCommand)
                    #affichage du résultat de la commande 
                    for row in cursor.fetchall():
                        print(f"Nombre de logements détenus par des hotes : {row[0]} logements")
                    break
                #valeur précise : Nombre de logements détenus par des super hotes
                elif valeur == 2 : 
                    #définition de la commande SQL
                    SQLCommand = ("""SELECT COUNT(*) AS nombre_total_logements, (SELECT COUNT(*) 
            FROM logements AS l
            JOIN hosts AS h ON l.host_id = h.host_id
            WHERE h.host_is_superhost = 1) AS nombre_logements_superhosts
            FROM logements l;
            """)
                    #éxécution de la commande
                    cursor.execute(SQLCommand)
                    #affichage du résultats de la commande 
                    for row in cursor.fetchall():
                        print(f"Nombre de logements détenus par des super-hotes : {row[1]} logements")
                    break
                else:
                    print("Veuillez entrer une valeur correcte")
            break
        else:
            print("\nVeuillez entrer une réponse correcte\n")
#requete numéro 4 : Pourcentage d'hôtes et de super hôtes
def requete4():
    while True:
        
        #entrée a faire par l'user pour choisir la requete qu'il veut faire diagramme ou une valeur précise
        reponse=int(input("Voulez-vous un diagramme ou une valeur en particulier ?\n1-Diagramme \n2-Valeur en particulier \n"))
        if reponse == 1:
            #requete SQL pour créer le diagramme
            SQLCommand = ("""SELECT
          ROUND(SUM(CASE WHEN host_is_superhost THEN 1 ELSE 0 END) / COUNT(*),2) * 100 AS pourcentage_superhotes,
          ROUND(SUM(CASE WHEN NOT host_is_superhost THEN 1 ELSE 0 END) / COUNT(*),2) * 100 AS pourcentage_hotes
        FROM hosts;
        """)
            #éxécution de la requete
            cursor.execute(SQLCommand)
            #stockage des résultat de la requete dans une variable
            results = cursor.fetchone()
            #définition des noms des partis du diagramme
            labels = ['Superhôtes', 'Hôtes']
            #definition des valeur du diagramme
            sizes = [results[0], results[1]] 
            #définition de la taille du diagramme
            plt.figure(figsize=(8, 6))
            #défintion du diagramme
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            #rendre les axes égaux
            plt.axis('equal')  
            
            # Titre du diagramme
            plt.title('Pourcentage de Superhôtes vs Hôtes')
            #affichage du diagramme
            plt.show()
            break
        #Deuxieme possibilité de réponse une valeur précise
        elif reponse == 2:
            #choix de la valeur précise
            valeur = int(input("Voulez-vous le pourcentage de superhote ou le pourcentage d'hote ?\n1- Super-Hote \n2- Hote\n"))
            #valeur du pourcentage de super hotes
            if valeur == 1:
                #définition de la requete SQL
                SQLCommand = ("""SELECT
              ROUND(SUM(CASE WHEN host_is_superhost THEN 1 ELSE 0 END) / COUNT(*),2) * 100 AS pourcentage_superhotes,
              ROUND(SUM(CASE WHEN NOT host_is_superhost THEN 1 ELSE 0 END) / COUNT(*),2) * 100 AS pourcentage_hotes
            FROM hosts;
            """)
                #éxécution de la requete SQL
                cursor.execute(SQLCommand)
                #affichage du pourcentage de super hotes
                for row in cursor.fetchall():
                    print(f"Pourcentage de super hotes : {row[0]} %")
            #valeur du pourcentage d'hotes
            elif valeur == 2:
                #définition de la requete SQL
                SQLCommand = ("""SELECT
              ROUND(SUM(CASE WHEN host_is_superhost THEN 1 ELSE 0 END) / COUNT(*),2) * 100 AS pourcentage_superhotes,
              ROUND(SUM(CASE WHEN NOT host_is_superhost THEN 1 ELSE 0 END) / COUNT(*),2) * 100 AS pourcentage_hotes
            FROM hosts;
            """)
                #éxécution de la requete SQL
                cursor.execute(SQLCommand)
                #affichage du pourcentage d'hotes
                for row in cursor.fetchall():
                    print(f"Pourcentage d'hotes : {row[1]} %")
            break
        else:
            print("\nVeuillez entrer une valeur correcte\n")
