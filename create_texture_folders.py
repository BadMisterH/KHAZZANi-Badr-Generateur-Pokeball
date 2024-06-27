import os

# Chemin de la racine de votre projet
root_path = os.path.abspath(os.path.dirname(__file__))
textures_path = os.path.join(root_path, 'Textures')

# Noms des sous-dossiers
subfolders = ['Pokeball', 'Superball', 'Hyperball', 'Masterball']

# Créez le dossier 'Textures' s'il n'existe pas
if not os.path.exists(textures_path):
    os.makedirs(textures_path)

# Créez les sous-dossiers pour chaque type de Pokéball
for folder in subfolders:
    folder_path = os.path.join(textures_path, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

print("Structure des dossiers de textures créée avec succès.")
