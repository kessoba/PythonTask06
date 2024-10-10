import PySimpleGUIQt as sg
import math

def affiche_erreur(resultat, texte):
    """Affiche le texte d'erreur dans le champ de résultat."""
    resultat.update(texte)

def somme(valeur0, valeur1):
    return float(valeur0) + float(valeur1)

def soustraction(valeur0, valeur1):
    return float(valeur0) - float(valeur1)

def multiplication(valeur0, valeur1):
    return float(valeur0) * float(valeur1)

def division(valeur0, valeur1, resultat):
    try:
        if float(valeur1) == 0:
            raise ZeroDivisionError
        return float(valeur0) / float(valeur1)
    except ZeroDivisionError:
        affiche_erreur(resultat, "Erreur : Division par zéro")
        return "Erreur division par zero impossible"

def racine_carree(valeur1, resultat):
    try:
        if float(valeur1) < 0:
            raise ValueError
        return math.sqrt(float(valeur1))
    except ValueError :
        affiche_erreur(resultat, "Erreur : Valeur négative")
        return "Erreur"

def puissance(valeur0, valeur1):
    return float(valeur0) ** float(valeur1)

def pourcent(valeur1):
    return float(valeur1) / 100

def cosinus(valeur1):
    return math.cos(math.radians(float(valeur1)))

def sinus(valeur1):
    return math.sin(math.radians(float(valeur1)))

def gere_operation_unaire(op, valeur1, resultat):
    """Redirige vers pourcent, racine_carree, cosinus ou sinus."""
    if op == "%":
        return pourcent(valeur1)
    elif op == "√":
        return racine_carree(valeur1, resultat)
    elif op == "cos":
        return cosinus(valeur1)
    elif op == "sin":
        return sinus(valeur1)
    else:
        return valeur1

def gere_operation_binaire(op, valeur0, valeur1, resultat):
    """Gère les opérations mathématiques avec 2 arguments."""
    if op == "+":
        return somme(valeur0, valeur1)
    elif op == "-":
        return soustraction(valeur0, valeur1)
    elif op == "*":
        return multiplication(valeur0, valeur1)
    elif op == "/":
        return division(valeur0, valeur1, resultat)
    elif op == "^":
        return puissance(valeur0, valeur1)
    else:
        return valeur1

def ajoute_a_la_valeur(ajout, valeur1):
    """Ajoute la valeur ajoutée à valeur1."""
    if valeur1 == "0" or valeur1 == "Erreur":
        valeur1 = ajout
    else:
        valeur1 += ajout
    return valeur1

def supprime_dernier_caractere(valeur1):
    """Supprime le dernier caractère dans la valeur1."""
    if len(valeur1) > 1:
        return valeur1[:-1]
    else:
        return "0"

def ajoute_virgule(valeur1):
    """Ajoute une virgule, s'il n'y en a pas déjà."""
    if valeur1.find(".") == -1:
        return valeur1 + "."
    else:
        return valeur1

def enregistre_operation(op, valeur1):
    """Mémorise l'opération en vue d'un futur clic sur le bouton '='."""
    return valeur1, "0", op

def reinitialise():
    """Réinitialise l'ancienne valeur0, la valeur1 courante, et l'opération."""
    return "", "0", ""

def gere_evenement(evenement, valeur0, valeur1, op, resultat):
    """Gestionnaire principal d'événements."""
    if valeur1 == "Erreur":
        valeur1 = "0"  # Réinitialiser si une erreur est présente

    if evenement in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}:
        valeur1 = ajoute_a_la_valeur(evenement, valeur1)
    elif evenement == ".":
        valeur1 = ajoute_virgule(valeur1)
    elif evenement == "«":
        valeur1 = supprime_dernier_caractere(valeur1)
    elif evenement == "C":
        valeur0, valeur1, op = reinitialise()
    elif evenement in {"+", "-", "*", "/", "^"}:
        valeur0, valeur1, op = enregistre_operation(evenement, valeur1)
    elif evenement in {"%", "cos", "sin", "√"}:
        valeur1 = gere_operation_unaire(evenement, valeur1, resultat)
    elif evenement == "=":
        valeur1 = gere_operation_binaire(op, valeur0, valeur1, resultat)
    
    resultat.update(valeur1)

    return valeur0, valeur1, op

def gui():
    """Gestion de l'interface utilisateur graphique."""
    disposition = [
        [sg.Input("0", key="resultat", justification="right")],
        [sg.Button("7"), sg.Button("8"), sg.Button("9"), sg.Button("/"), sg.Button("«"), sg.Button("C")],
        [sg.Button("4"), sg.Button("5"), sg.Button("6"), sg.Button("*"), sg.Button("^"), sg.Button("√")],
        [sg.Button("1"), sg.Button("2"), sg.Button("3"), sg.Button("-"), sg.Button("cos"), sg.Button("sin")],
        [sg.Button("0"), sg.Button("."), sg.Button("%"), sg.Button("+"), sg.Button("=")],
    ]

    fenetre = sg.FlexForm("Calculatrice",
                          default_button_element_size=(5, 1),
                          auto_size_buttons=False)
    fenetre.Layout(disposition)

    op = ""
    valeur0 = ""
    valeur1 = "0"
    resultat = fenetre.FindElement('resultat')

    while True:
        evenement, _ = fenetre.read()
        if evenement == sg.WIN_CLOSED:
            break

        try:
            valeur0, valeur1, op = gere_evenement(evenement, 
                                                  valeur0,
                                                  valeur1,
                                                  op,
                                                  resultat)
        except Exception as e:
            affiche_erreur(resultat, f"Erreur : {str(e)}")

    fenetre.close()

if __name__ == "__main__":
    gui()
