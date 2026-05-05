import hashlib


def calculer_hash_texte(texte):
    return hashlib.sha256(texte.encode("utf-8")).hexdigest()


def calculer_hash_fichier(chemin):
    sha256 = hashlib.sha256()

    with open(chemin, "rb") as fichier:
        while True:
            bloc = fichier.read(4096)
            if not bloc:
                break
            sha256.update(bloc)

    return sha256.hexdigest()


def sauvegarder_hash(type_donnee, source, hash_resultat):
    reponse = input("\nVoulez-vous sauvegarder le hash dans hash_output.txt ? (o/n) : ")

    if reponse.lower() == "o":
        try:
            with open("hash_output.txt", "w", encoding="utf-8") as fichier:
                fichier.write(f"{type_donnee} : {source}\n")
                fichier.write(f"SHA-256 : {hash_resultat}\n")

            print("Le hash a été sauvegardé dans hash_output.txt.")

        except Exception as erreur:
            print("Erreur lors de la sauvegarde :", erreur)


def hacher_texte():
    texte = input("Entrez le texte à hacher : ")

    if texte.strip() == "":
        print("Erreur : le texte ne peut pas être vide.")
        return

    hash_resultat = calculer_hash_texte(texte)

    print("\nSHA-256 :", hash_resultat)
    sauvegarder_hash("Texte saisi", texte, hash_resultat)


def hacher_fichier():
    chemin = input("Entrez le chemin du fichier à hacher : ")

    if chemin.strip() == "":
        print("Erreur : le chemin du fichier ne peut pas être vide.")
        return

    try:
        hash_resultat = calculer_hash_fichier(chemin)

        print("\nSHA-256 :", hash_resultat)
        sauvegarder_hash("Fichier", chemin, hash_resultat)

    except FileNotFoundError:
        print("Erreur : fichier introuvable.")
    except PermissionError:
        print("Erreur : permission refusée pour lire ce fichier.")
    except Exception as erreur:
        print("Une erreur est survenue :", erreur)


def afficher_menu():
    print("Choisissez une option :")
    print()
    print("[1] Hacher un texte")
    print("[2] Hacher un fichier")
    print()


def main():
    afficher_menu()

    choix = input("Votre choix : ")

    if choix == "1":
        hacher_texte()
    elif choix == "2":
        hacher_fichier()
    else:
        print("Erreur : choix invalide.")


if __name__ == "__main__":
    main()