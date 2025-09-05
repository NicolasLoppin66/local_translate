#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from translate import Translator
import pyperclip  # Pour la fonction copier-coller


class ApplicationTraduction(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Traducteur Local - Sans API")
        self.geometry("1000x700")
        self.configure(bg="#f0f0f0")

        # Dictionnaire des langues disponibles
        self.langues = {
            "Français": "fr",
            "Anglais": "en",
            "Espagnol": "es",
            "Allemand": "de",
            "Italien": "it",
            "Portugais": "pt",
            "Néerlandais": "nl",
            "Russe": "ru",
            "Japonais": "ja",
            "Chinois": "zh",
            "Arabe": "ar",
            "Hindi": "hi",
            "Auto-détection": "auto",
        }

        self.creer_widgets()
        self.charger_historique()

    def creer_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configuration des poids pour le redimensionnement
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Titre
        titre = ttk.Label(
            main_frame, text="Traducteur Local avec Retour", font=("Arial", 16, "bold")
        )
        titre.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Sélection des langues
        langue_frame = ttk.Frame(main_frame)
        langue_frame.grid(
            row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10)
        )

        ttk.Label(langue_frame, text="Langue source:").grid(
            row=0, column=0, sticky=tk.W, padx=(0, 5)
        )
        self.langue_source_var = tk.StringVar(value="Auto-détection")
        self.combo_source = ttk.Combobox(
            langue_frame,
            textvariable=self.langue_source_var,
            values=list(self.langues.keys()),
            state="readonly",
            width=15,
        )
        self.combo_source.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))

        ttk.Label(langue_frame, text="Langue cible:").grid(
            row=0, column=2, sticky=tk.W, padx=(0, 5)
        )
        self.langue_cible_var = tk.StringVar(value="Anglais")
        self.combo_cible = ttk.Combobox(
            langue_frame,
            textvariable=self.langue_cible_var,
            values=[lang for lang in self.langues.keys() if lang != "Auto-détection"],
            state="readonly",
            width=15,
        )
        self.combo_cible.grid(row=0, column=3, sticky=tk.W, padx=(0, 20))

        # Zone de texte source
        source_frame = ttk.LabelFrame(main_frame, text="Texte à traduire", padding="5")
        source_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        source_frame.columnconfigure(0, weight=1)
        source_frame.rowconfigure(0, weight=1)

        self.text_source = scrolledtext.ScrolledText(
            source_frame, height=10, wrap=tk.WORD, font=("Arial", 11)
        )
        self.text_source.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Zone de texte traduit
        trad_frame = ttk.LabelFrame(main_frame, text="Traduction", padding="5")
        trad_frame.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        trad_frame.columnconfigure(0, weight=1)
        trad_frame.rowconfigure(0, weight=1)

        self.text_traduction = scrolledtext.ScrolledText(
            trad_frame, height=10, wrap=tk.WORD, font=("Arial", 11), state="disabled"
        )
        self.text_traduction.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Zone de texte retour de traduction
        retour_frame = ttk.LabelFrame(
            main_frame, text="Retour de traduction", padding="5"
        )
        retour_frame.grid(row=2, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        retour_frame.columnconfigure(0, weight=1)
        retour_frame.rowconfigure(0, weight=1)

        self.text_retour = scrolledtext.ScrolledText(
            retour_frame, height=10, wrap=tk.WORD, font=("Arial", 11), state="disabled"
        )
        self.text_retour.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=15)

        self.btn_traduire = ttk.Button(
            button_frame, text="Traduire →", command=self.traduire
        )
        self.btn_traduire.pack(side=tk.LEFT, padx=5)

        self.btn_retour = ttk.Button(
            button_frame, text="Traduire le retour ←", command=self.traduire_retour
        )
        self.btn_retour.pack(side=tk.LEFT, padx=5)

        self.btn_effacer = ttk.Button(
            button_frame, text="Effacer tout", command=self.effacer
        )
        self.btn_effacer.pack(side=tk.LEFT, padx=5)

        self.btn_copier = ttk.Button(
            button_frame, text="Copier traduction", command=self.copier_traduction
        )
        self.btn_copier.pack(side=tk.LEFT, padx=5)

        self.btn_copier_retour = ttk.Button(
            button_frame, text="Copier retour", command=self.copier_retour
        )
        self.btn_copier_retour.pack(side=tk.LEFT, padx=5)

        self.btn_echanger = ttk.Button(
            button_frame, text="Échanger langues", command=self.echanger_langues
        )
        self.btn_echanger.pack(side=tk.LEFT, padx=5)

        # Statistiques de traduction
        stats_frame = ttk.Frame(main_frame)
        stats_frame.grid(row=4, column=0, columnspan=3, pady=(10, 5))

        self.label_stats_source = ttk.Label(stats_frame, text="Caractères source: 0")
        self.label_stats_source.pack(side=tk.LEFT, padx=10)

        self.label_stats_trad = ttk.Label(stats_frame, text="Caractères traduction: 0")
        self.label_stats_trad.pack(side=tk.LEFT, padx=10)

        self.label_stats_retour = ttk.Label(stats_frame, text="Caractères retour: 0")
        self.label_stats_retour.pack(side=tk.LEFT, padx=10)

        # Historique
        historique_frame = ttk.LabelFrame(
            main_frame, text="Historique des traductions", padding="5"
        )
        historique_frame.grid(
            row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0)
        )
        historique_frame.columnconfigure(0, weight=1)
        historique_frame.rowconfigure(0, weight=1)

        self.historique_listbox = tk.Listbox(
            historique_frame, height=4, font=("Arial", 9)
        )
        self.historique_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Barre de défilement pour l'historique
        scrollbar = ttk.Scrollbar(
            historique_frame, orient=tk.VERTICAL, command=self.historique_listbox.yview
        )
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.historique_listbox.configure(yscrollcommand=scrollbar.set)

        # Bind events
        self.historique_listbox.bind(
            "<Double-Button-1>", self.charger_historique_selection
        )
        self.text_source.bind("<KeyRelease>", self.maj_stats_source)
        self.text_source.bind("<Control-Return>", lambda e: self.traduire())

    def maj_stats_source(self, event=None):
        texte = self.text_source.get("1.0", tk.END).strip()
        self.label_stats_source.config(text=f"Caractères source: {len(texte)}")

    def traduire(self):
        texte = self.text_source.get("1.0", tk.END).strip()
        if not texte:
            messagebox.showwarning("Attention", "Veuillez entrer du texte à traduire.")
            return

        try:
            langue_source = self.langues[self.langue_source_var.get()]
            langue_cible = self.langues[self.langue_cible_var.get()]

            # Afficher un message de progression
            self.status_bar = ttk.Label(
                self, text="Traduction en cours...", relief=tk.SUNKEN, anchor=tk.W
            )
            self.status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
            self.update()

            translator = Translator(from_lang=langue_source, to_lang=langue_cible)
            traduction = translator.translate(texte)

            # Afficher la traduction
            self.text_traduction.config(state="normal")
            self.text_traduction.delete("1.0", tk.END)
            self.text_traduction.insert("1.0", traduction)
            self.text_traduction.config(state="disabled")

            # Effacer l'ancien retour de traduction
            self.text_retour.config(state="normal")
            self.text_retour.delete("1.0", tk.END)
            self.text_retour.config(state="disabled")

            # Mettre à jour les statistiques
            self.label_stats_trad.config(
                text=f"Caractères traduction: {len(traduction)}"
            )
            self.label_stats_retour.config(text=f"Caractères retour: 0")

            # Ajouter à l'historique
            self.ajouter_historique(
                texte,
                traduction,
                self.langue_source_var.get(),
                self.langue_cible_var.get(),
            )

            # Cacher la barre de statut
            self.status_bar.grid_forget()

        except Exception as e:
            self.status_bar.grid_forget()
            messagebox.showerror("Erreur", f"Erreur lors de la traduction:\n{str(e)}")

    def traduire_retour(self):
        texte_trad = self.text_traduction.get("1.0", tk.END).strip()
        if not texte_trad:
            messagebox.showwarning("Attention", "Aucune traduction à retraduire.")
            return

        try:
            # Pour le retour, on inverse source et cible
            langue_cible_actuelle = self.langues[self.langue_cible_var.get()]
            langue_source_actuelle = self.langues[self.langue_source_var.get()]

            # Si la source était auto, on utilise la cible actuelle comme source pour le retour
            if langue_source_actuelle == "auto":
                langue_source_retour = langue_cible_actuelle
                langue_cible_retour = self.langues[
                    "Français"
                ]  # Par défaut vers français
            else:
                langue_source_retour = langue_cible_actuelle
                langue_cible_retour = langue_source_actuelle

            self.status_bar = ttk.Label(
                self,
                text="Traduction retour en cours...",
                relief=tk.SUNKEN,
                anchor=tk.W,
            )
            self.status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
            self.update()

            translator = Translator(
                from_lang=langue_source_retour, to_lang=langue_cible_retour
            )
            traduction_retour = translator.translate(texte_trad)

            # Afficher le retour de traduction
            self.text_retour.config(state="normal")
            self.text_retour.delete("1.0", tk.END)
            self.text_retour.insert("1.0", traduction_retour)
            self.text_retour.config(state="disabled")

            # Mettre à jour les statistiques
            self.label_stats_retour.config(
                text=f"Caractères retour: {len(traduction_retour)}"
            )

            # Ajouter au commentaire quelle langue a été utilisée pour le retour
            nom_langue_retour = [
                k for k, v in self.langues.items() if v == langue_cible_retour
            ][0]
            self.text_retour.config(state="normal")
            self.text_retour.insert("1.0", f"(Retour en {nom_langue_retour})\n\n")
            self.text_retour.config(state="disabled")

            self.status_bar.grid_forget()

        except Exception as e:
            self.status_bar.grid_forget()
            messagebox.showerror(
                "Erreur", f"Erreur lors de la traduction retour:\n{str(e)}"
            )

    def effacer(self):
        self.text_source.delete("1.0", tk.END)
        self.text_traduction.config(state="normal")
        self.text_traduction.delete("1.0", tk.END)
        self.text_traduction.config(state="disabled")
        self.text_retour.config(state="normal")
        self.text_retour.delete("1.0", tk.END)
        self.text_retour.config(state="disabled")

        # Réinitialiser les statistiques
        self.label_stats_source.config(text="Caractères source: 0")
        self.label_stats_trad.config(text="Caractères traduction: 0")
        self.label_stats_retour.config(text="Caractères retour: 0")

    def copier_traduction(self):
        traduction = self.text_traduction.get("1.0", tk.END).strip()
        if traduction:
            try:
                pyperclip.copy(traduction)
                messagebox.showinfo(
                    "Succès", "Traduction copiée dans le presse-papier!"
                )
            except:
                messagebox.showerror(
                    "Erreur", "Impossible de copier dans le presse-papier"
                )
        else:
            messagebox.showwarning("Attention", "Aucune traduction à copier.")

    def copier_retour(self):
        retour = self.text_retour.get("1.0", tk.END).strip()
        if retour:
            try:
                pyperclip.copy(retour)
                messagebox.showinfo(
                    "Succès", "Retour de traduction copié dans le presse-papier!"
                )
            except:
                messagebox.showerror(
                    "Erreur", "Impossible de copier dans le presse-papier"
                )
        else:
            messagebox.showwarning("Attention", "Aucun retour de traduction à copier.")

    def echanger_langues(self):
        source = self.langue_source_var.get()
        cible = self.langue_cible_var.get()

        # Échanger les valeurs
        self.langue_source_var.set(cible)
        self.langue_cible_var.set(source)

        # Échanger les textes si les zones contiennent du texte
        texte_source = self.text_source.get("1.0", tk.END).strip()
        texte_trad = self.text_traduction.get("1.0", tk.END).strip()

        if texte_source and texte_trad:
            self.text_source.delete("1.0", tk.END)
            self.text_source.insert("1.0", texte_trad)

            self.text_traduction.config(state="normal")
            self.text_traduction.delete("1.0", tk.END)
            self.text_traduction.insert("1.0", texte_source)
            self.text_traduction.config(state="disabled")

            # Effacer le retour lors de l'échange
            self.text_retour.config(state="normal")
            self.text_retour.delete("1.0", tk.END)
            self.text_retour.config(state="disabled")

            # Mettre à jour les statistiques
            self.maj_stats_source()
            self.label_stats_trad.config(
                text=f"Caractères traduction: {len(texte_source)}"
            )
            self.label_stats_retour.config(text=f"Caractères retour: 0")

    def ajouter_historique(self, original, traduction, source, cible):
        # Format: "Source → Cible: Original -> Traduction"
        entree = f"{source} → {cible}: {original[:30]}... -> {traduction[:30]}..."
        self.historique_listbox.insert(0, entree)

        # Garder seulement les 15 dernières entrées
        if self.historique_listbox.size() > 15:
            self.historique_listbox.delete(15, tk.END)

        # Sauvegarder l'historique complet
        with open("historique_traductions.txt", "a", encoding="utf-8") as f:
            f.write(f"{source}|{cible}|{original}|{traduction}\n")

    def charger_historique(self):
        try:
            with open("historique_traductions.txt", "r", encoding="utf-8") as f:
                lignes = f.readlines()[-15:]  # Dernières 15 entrées
                for ligne in reversed(lignes):
                    parts = ligne.strip().split("|", 3)
                    if len(parts) == 4:
                        source, cible, original, traduction = parts
                        entree = f"{source} → {cible}: {original[:30]}... -> {traduction[:30]}..."
                        self.historique_listbox.insert(0, entree)
        except FileNotFoundError:
            pass

    def charger_historique_selection(self, event):
        selection = self.historique_listbox.curselection()
        if selection:
            index = selection[0]
            try:
                with open("historique_traductions.txt", "r", encoding="utf-8") as f:
                    lignes = f.readlines()
                    if index < len(lignes):
                        ligne = lignes[-(index + 1)]  # Inverser l'index
                        parts = ligne.strip().split("|", 3)
                        if len(parts) == 4:
                            source, cible, original, traduction = parts

                            # Charger les langues
                            for nom, code in self.langues.items():
                                if code == source or nom == source:
                                    self.langue_source_var.set(nom)
                                if code == cible or nom == cible:
                                    self.langue_cible_var.set(nom)

                            # Charger les textes
                            self.text_source.delete("1.0", tk.END)
                            self.text_source.insert("1.0", original)

                            self.text_traduction.config(state="normal")
                            self.text_traduction.delete("1.0", tk.END)
                            self.text_traduction.insert("1.0", traduction)
                            self.text_traduction.config(state="disabled")

                            # Effacer le retour
                            self.text_retour.config(state="normal")
                            self.text_retour.delete("1.0", tk.END)
                            self.text_retour.config(state="disabled")

                            # Mettre à jour les statistiques
                            self.maj_stats_source()
                            self.label_stats_trad.config(
                                text=f"Caractères traduction: {len(traduction)}"
                            )
                            self.label_stats_retour.config(text=f"Caractères retour: 0")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement: {str(e)}")


if __name__ == "__main__":
    app = ApplicationTraduction()
    app.mainloop()
