import shutil

# Chemin de l'image originale
source_image_path = '/Users/salahidbelouch/Documents/projects/CIT/dockerSpark/test1.jpeg'

# Dossier où les images copiées seront enregistrées
destination_folder1 = '/Users/salahidbelouch/Documents/projects/CIT/dockerSpark/apps/sparkJob/images/'
destination_folder2 = '/Users/salahidbelouch/Documents/projects/CIT/dockerSpark/apps/sparkWork/images/'
# Créer 100 copies de l'image
for i in range(1, 101):
    destination_image_path1 = f'{destination_folder1}image{i}.jpeg'
    shutil.copy(source_image_path, destination_image_path1)
    destination_image_path2 = f'{destination_folder2}image{i}.jpeg'
    shutil.copy(source_image_path, destination_image_path2)

print("100 copies de l'image ont été créées.")