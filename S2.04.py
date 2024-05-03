import pyodbc as pc
import matplotlib as plt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
conn=pc.connect("DSN=bd_edumai")
cursor = conn.cursor()
#importation d'une bibliothèque permettant d'acceder à une base de données

#definitions d'un curseur
cursor = conn.cursor()
RefArticles = []
qteStockArticles = []


def requete1():
    SQLCommand = ("""SELECT TP.logt_room_type As TypeDeLogement, 
       ROUND((count(TP.log_room_idtype)*100)/ (SELECT COUNT(*) FROM logements), 2) AS Pourcentage
FROM logements L
INNER JOIN types_logements TP ON L.log_room_idtype = TP.log_room_idtype 
INNER JOIN nodenot_bd.agglo_paysbasque AP ON L.logt_codeINSEE = nodenot_bd.AP.code_insee
GROUP BY TP.logt_room_type
ORDER BY Pourcentage DESC;""")
    cursor.execute(SQLCommand)
    for row in cursor.fetchall():
        print(f"{row[0]}: {round(row[1], 2)}")
requete1()
def requete2():
    SQLCommand = """
    SELECT TP.logt_room_type AS TypeDeLogement, ROUND(AVG(logt_prix), 2) AS MoyennePrix
    FROM logements L
    INNER JOIN nodenot_bd.agglo_paysbasque AG ON L.logt_codeINSEE = nodenot_bd.AG.code_insee
    INNER JOIN types_logements TP ON L.log_room_idtype = TP.log_room_idtype
    GROUP BY TP.log_room_idtype
    ORDER BY MoyennePrix DESC;
    """
    cursor.execute(SQLCommand)
    for row in cursor.fetchall():
        print(f"{row[0]}: {round(row[1], 2)}")  # Round to 2 decimal places when printing

requete2()
def requete3():
    SQLCommand = ("""SELECT COUNT(*) AS nombre_total_logements, (SELECT COUNT(*) 
FROM logements AS l
JOIN hosts AS h ON l.host_id = h.host_id
WHERE h.host_is_superhost = 1) AS nombre_logements_superhosts
FROM logements l;
""")
    cursor.execute(SQLCommand)
    for row in cursor.fetchall():
        print(row)
requete3()
def requete4():
    reponse=int(input("Voulez - vous un diagramme ou une valeur en particulier ?\n1-Diagramme \n2-Valeur en particulier \n"))
    if reponse == 1:
        SQLCommand = ("""SELECT
      ROUND(SUM(CASE WHEN host_is_superhost THEN 1 ELSE 0 END) / COUNT(*),2) * 100 AS pourcentage_superhotes,
      ROUND(SUM(CASE WHEN NOT host_is_superhost THEN 1 ELSE 0 END) / COUNT(*),2) * 100 AS pourcentage_hotes
    FROM hosts;
    """)
        cursor.execute(SQLCommand)
        results = cursor.fetchone()
        print("TTTTTTTTTTTTTTTT")
        labels = ['Superhôtes', 'Hôtes']
        sizes = [results[0], results[1]] 
        plt.figure(figsize=(8, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')  
        
        # Titre
        plt.title('Pourcentage de Superhôtes vs Hôtes')
        plt.show()
    elif reponse == 2:
        valeur = int(input("Voulez - vous le pourcentage de superhote ou le pourcentage d'hote ?\n1- Super-Hote \n2- Hote\n"))
        if valeur == 1:
            
            SQLCommand = ("""SELECT
          ROUND(SUM(CASE WHEN host_is_superhost THEN 1 ELSE 0 END) / COUNT(*),2) * 100 AS pourcentage_superhotes,
          ROUND(SUM(CASE WHEN NOT host_is_superhost THEN 1 ELSE 0 END) / COUNT(*),2) * 100 AS pourcentage_hotes
        FROM hosts;
        """)
            cursor.execute(SQLCommand)
            for row in cursor.fetchall():
                print(f"Pourcentage de super hotes : {row[0]} %")
        elif valeur == 2:
            
            SQLCommand = ("""SELECT
          ROUND(SUM(CASE WHEN host_is_superhost THEN 1 ELSE 0 END) / COUNT(*),2) * 100 AS pourcentage_superhotes,
          ROUND(SUM(CASE WHEN NOT host_is_superhost THEN 1 ELSE 0 END) / COUNT(*),2) * 100 AS pourcentage_hotes
        FROM hosts;
        """)
            cursor.execute(SQLCommand)
            for row in cursor.fetchall():
                print(f"Pourcentage d'hotes : {row[1]} %")
        
    
requete4()
def create_pie_chart_with_pyodbc():
    # Fetch data
    SQLCommand= ("""SELECT TP.logt_room_type As TypeDeLogement, 
       ROUND((count(TP.log_room_idtype)*100)/ (SELECT COUNT(*) FROM logements), 2) AS Pourcentage
FROM logements L
INNER JOIN types_logements TP ON L.log_room_idtype = TP.log_room_idtype 
INNER JOIN nodenot_bd.agglo_paysbasque AP ON L.logt_codeINSEE = nodenot_bd.AP.code_insee
GROUP BY TP.logt_room_type
ORDER BY Pourcentage DESC;""")

    # Create pie chart
    fig, ax = plt.subplots()
    ax.pie(data['Pourcentage'], labels=data['TypeDeLogement'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Ensures pie is circular

    # Show chart
    plt.show()
    #stockage du script sql dans une variable
    SQLCommand = ("select Article.Reference, Article.QteStock from Article WHERE prixHT>5  ORDER BY Article.QteStock ASC ")
    #execution du script sql avec le curseur 
    cursor.execute(SQLCommand)
    
    for l in cursor.fetchall():
        RefArticles.append(l[0])
        qteStockArticles.append(l[1])
    
    plt.bar(RefArticles, qteStockArticles)
    plt.xlabel("Référence des articles")
    plt.ylabel("Stock articles")
    plt.title("Graphique des stocks des articles de plus de 5 euros à l'unité")
    plt.show()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
print("Voila la liste des commandes : ")
sql = "select Commande.Numero, Commande.NomClient from Commande"
cursor.execute(sql)
for row in cursor.fetchall() : 
    print(row)
filter = input("Choisissez la commande dont vous voulez connaitre le prix TTC : ")
sql = "SELECT LDC.Numero, SUM(A.CoutHT*LDC.Quantite) AS coutTotalHT FROM Article A INNER JOIN LigneDeCommande LDC ON LDC.Reference = A.Reference WHERE LDC.numero = ? GROUP BY LDC.Numero"
param = (f'{filter}%')
cursor.execute(sql, param)
for row in cursor.fetchall() : 
    print(row)