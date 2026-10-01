NOVAFLUX — Dashboard Streamlit
================================

Fichiers du projet
------------------
- app.py            : application Streamlit complète
- dataset.csv       : données de gestion de fabrication fournies
- requirements.txt  : bibliothèques Python nécessaires
- logo.svg          : logo original de NOVAFLUX
- icon_dashboard.svg
- icon_analyse.svg
- icon_performance.svg
- icon_data.svg     : icônes SVG originales utilisées dans le projet
- README.txt        : guide de lancement

Lancement
---------
1. Ouvrir un terminal dans ce dossier.
2. Installer les dépendances :
   pip install -r requirements.txt
3. Lancer :
   streamlit run app.py

Connexion de démonstration
--------------------------
Identifiant : admin
Mot de passe : Nova@2026

Deuxième compte :
Identifiant : manager
Mot de passe : Manager@2026

Important : modifier les identifiants avant une utilisation réelle.

Fonctionnalités
---------------
- Connexion avec identifiant et mot de passe
- Dashboard principal
- KPI : production, prévision, taux de réalisation, taux de défaut, ordres
- Filtres interactifs : machine, ligne, produit, statut, période
- Graphiques Matplotlib et Seaborn
- Analyse par machine et produit
- Saisie de nouvelles données
- Mise à jour automatique du CSV, des KPI et des graphiques
- Contrôle/nettoyage des données
- Export CSV
- Interface française moderne
- Logo et icônes SVG sans dépendance à un dossier "icons"

Structure
---------
Le ZIP est volontairement PLAT : aucun dossier n'est créé à l'intérieur.
Tous les fichiers sont au même niveau.
