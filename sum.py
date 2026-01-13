import sys
# V r i f i e r si deux arguments sont fournis
if len(sys.argv ) != 3:
    print (" Erreur : Deux arguments sont necessaires.")
    sys.exit (1)
# I n t e r p r t e r les arguments
try:
    arg1 = float (sys.argv [1])
    arg2 = float ( sys.argv [2])
except ValueError :
    print (" Erreur :Les arguments doivent etre des nombres .")
    sys.exit (1)
# Calculer la somme
resultat = arg1 + arg2
# Afficher lersultat
print(resultat)