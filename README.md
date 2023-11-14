[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/NPsCwZiZ)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-718a45dd9cf7e7f842a935f5ebbe5719a5e09af4491e668f4dbf3b35d5cca122.svg)](https://classroom.github.com/online_ide?assignment_repo_id=12365787&assignment_repo_type=AssignmentRepo)
# Projet Cloud IoT - INSA Lyon

Dans ce repertoire vous allez enregistrez les démarches que l'équipe de travail a suivi
pour mettre en place une architecture Edge/Fog IoT fonctionnel.

Dans ce fichier `README.md` vous devez décrire en format Markdown chacune des étapes et comptes rendus de chaque avancement, pensez bien à la répartition des tâches dans votre équipe et si besoin créez d'autres repertoires ou utilisez les sous-dossiers proposés.


## Équipe

Notre équipe projet est composée par :

- Vivekananda Boudia (Sensors)
- Zoé Batello (Sensors)

- Chakib Hamie (Messaging)
- Abdeladem Fattah (Messaging)
- Mohamed Bouzoubaa(Messaging)
- Adrianos Sidiras-Galante (Messaging)

- Nabil Azakkour (Reactive Streaming)
- Zihao Wan (Reactive Streaming)
- Khadija Ly(Reactive Streaming)
- Zhenglin Jiang (Reactive Streaming)

- Hiba Bellagnech (Storage)
- Salah Idbelouch (Computing)
- Safae Hariri(Computing)

- Morgan Clot (DevOps)
- Etienne Brunel (DevOps)
- Hugo Thomas (DevOps)
- Abdellah Kabbaj (DevOps)

- Armand Prioreschi (Project manager and Storage)
- Alice Gangneux (Project manager and Sensors)


## Description du Projet

Traitement d'images


### Infrastructure

Le présent projet est deployé dans la plateforme YouPi du Laboratoire CITI en utilisant les noeuds suivants :

```
Rajouter tous les noeuds utilisés
```
Pour se connecter aux noeuds, il faut passer par l'intermediaire du noeud bastion en ssh :

```
youpi.citi-lab.fr
```

Les noeuds sont à réserver sur le site web de la plateforme.


### Cas d'utilisation


## Répartition des tâches
Lors de ce projet les tâches ont été réparties comme suit :

- Equipe Sensors 
- Equipe Messaging 
- Equipe Reactive Streaming
- Equipe Storage
- Equipe Computing
- Equipe Deployment 


### Suivi journalier

**Vendredi 13/10/2023** :
- Introduction du projet Cloud-IoT
- Mise en place des équipes
- Création des comptes Youpi et premières connections aux Raspberry Pi à l'aide des clés SSH
- Création d'un serveur Discord avec des channels pour la communication
- Création d'un board Trello pour chaque équipe pour la gestion de projet

**Lundi 16/10/2023** :
- L'équipe Capteurs a réussi à récupérer des images depuis les 3 caméras fonctionnelles (sur 5). L'équipe a fait le choix du protocole MQTT.
- L'équipe Messaging a installé Californium et RabbitMQ mais opte finalement pour cette dernière solution. La séance a été principalement dédiée à la documentation.
- L'équipe Reactive Streaming a commencé à mettre en place Kafka (au détriment de Vert.X qui ne supporte pas Python) et a commencé à discuter avec les groupes en aval et en amont afin de cerner au mieux ses problématiques et ses enjeux.
- L'équipe Storage Computation s'est documenté sur la manière de mettre en place et tester ses systèmes distribués (base de données et application de traitement d'image), après discussion avec l'équipe Reactive Streaming.
- L'équipe Deployement a commencé à instancier des services avec k3s afin de déployer au mieux les services des autres équipes.
- Une présentation suivi de quelques questions, le tout pour un total de 5 minutes par équipe à été réalisé à la fin de la séance (environ 30 min au total) afin que tout le monde puisse comprendre les enjeux et les difficultés techniques de l'ensemble du projet.

**Mercredi 18/10/2023** :
- L’équipe Capteurs s’est penchée sur la transmission de messages MQTT. En collaboration avec l’équipe Messaging. Ils ont pu mettre en place un broker Rabbit MQ sur un Raspberry et lui envoyer des messages depuis un autre Raspberry (client). L’équipe a réussi à envoyer des messages simples (string), mais également des images avec une faible résolution. Elle a pour objectif maintenant de réfléchir à la manière d’envoyer des images avec une meilleure résolution (discussions sur la compression ou le découpage des images à envoyer).
 - L’équipe Messaging a donc travaillé avec l’équipe Capteurs pour établir la communication et a pour objectif pour la prochaine séance de déployer Rabbit MQ sur plusieurs nœuds.
 - L’équipe Reactive Streaming a réussi à déployer Kafka sur un seul nœud sur lequel leur code Python fonctionne bien. Il faut maintenant réussir à distribuer ces fonctionnalités sur plusieurs nœuds. L’équipe va également devoir utiliser un broker et leur choix s’est porté sur ZooKeeper.
 - L’équipe Storage voulait réussir lors de cette séance à réaliser un réplica set avec MongoDB. Malheureusement, l’équipe a eu des problèmes de configurations et n’a pas réussi à faire fonctionner MongoDB. L’idéal serait d’installer Mongo DB ave Image Docker pour faciliter le travail de l’équipe de déploiement.
 - L’équipe Computing a un code fonctionnel qui détecte bien les personnes, basé sur le module de YOLO qui est pré-entrainé. Leur prochain objectif est de faire la conversion du modèle à TensorFlow.
 - L’équipe Déploiement a set up un cluster Kubernetes avec Ansible. Les prochaines étapes sont de déployer une application dans ce cluster et de monter en compétences sur Ansible.  Ils rappellent aux autres équipes que la communication avec eux est très importante dès maintenant, notamment l’équipe Storage (support Docker).
 - Les chefs de projet ont rappelé que l’objectif était que chaque équipe ait sa partie du projet fonctionnelle à la fin de la prochaine séance qui est dans un mois (13 novembre) et qui laisse donc le temps aux équipes qui ont rencontré des difficultés d’avancer pendant les vacances notamment et/ou d’appeler à l’aide si cet objectif leur parait vraiment difficile à atteindre.  Ceci est dans le but de pouvoir avoir un maximum de temps lors des prochaines séances pour pouvoir faire l’intégration.

**Lundi 13/11/2023**:
La dernière séance était il y a un mois, nous avons donc fait un rappel de l’architecture globale du projet et fait un point sur les avancées de certains groupes lors de ce mois, notamment l’équipe Storage qui a réussi à régler son problème d’installation.
- L’équipe Capteurs a réussi à envoyer des images compressées au broker. La taille des images envoyées est donc passée de 4Mo à 250ko. L’équipe a commencé un script pour automatiser la prise d’image mais elle a besoin de savoir combien d’images doivent être envoyées et tous les combien de temps. Elle a précisé à l’ensemble du groupe les 3 Raspberry utilisés (ceux reliés aux caméras). Elle n’envoie pas d’images à l’équipe messaging mais des images encodées en base 64 (string). Elle a communiqué ses besoins à l’équipe Déploiement. 
- L’équipe Messaging a écrit un script Bash pour l’installation et la mise en cluster. Il faut maintenant les placer sur les Raspberry. Pour l’instant, il n’y a pas de Gateway dans Rabbit MQ. L’équipe regarde les options pour mettre en place du mirroring sur les 3 nœuds. L’équipe est en train d'explorer la possibilité de définir la taille du buffer d'entrée. Actuellement, il n'y a pas de limite pour ce que nous envoyons, mais il est nécessaire de prendre en compte la capacité du réseau afin de ne pas le saturer. Le cluster est configuré mais n’a pas encore été testé. 
- L’équipe Reactive streaming a distribué les brokers (3 noeuds Zookeepers en architecture master/slave). Ils doivent maintenant “kafka-iser” les différents services. Elle a communiqué ses besoins à l’équipe Déploiement. 
- L’équipe Computing a mis en place un cluster avec une architecture master/slave avec 3 Raspberry.  Le but est de distribuer le travail entre plusieurs Raspberry (chaque Raspberry travaille sur un certain nombre d’images). Elle a fait la documentation pour l’équipe Déploiement. Il leur reste à voir comment envoyer leurs résultats à l’équipe Reactive streaming. 
- L’équipe Storage a réussi à résoudre son problème d’installation en passant les OS des Raspberry de 32 à 64 bits. Elle est en tain de mettre en place des réplicas sets mais doit déjà réussir à faire communiquer les Raspberry entre eux. Elle doit donc réussir à faire ça pour la prochaine séance. Elle a travaillé avec l’équipe Déploiement. 
- L’équipe Déploiement a conteneurisé les applications Kafka et Zookeeper. Il leur reste à régler le problème de la gestion des IP si un nœud tombe, avec K3s. Ils mettent également en place plusieurs serveurs pour ne pas avoir de problèmes si le serveur tombe.  Ansible sera utilisé pour les parties capteurs et messaging, car ça ne peut pas être dockerisé car ils ont besoin d’accéder au hardware. 
Chaque partie indépendante doit donc être terminée pour la prochaine séance qui a lieu dans 2 mois (26 janvier) ET doit également communiquer avec les parties précédentes et suivantes (et avec l’équipe déploiement) pour commencer les tests le plus rapidement possible à la prochaine séance. 

**Vendredi 26/01/2024** :
- 
- 
- 
- 
- 
- 

**Mardi 30/01/2024** :
- 
- 
- 
- 
- 

**Mercredi 31/01/2024** :
- 
- 
- 
- 
- 

**Soutenance 02/02/2024** :
- 
- 
- 
- 
- 
- 

## Procédure de mise en place de votre architecture Cloud IoT


## Conclusions et recommandations
