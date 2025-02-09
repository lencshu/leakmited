
## Stratégie

- SvelteKit Frontend

  - AWS pour le déploiement, prévoir d’utiliser S3 + CloudFront au lieu du SSR afin de simplifier le déploiement
  - RESTful API pour la communication avec le backend

- fastapi (python) pour le backend

  - AWS pour le déploiement
  - Déployer ce framework sur AWS Lambda afin de mieux équilibrer coût et performance.
  - Fournir une API de requête de données géographiques (avec filtres, pagination, etc.).
  - Fournir une API de statistiques (longueur des routes, distribution des vitesses).
  - Interagir avec PostGIS pour récupérer ou agréger des données géographiques.

- Postgres pour la base de données
  - Amazon RDS for PostgreSQL avec PostGIS
  - Utiliser une bounding box pour renvoyer dynamiquement les données en fonction de la zone visible.

## Chiffrage

1. Données et base de données : Parsing du fichier .pbf et importation dans PostGIS – 1 jour, un ticket avec une estimation à 5.
2. Back-end API : Fournir des fonctionnalités de requête, filtrage et statistiques sur les segments de route – 1 jour, Un ticket de 5
3. Front-end SvelteKit : Visualisation cartographique, filtres interactifs, tooltips, tableau de bord – 2 jours, Un ticket de 8
4. CI/CD AWS avec github actions – 1 jour, un ticket de 3
5. Documentation et tests – 0.5 jour, un ticket de 2
6. Présentation générale du projet