[TOC]

# Exigences du projet.

[CDC](./_doc/req.md)

# Planning

[Planning](./_doc/planning.md)

# Implémentation technique spécifique.

## Livrable du projet

L’ensemble du projet, frontend et backend, est entièrement configuré avec une CI/CD en utilisant github actions, le backend utilise également le Serverless Framework pour faciliter la surveillance, la gestion et le déploiement. Toutes les modifications sont automatiquement testées et déployées sur AWS.

- **Mono repo** : Les projets frontend et backend sont respectivement situés dans les dossiers frontend et backend. Le frontend déclenche le pipeline CI/CD et les opérations de déploiement via la branche `fprod`. Le backend est déployé lorsqu’un push est effectué sur la branche `bprod`.

- **Frontend** : Il est déployé sous forme de pages statiques sur S3, avec CloudFront configuré pour permettre l’accès externe. voici le lien: [https://d35uth7kuvvexq.cloudfront.net](https://d35uth7kuvvexq.cloudfront.net/)

- **Backend** : Tout le projet est déployé en utilisant Lambda Function URLs, ce qui permet d’obtenir directement une URL publique. De plus, une documentation interactive est automatiquement générée pour decrire l’API RESTful. voici le lien [https://banct6txmmohof735llh5quy6m0pzdua.lambda-url.eu-west-3.on.aws/docs](https://banct6txmmohof735llh5quy6m0pzdua.lambda-url.eu-west-3.on.aws/docs)

- **DB** : Si la base de données utilise AWS RDS for PostgreSQL, elle engendrera des coûts quotidiens. Par conséquent, en guise de compromis, elle a été déployée sur mon propre serveur, où la vitesse de test est acceptable.

- **CI/CD** et **unit test** : Les configurations GitHub Actions et Serverless sont prêtes à l’emploi et peuvent être facilement migrées vers un autre environnement de développement. Dans le pipeline CI/CD, le frontend utilise le **prebuild** hook pour imposer les tests unitaires. le backend dispose d’une étape dédiée pour exécuter les tests avec pytest, afin de réduire les bugs dans le code en production.

## backend

### quick start

Comme le backeend est entièrement déployé sur AWS sous forme de Lambda Function URLs, il n’est pas nécessaire d’utiliser Docker pour l’emballer en image.
Donc, si l’on veut exécuter le projet en local, il faudra configurer manuellement l’environnement d’exécution.

```bash
# un env virtuel est recommandé
# Il est recommandé aussi d’utiliser Python 3.9 afin de rester cohérent avec l’env cloud
virtualenv .venv
source .venv/bin/activate

# Installer les dépendances de l’env
cd backend
pip install -r requirements.txt
```

Placer le fichier de configuration de la base de données `.env.dev` dans le dossier backend.
Le format du fichier est le suivant :

```env
DB_USER=***
DB_PASS=***
DB_HOST=***
DB_PORT=***
DB_NAME=***
```

Commencez par exécuter pytest pour vérifier si la configuration est correcte :

```sh
pytest -vv -W ignore::DeprecationWarning -m sls
```

Ensuite, dans le dossier backend, exécutez la commande suivante pour lancer le backend FastAPI :

```sh
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Technologies

#### Technologies principales

- **FastAPI** : Cadre Python permettant de définir des endpoints RESTFul.
- **SQLAlchemy** + **PostgreSQL** : Gestion de la base de données relationnelle et du stockage géographique.
- **HStore** et **PostGIS**：Les données de routes sont importées automatiquement via **osm2pgsql** et stockées dans une table contenant des champs géométriques (LINESTRING) et un champ HSTORE pour divers attributs (maxspeed, etc.). Pour optimiser davantage, il est possible d’utiliser un fichier de style personnalisé afin d’extraire la limite de vitesse maximale en tant que colonne distincte.
- **Mangum** : Utilisé pour déployer FastAPI sur AWS Lambda (serverless). Cela permet également de garder l’exécution locale fonctionnelle, facilitant ainsi le débogage et le développement en temps réel.
- **GZip** : Les réponses du backend sont compressées pour alléger le volume de données transférées.

- **cache** : Utiliser des variables globales comme cache afin d’optimiser la vitesse des requêtes. D’après les tests, cela permet au moins de doubler la vitesse d’exécution.

#### Endpoints majeurs

- **/roads** : Permet d’obtenir la liste des routes avec une vitesse max éventuelle (?max_speed=50, etc.). Retourne généralement un format GeoJSON ou un tableau d’objets.
- **/roads-statistics** : Retourne une répartition de la longueur totale pour différents paliers de vitesse (30, 50, 70, 90 km/h).
- **/stats** : Renvoie un objet global contenant la longueur totale du réseau et, au besoin, d’autres informations telles que la distribution des routes.

#### CI/CD

voici le lien serverless : [https://app.serverless.com/demov/apps](https://app.serverless.com/demov/apps)
voici le lien github actions front : [https://github.com/lencshu/leakmited/actions/workflows/front_prod.yml](https://github.com/lencshu/leakmited/actions/workflows/front_prod.yml)
voici le lien github actions back : [https://github.com/lencshu/leakmited/actions/workflows/back_prod.yml](https://github.com/lencshu/leakmited/actions/workflows/back_prod.yml)

## frontend

### quick start

Le frontend utilise pnpm pour la gestion des packages

```sh
npm install -g pnpm
```

Initialisation et exécution du projet

```sh
cd frontend
pnpm install
# Par défaut, le projet utilisera l’adresse API du backend définie dans .env.dev
pnpm run dev
# pour utiliser l’API backend locale, exécute la commande suivante dans le dossier frontend
pnpm run dev:local

# test unitaire
pnpm run test
```

### Technologies principales

- **SvelteKit** : Utilisation du framework conformément aux exigences.
- **Leaflet** : Librairie JavaScript pour l’affichage cartographique.
- **Chart.js** : Outil de visualisation pour créer des diagrammes
- **Vitest** : Outil de test unitaire pour valider la logique frontend.
- **Tailwind CSS** : Framework CSS pour la mise en page rapide.
- **Cache local** : Éviter de redemander au backend les mêmes vitesses déjà chargées (cache en mémoire).
- **Lazy loading** : Sur Leaflet, limiter l’affichage aux routes de la zone visible, ou réaliser un clustering / simplification si la quantité de données est très élevée.

### Composants clés

1. **MapRoads** :

- Affiche la carte Leaflet, récupère la liste des routes depuis un store global, applique un style selon la vitesse, propose des popups avec la vitesse max, etc.

2. **SpeedFilter** :

- Permet de sélectionner/désélectionner des vitesses (30, 50, 70, 90 km/h). Chaque changement met à jour un store Svelte (selectedSpeeds) et récupère ou supprime les routes correspondantes du store (roadsData).

3. **SpeedPieChart** :

- Affiche un diagramme montrant la répartition des routes par vitesse. Lit directement la liste de routes dans le store.

4. **Dashboard Stats** :

- Permet de présenter la longueur totale du réseau, ainsi que la répartition par vitesse.

## conclusion

### Points forts du projet

- **Modernité et scalabilité** : L’architecture serverless du backend permet une mise à l’échelle automatique et un coût maîtrisé.
- **Qualité et fiabilité** : Une solide stratégie de tests et une pipeline CI/CD garantissent la robustesse et la maintenabilité du système.
- **Adaptation aux exigences métiers**, La conception répond aux exigences fonctionnelles:
  - [x] Map display: Display all & filter by speed
  - [x] Interactive map: roads selectable & tooltip
  - [x] Dashboard: separate dashboard page & Distribution & Total length of the road network
  - [x] Documentation: how to install and run your project
  - [x] AWS Deployment: deploy on AWS
  - [x] Unit tests
  - [x] User experience and interface design
  - [x] Additional features:
    - [x] Le développement du backend a suivi une approche TDD (Test-Driven Development), en commençant par des tests unitaires pour chaque module, puis en procédant à des itérations rapides
    - [x] Lazy loading de la carte côté frontend
    - [x] Cache mémoire pour le frontend et le backend
    - [x] Optimisation des coûts à l’extrême, avec quasiment aucune dépense
    - [x] Configuration CI/CD complète pour le frontend et le backend, prête à l’emploi
    - [x] Les adresses HTTPS accessibles pour le frontend et le backend à distance
    - [x] Le frontend et le backend peuvent être facilement exécutés et débogués en local, même avec le déploiement backend basé sur AWS Lambda.
    - [x] Le backend peut renvoyer plus de données afin que le frontend puisse afficher des informations supplémentaires lors du clic sur une route, comme le type de route ou l’ID dans la base de données. Cependant, pour réduire la taille des réponses API, ces champs ont été temporairement commentés.
    - [x] Le backend a un variable globale pour limiter la taille des données renvoyées, actuellement fixée à 100 000 entrées. Étant donné le volume important des données, cette limite permet de maintenir une lisibilité acceptable sur la carte. Elle peut être ajustée en fonction des besoins.
    - [x] Gzip compression pour réduire la taille des données transmises entre le backend et le frontend.
    - [x] Les informations sensibles sont transmises au projet via GitHub Secrets lors de l’exécution du CI/CD et sont configurées comme variables d’environnement pour la fonction Lambda
    - [x] Le développement suit une approche frontend / backend séparée, avec l’utilisation de données mockées côté frontend pour accélérer le développement
    - [x] Réutiliser le code autant que possible, par exemple avec la fonction getColorBySpeedNum du frontend

### Trade-offs

(La première semaine a été plus chargée que prévu, le développement n’a pris qu’une semaine)

- Comme je n’étais pas familier avec Svelte au départ, le développement du frontend n’a pas suivi une approche TDD.
- Bien que le frontend utilise déjà le lazy loading, la quantité de données étant trop importante, le chargement de toutes les routes simultanément entraîne un certain ralentissement de la page. À optimiser. il est envisageable d’utiliser une **bounding box** afin que le frontend ne charge et ne traite que les données situées dans la zone visible de la carte
- Pour des raisons de coût, la base de données n’utilise pas le service AWS RDS. Étant hébergée sur mon propre serveur, il y a un compromis sur la vitesse des requêtes, mais les performances restent suffisantes pour une utilisation courante.
- La gestion des erreurs pourrait être plus complète.
- Le frontend pourrait utiliser des `interfaces` pour appliquer une vérification stricte des modèles de données. Actuellement, seules les données statistiques ont une `interface` définie.
- Avec plus de temps, l’affichage sur mobile pourrait être optimisé pour rendre l’interface plus responsive. Cependant, comme Tailwind CSS est utilisé, le développement sera relativement rapide
- Étant donné qu’il est complexe de manipuler directement le DOM pour les tests dans SvelteKit, cela prendrait du temps. C’est pourquoi les tests d’intégration frontend/backend n’ont pas été réalisés.
- Lambda a un temps de cold start, qui peut être réduit en utilisant des instances provisionnées (Provisioned Concurrency) pour accélérer le premier accès. En cas de forte affluence attendue, il est aussi possible de préchauffer la fonction en la réveillant à l’avance via un appel programmé.