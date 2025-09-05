# Traducteur Local - README

## Présentation

`index.py` est une application graphique Python permettant de traduire du texte localement entre plusieurs langues, sans utiliser d'API externe. Elle propose une interface conviviale basée sur Tkinter, avec gestion de l'historique, retour de traduction, statistiques et fonctions de copier-coller.

## Fonctionnalités principales

- **Traduction multilingue** : Français, Anglais, Espagnol, Allemand, Italien, Portugais, Néerlandais, Russe, Japonais, Chinois, Arabe, Hindi, et auto-détection.
- **Retour de traduction** : Traduisez le texte traduit vers la langue source pour vérifier la qualité.
- **Statistiques** : Affichage du nombre de caractères pour chaque zone de texte.
- **Copier-coller** : Copiez facilement la traduction ou le retour dans le presse-papier.
- **Échange des langues** : Inversez rapidement la langue source et cible.
- **Historique** : Les 15 dernières traductions sont affichées et toutes sont sauvegardées dans `historique_traductions.txt`.
- **Restauration rapide** : Double-cliquez sur une entrée de l'historique pour restaurer la traduction.

## Utilisation

Lancez l'application avec :

```powershell
python index.py
```

### Interface

- **Zone source** : Saisissez le texte à traduire.
- **Sélection des langues** : Choisissez la langue source et cible.
- **Boutons** : Traduire, retour, effacer, copier, échanger les langues.
- **Historique** : Visualisez et restaurez les traductions précédentes.

## Fichiers

- `index.py` : Code principal de l'application.
- `historique_traductions.txt` : Historique des traductions.
- `main.py` : Variante ou ancienne version de l'application.

## Dépendances

- Python 3.x
- `tkinter` (inclus avec Python)
- `pyperclip`
- `translate`

Installez les dépendances avec :

```powershell
pip install pyperclip translate
```

## Remarques

- L'application utilise la classe `translate.Translator` pour la traduction.
- L'historique est sauvegardé en texte brut dans `historique_traductions.txt`.
- La détection automatique de la langue source est disponible.

---

Pour toute question ou problème, consultez le code source ou le fichier d'historique.
