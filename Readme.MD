# ⚡ Quiz Master Pro v3

## 🆕 Nouveautés v3

### ♾️ CSV illimités
- **Aucune limite de lignes** — ajoutez 500, 1000 ou 5000 entrées dans vos CSV
- **Lecture robuste** : virgules dans le contenu, guillemets, encodage mixte → tout est géré
- **Cache 60s** : les nouvelles lignes apparaissent sans redémarrer l'app
- **Colonnes auto-détectées** : un message d'erreur clair si une colonne est manquante

### 🔗 Multijoueur partageable
- **Lien direct** : `https://votre-app.streamlit.app/?room=ABCDEF` → auto-connexion
- **Code de salle** : 6 caractères alphanumériques, partageable par SMS/WhatsApp
- **Chaque joueur sur son propre appareil** : téléphone, tablette ou ordinateur
- **Chaque joueur à son propre rythme** : son timer est indépendant
- **Classement en temps réel** dans la sidebar
- **Résultats finaux** une fois que tout le monde a terminé

---

## 📁 Structure

```
quiz_master_pro/
├── app.py
├── requirements.txt
├── README.md
├── data/                          ← vos CSV ici
│   ├── securite_financiere.csv
│   ├── apprentissage_francais.csv
│   ├── anglais.csv
│   ├── espagnol.csv
│   ├── creole_haitien.csv
│   ├── monuments_monde.csv
│   ├── musique_monde.csv
│   ├── mathematiques.csv
│   ├── histoire.csv
│   └── culture_generale.csv
└── rooms/                         ← créé automatiquement (salles multijoueur)
```

---

## 🚀 Déploiement Streamlit Cloud (recommandé)

### Étape 1 — GitHub
1. Créer un compte [github.com](https://github.com)
2. Nouveau repo → nommer par ex. `quiz-master-pro`
3. Uploader **tous** les fichiers en respectant la structure ci-dessus
   - `app.py` à la racine
   - tous les `.csv` dans le dossier `data/`

### Étape 2 — Streamlit Cloud
1. Aller sur [share.streamlit.io](https://share.streamlit.io)
2. **Sign in with GitHub**
3. **New app** → sélectionner votre repo → branche `main`
4. **Main file path** : `app.py`
5. Cliquer **Deploy** → l'app est en ligne en ~2 minutes

### Étape 3 — Partager
- Votre URL ressemblera à : `https://votre-nom-quiz-master-pro-abcd.streamlit.app`
- Pour inviter quelqu'un dans une salle multijoueur : `https://votre-url/?room=ABCDEF`

---

## 🎮 Modes de jeu

| Mode | Explication |
|------|-------------|
| **🎯 Solo** | Jouez seul, à votre rythme, avec timer et révision finale |
| **🏠 Créer une salle** | Créez une salle, obtenez un code, partagez-le |
| **🔗 Rejoindre** | Entrez le code reçu pour rejoindre une salle |

---

## 📋 Format des CSV

Vous pouvez ajouter autant de lignes que vous voulez. Le seul impératif : **respecter les noms de colonnes**.

### Vocabulaire (francais, anglais, espagnol, créole, monuments…)
```csv
Mot_Expression,Definition_Synonyme
Ephémère,"Qui ne dure qu'un temps très court, passager."
Altruiste,Qui se préoccupe du bien-être d'autrui.
```

### Musique
```csv
Artiste,Chanson,Pays_Origine,Genre
Coupé Cloué,Haïti Chérie,Haïti,Mizik Rasin
```

### Histoire / Culture Générale (QCM)
```csv
Question,Reponse_Correcte,Choix_2,Choix_3,Choix_4,Categorie,Difficulte
En quelle année...,1804,1800,1798,1810,Histoire d'Haïti,debutant
```
> Les niveaux valides : `debutant` | `potentiel` | `legende` | `superstar`

### Mathématiques
```csv
Question,Reponse,Niveau,Explication
Si x + 5 = 12 alors x = ?,7,potentiel,x = 12 - 5 = 7
```

---

## ⏱ Niveaux de difficulté

| Niveau | Timer | Questions | Pts/bonne réponse |
|--------|-------|-----------|-------------------|
| 🌱 Débutant | 30s | 10 | ×1 |
| ⚡ Potentiel | 20s | 15 | ×2 |
| 🔥 Légende | 15s | 20 | ×3 |
| 👑 Superstar | 10s | 25 | ×5 |

---

## 🔄 Comment ajouter des données

1. Ouvrir le fichier CSV correspondant dans Excel ou Google Sheets
2. Ajouter vos lignes en respectant les colonnes
3. Sauvegarder en `.csv` (encodage UTF-8)
4. Re-uploader sur GitHub (remplacer le fichier existant)
5. Streamlit Cloud redéploie automatiquement en ~1 minute
