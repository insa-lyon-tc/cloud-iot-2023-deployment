### Computing :


Commande de lancement de la partie computing avec le fetch des images des topics et leurs traitement puis renvoie vers les topics processed :
- À adapter au deploiement. L'ip du pod du master de ce deploiement est 10.42.8.8 . Si l'ip change, il faut la changer dans le commande. 
- Il faut avoir le fichier sparkjob2.py et le dossier tf-model dans le dossier /opt/spark-apps de tous les pods ( master et workers)

```
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.3 --conf spark.executor.memory=2g --conf spark.driver.port=32831 --conf spark.driver.host=10.42.8.8 --master spark://10.42.8.8:7077 --deploy-mode client /opt/spark-apps/sparkjob2.py

```