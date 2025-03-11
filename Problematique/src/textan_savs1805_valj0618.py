#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Ce fichier contient la classe TextAn, à utiliser pour résoudre la problématique.
    C'est un gabarit pour l'application de traitement des fréquences de mots dans les oeuvres d'auteurs divers.

    Les méthodes apparaissant dans ce fichier définissent une API qui est utilisée par l'application
    de test test_textan.py
    Les paramètres d'entrée et de sortie (Application Programming Interface, API) sont définis,
    mais le code est à écrire au complet.
    Vous pouvez ajouter toutes les méthodes et toutes les variables nécessaires au bon fonctionnement du système

    La classe TextAn est invoquée par la classe TestTextAn (contenue dans test_textan.py) :

        - Tous les arguments requis sont présents et accessibles dans args (dans le fichier test_textan.py)
        - Les arguments proviennent :
            - soit du fichier de configuration test_textan_config.yml,
            - soit de la ligne de commande
        - Note : vous pouvez tester votre code en utilisant les commandes :
            + "python test_textan.py"
            + "python test_textan.py -h" (donne la liste des arguments possibles)
            + "python test_textan.py -v" (mode "verbose", qui indique les valeurs de tous les arguments)
        - Note (2) : vous pouvez modifier le fichier test_textan_config.yml :
            - Vous le trouverez dans le répertoire de travail (Problematique/data)
            - Les mêmes options existent dans le fichier test_textan_config.yml et en ligne de commande
            - Les paramètres passés en ligne de commande ont priorité sur ceux définis dans le fichier de configuration

    Copyright 2018-2025, F. Mailhot et Université de Sherbrooke
"""

import io
import math
import random
from textan_common import TextAnCommon

class TextAn(TextAnCommon):
    """Classe à utiliser pour coder la solution à la problématique :

        - La classe héritée TextAnCommon contient certaines fonctions de base pour faciliter le travail :
            - recherche des auteurs
            - ouverture des répertoires
            - obtention de la liste des oeuvres d'un auteur (get_aut_files(auteur))
            - et autres (voir la classe TextAnCommon pour plus d'information)
        - Les interfaces du code à développer sont présentes, mais tout le code est à écrire
        - En particulier, il faut compléter les fonctions suivantes :
            - add_dict(dict1, dict2)
            - analyze()
            - dot_product_dict (dict1, dict2)
            - find_author (oeuvre)
            - gen_text_dict(auteur_dict, taille, to_file)
            - get_kth_element (auteur, k)
            - get_ngram_occurrence (auteur, ngram)
            - get_total_occurrences (auteur)
            - get_vector_size(dict)
            - normalize_vector(dict)


    Copyright 2018-2025, F. Mailhot et Université de Sherbrooke
    """

    # Signes de ponctuation à traiter comme des mots
    PONC = ["!", ",", ".", ";", ":", "(", ")", "[", "]", "-", "*", "_", "—" "‘", "’", "«", "»", "<",">", "'", "/", "#", "|", "&", "?"]

    # Ajouter les structures de données et les fonctions nécessaires à l'analyse des textes,
    # la production de textes aléatoires, la détection d'oeuvres inconnues,
    # l'identification des k-ièmes mots les plus fréquents.
    #
    # Les méthodes qui suivent doivent toutes être complétées pour que le système soit opérationnel
    # et que le harnais de test (test_textan.py) puisse exécuter tous les tests requis.
    #
    #  Note : Voir
    #

    @staticmethod
    def get_vector_size(dict_de_ngrams: dict) -> float:
        """Calcule la longueur (norme) du vecteur (dictionnaire) de ngrams contenus dans un dictionnaire

        Args :
            dict_de_ngrams (dict) : le vecteur de ngrams (dict) en question

        Returns :
            taille (float) : La norme du vecteur (dict) est retournée

        Copyright 2024-2025, F. Mailhot et Université de Sherbrooke
        """

        # Variables
        norme = 0.0

        # Passer dans chaque valeur du dictionnaire et additioner leurs carres
        for valeurs in dict_de_ngrams.values():
            norme += valeurs ** 2

        # Racine de la somme au carre pour avoir la norme
        norme = math.sqrt(norme)

        # Retourner la norme
        return norme

    def normalize_vector(self, dict_de_ngrams: dict) -> dict:
        """Normalize le vecteur (dictionnaire), en divisant chaque occurrence par la taille totale

        Args :
            dict_de_ngrams (dict) : le vecteur de n-grammes (dict) en question

        Returns :
            (dict) : Une nouvelle version normalisée du dictionnaire est retournée

        Copyright 2024-2025, F. Mailhot et Université de Sherbrooke
        """

        # Calcul de la norme du vecteur
        norme = self.get_vector_size(dict_de_ngrams)
        if norme <= 0: # CAS BIZZ (A REVOIR)
            return dict_de_ngrams

        # Normalisée le vecteur temporaire
        for cle in dict_de_ngrams.keys():
            dict_de_ngrams[cle] = dict_de_ngrams[cle] / norme

        # Retourner dict_de_ngrams normalisée
        return dict_de_ngrams

    @staticmethod
    def add_dict(dict1: dict, dict2: dict) -> dict:
        """Additionne deux vecteurs représentés par des dictionnaires
        Note : le vecteur de retour n'est PAS NORMALISÉ

        Args :
            dict1 (dict) : le premier vecteur
            dict2 (dict) : le deuxième vecteur

        Returns :
            sum_dict (dict) : La somme des deux vecteurs passés en paramètre

        Copyright 2025, F. Mailhot et Université de Sherbrooke
        """

        # Copie de dict2 dans dict1
        for cle, valeur in dict2.items():
            if cle in dict1.keys():
                dict1[cle] += valeur
            else:
                dict1[cle] = valeur

        # Retourner dict1 (contenant le somme des 2 dict)
        return dict1

    @staticmethod
    def dot_product_dict(dict1: dict, dict2: dict) -> float:
        """Calcule le produit scalaire de deux vecteurs représentés par des dictionnaires
            Note : ce produit scalaire n'est PAS normalisé

        Args :
            dict1 (dict) : le premier vecteur
            dict2 (dict) : le deuxième vecteur

        Returns :
            dot_product (float) : Le produit scalaire normalisé de deux vecteurs

        Copyright 2024-2025, F. Mailhot et Université de Sherbrooke
        """

        # Variables
        dot_product = 0.0

        # Calculer le produit scalaire
        for cle in dict1.keys():
            if cle in dict2.keys():
                dot_product += dict1[cle] * dict2[cle]

        # Retourner le produit scalaire
        return dot_product

    def find_author(self, oeuvre: str) -> []:
        """Après analyse des textes d'auteurs connus, retourner la liste d'auteurs
            et le niveau de proximité (un nombre entre 0 et 1) de l'oeuvre inconnue
            avec les écrits de chacun d'entre eux

        Args :
            oeuvre (str) : Nom du fichier contenant l'oeuvre d'un auteur inconnu

        Returns :
            resultats (Liste[(string, float)]) : Liste de tuples (auteurs, niveau de proximité),
            où la proximité est un nombre entre 0 et 1)
        """

        # Variables
        resultats = []

        # Analyze l'oeuvre et calcul sa norme
        mots_oeuvre = self.anaylyze_oeuvre(oeuvre) # Lecture de l'oeuvre et création d'une liste des mots (mots et ponctuations)
        dict_oeuvre = self.creation_ngram_dict(mots_oeuvre) # Creation d'un dict avec la liste mots_oeuvre
        norme_oeuvre = self.get_vector_size(dict_oeuvre)

        # Comparer avec tous les auteurs
        for auteurs in self.auteurs:
            dict_auteur = self.ngrams_auteurs[auteurs]
            norme_auteur = self.get_vector_size(dict_auteur)

            # Calcul de la proximité
            if norme_oeuvre > 0 and norme_auteur > 0:
                proximite = self.dot_product_dict(dict_auteur, dict_oeuvre) / (norme_auteur * norme_oeuvre)
            else:
                proximite = 0
            tuple_auteur = (auteurs, proximite)
            resultats.append(tuple_auteur)

        # Retourner le résultat (liste de tuples resultats)
        return resultats

    def get_ngram_occurrence(self, auteur: str, ngram: str) -> int:
        """Retourne le nombre d'occurrences du n-gramme pour cet auteur

        Args :
            auteur (string) : le nom de l'auteur
            ngram (objet de type ngram) : le n-gramme dont on désire la fréquence

        Returns :
            int : retourne le nombre d'occurrences du n-gramme pour l'auteur donné

        Copyright 2024-2025, F. Mailhot et Université de Sherbrooke
        """

        # Variables
        nb_ngram = 0

        # Vérifier si l'auteur existe dans la base de données
        if auteur not in self.auteurs:
            return nb_ngram

        # Récupérer le dictionnaire des n-grammes pour cet auteur
        ngrams_dict = self.ngrams_auteurs[auteur]

        # Vérifier si le n-gramme est présent dans le dictionnaire
        if ngram in ngrams_dict.keys():
            nb_ngram = ngrams_dict[ngram]

        # Retourner le nombre d'occurrences du n-gramme
        return nb_ngram

    def get_total_occurrences(self, auteur: str) -> int:
        """Retourne le nombre total d'occurrences de n-grammes pour cet auteur
            - Représente le total de n-grammes pour l'ensemble des oeuvres de cet auteur
            - Ce nombre est différent de la norme du vecteur :
                - il s'agit seulement du total d'occurrences de l'ensemble des ngrammes
                - Le calcul doit donner la somme des valeurs, et non la racine carrée de la somme des carrés des valeurs

        Args :
            auteur (string) : le nom de l'auteur

        Returns :
            int : retourne le nombre total d'occurrences pour l'auteur donné

        Copyright 2024-2025, F. Mailhot et Université de Sherbrooke
        """

        # Variables
        somme: int = 0

        # Vérifier si l'auteur passer en paramètres existe dans la liste
        if auteur not in self.auteurs:
            return somme

        # Récupérer le dictionnaire des n-grammes pour cet auteur
        ngrams_dict = self.ngrams_auteurs[auteur]

        # Calculer la somme
        for cle in ngrams_dict:
            somme += ngrams_dict[cle]

        # Retourner la sommme
        return somme

    def gen_text_dict(self, auteur_dict: dict, taille: int, to_file: io.TextIOWrapper) -> None:
        """Après analyse des textes d'auteurs connus, produire un texte selon des statistiques d'un dictionnaire.

        Args :
            auteur_dict (dict) : Dictionnaire à utiliser (soit d'un auteur, ou d'un amalgame)
            taille (int) : Taille du texte à générer
            to_file (io.TextIOWrapper) : Pointeur vers le fichier à créer.

        Returns :
            void : ne retourne rien, le texte produit doit être écrit dans le fichier fourni.
        """

        # Variables
        dict_prefix_suffix = {}

        # Remplir le dict_prefix_suffix
        for cle, valeur in auteur_dict.items():
            prefix = cle[:len(cle) - 1]
            suffix = cle[-1]
            if prefix not in dict_prefix_suffix:
                dict_prefix_suffix[prefix] = {}
            dict_prefix_suffix[prefix][suffix] = valeur

        # Choix du premier ngram
        first_n_gram = random.choices(list(auteur_dict.keys()), weights=list(auteur_dict.values()))[0]
        liste_mots = list(first_n_gram)

        # Remplir la liste de mots
        for i in range(0, taille - self.ngram_size):
            if self.ngram_size == 1:
                # Cas où on génère un mot sans n-gramme, on choisit un mot parmi ceux dans auteur_dict
                next_ngram = random.choices(list(auteur_dict.keys()), weights=list(auteur_dict.values()))[0][0]
            else:
                # Cas où on génère un mot basé sur un n-gramme
                last_prefix = tuple(liste_mots[-self.ngram_size + 1:])

                # Si le préfixe n'existe pas dans le dictionnaire, on génère un mot aléatoire pondéré
                if last_prefix not in dict_prefix_suffix:
                    next_ngram = random.choices(list(auteur_dict.keys()), weights=list(auteur_dict.values()))[0][0]
                else:
                    # Sinon, on prend le suffixe probable du préfixe
                    possible_ngram = dict_prefix_suffix[last_prefix]
                    next_ngram = random.choices(list(possible_ngram.keys()), weights=list(possible_ngram.values()))[0]

            liste_mots.append(next_ngram)

        # Transformer la liste en texte et gérer les caractère spéciaux (en cas de besoin)
        texte = " ".join(liste_mots)
        texte = texte.encode("charmap", errors="replace").decode("charmap")

        # Écrire le texte dans le fichier
        print(texte, file=to_file)

        # Retourner rien
        return

    def get_kth_element(self, auteur: str, k: int) -> list[list[str]]:
        """Retourne la liste des n-grammes à la k-ième position en fréquence pour un auteur donné.

        Args:
            auteur (str): Nom de l'auteur à utiliser.
            k (int): Indice du n-gramme à retourner.

        Returns:
            list[list[str]]: Liste de listes contenant les n-grammes ayant la k-ième fréquence.
        """

        # Variables
        dict_auteur = self.ngrams_auteurs[auteur]
        ngrams_sorted = list(dict_auteur.items())
        list_ngrams = []
        kth_counter = 1
        prev_freq = ngrams_sorted[0][1]

        # Remplir la liste de ngram de kème position de fréquence
        for ngram, freq in ngrams_sorted:
            if freq < prev_freq:
                kth_counter += 1
            if kth_counter == k:
                list_ngrams.append(ngram)
            elif kth_counter > k:
                return list_ngrams
            prev_freq = freq

        # Retourner la liste de ngram
        return list_ngrams

    def analyze(self) -> None:
        """Fait l'analyse des textes fournis, en traitant chaque oeuvre de chaque auteur

        Args :
            void : toute l'information est contenue dans l'objet TextAn

        Returns :
            void : ne retourne rien, toute l'information extraite est conservée dans des structures internes
        """

        # Analyzer tous les auteurs, tous les oeuvres
        for auteur in self.auteurs:
            oeuvres = self.get_aut_files(auteur)
            for oeuvre in oeuvres:
                # Analyze l'oeuvre
                mots_oeuvre = self.anaylyze_oeuvre(oeuvre)

                # Ajouter les n-grammes de l'oeuvre au dict de l'auteur
                self.add_dict(self.ngrams_auteurs[auteur], self.creation_ngram_dict(mots_oeuvre))

            # Trier les n-grammes pour cet auteur
            self.ngrams_auteurs[auteur] = dict(sorted(self.ngrams_auteurs[auteur].items(), key=lambda item: item[1], reverse=True))

        # Retourner rien
        return

    def __init__(self) -> None:
        """Initialize l'objet de type TextAn lorsqu'il est créé

        Args :
            (void) : Utilise simplement les informations fournies dans la classe TextAnCommon

        Returns :
            (void) : Ne fait qu'initialiser l'objet de type TextAn
        """

        # Initialisation des champs nécessaires aux fonctions fournies
        super().__init__()

        # Au besoin, ajouter votre code d'initialisation de l'objet de type TextAn lors de sa création

        return

    def anaylyze_oeuvre(self, oeuvre: str) -> []:
        """Fonction personelle -- Analyzer 1 oeuvre passer en paramètre (extraire tous les mots de l'oeuvre)"""

        # Lire le fichier oeuvre
        with open(oeuvre, "r", encoding="utf8") as fichier_oeuvre:
            lignes = fichier_oeuvre.readlines()

        # Remplir une liste de mots avec tous les oeuvres de l'auteur
        liste_mots = []
        for ligne in lignes:
            # Ajouter un espace avant et après chaque ponctuation dans la ligne
            for i in self.PONC:
                # Remplacer chaque ponctuation par elle-même entourée d'un espace
                ligne = ligne.replace(i, " " + i + " ").strip()

            # Séparer les mots de la ligne
            mots = ligne.split()
            liste_mots.extend(mots)

        # Retourner la liste de mots
        return liste_mots

    def creation_ngram_dict(self, liste_mots) -> {}:
        """Fonction personelle -- Créer un dictionnaire de ngram avec une liste de mots passer en paramètre"""

        # Variables
        ngram_dict = {}

        # Remplir le dict
        for i in range(len(liste_mots) - self.ngram_size + 1):  # Éviter les erreurs d'index
            ngram = tuple(liste_mots[i + j] for j in range(self.ngram_size))
            if ngram in ngram_dict:
                ngram_dict[ngram] += 1
            else:
                ngram_dict[ngram] = 1

        # Retourner le dict
        return ngram_dict