# Plugin Nextcloud Talk

## Présentation

Nextcloud Talk est un système de messagerie utilisé sur la plateforme de partage Nextcloud.

Le plugin permet de créer des équipements pouvant communiquer (Lire, Ecrire) sur les Talks de Nextcloud.

Les Talks peuvent réaliser des Interactions et est compatible avec Ask.

## Configuration du plugin

Dans Nextcloud :

  * Créer un utilisateur ou utiliser un autre utilisateur que vous même.

  * Définir de préférence un mot de passe d'application (pour éviter les symbols " et :)

Dans Jeedom sur la page du plugin on peut :

  * Définir l'url de nextcloud

  * Définir le nom et le mot de passe de l'utilisateur qui postera sur les Talks (cet utilisateur doit être au préalable existant sur Nextcloud) et avoir accès aux Talks.

  * Définir le dossier de l'utilisateur sur Nextcloud où seront uploadées les pièces jointes (par défaut dossier Talk)

  * Définir la fréquence de rafraichissement des Talks

  * Configurer le port du démon

_Le mot de passe ne doit pas contenir de : ou de ". D'une manière générale préférez un mot de passe d'application._

## Configuration des équipements

Les équipements ont le paramètre suivant :

  * ID du Talk, cela correspond au code en fin d'url du talk.
  * Options :
    - Interactions Jeedom, permet d'envoyer les messages au moteur d'interaction Jeedom et d'avoir le retour dans le Talk

### Commandes des équipements
Les équipements ont les commandes suivantes :

* Informations :
  - Auteur : contient le nom de l'auteur du dernier message
  - Timestap : contient le timestamp du dernier message
  - Lire : pour lire le dernier message du talk

* Commandes :
    - Envoyer : pour envoyer un message sur le talk

_Le message peut contenir le code @'user name' pour notifier un utilisateur à nom composé._

## FAQ

## Changelog

[Voir la page dédiée](changelog.md).
