# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.OpenMayaUI as omui
from PySide6 import QtWidgets, QtCore, QtGui
from shiboken6 import wrapInstance
import os
import random
import math

# Liste pour garder les positions des Pokéballs déjà créées
existing_positions = []

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class PokeballUI(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(PokeballUI, self).__init__(parent)
        self.setWindowTitle("Pokeball Generator")
        self.setFixedSize(400, 300)
        
        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.size_label = QtWidgets.QLabel("Taille:")
        self.size_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.size_slider.setRange(1, 10)
        self.size_slider.setValue(5)

        self.pattern_label = QtWidgets.QLabel("Motif:")
        self.pattern_combo = QtWidgets.QComboBox()
        self.pattern_combo.addItems(["Pokeball", "Superball", "Hyperball", "Masterball"])

        self.texture_label = QtWidgets.QLabel("Texture:")
        self.texture_button = QtWidgets.QPushButton("Selectionner Texture")
        self.texture_path = QtWidgets.QLabel("Aucune texture selectionnée")

        self.generate_button = QtWidgets.QPushButton("Générer Pokeballs")

    def create_layout(self):
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.size_label)
        layout.addWidget(self.size_slider)
        layout.addWidget(self.pattern_label)
        layout.addWidget(self.pattern_combo)
        layout.addWidget(self.texture_label)
        layout.addWidget(self.texture_button)
        layout.addWidget(self.texture_path)
        layout.addWidget(self.generate_button)
        self.setLayout(layout)

    def create_connections(self):
        self.generate_button.clicked.connect(self.generate_pokeballs)
        self.texture_button.clicked.connect(self.select_texture)

    def select_texture(self):
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Selectionner Texture", "", "Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)", options=options)
        if file_path:
            self.texture_path.setText(file_path)

    def generate_pokeballs(self):
        size = self.size_slider.value()
        texture = self.texture_path.text()
        if texture == "Aucune texture selectionnée":
            texture = None

        pattern = self.pattern_combo.currentText()
        create_pokeball(size, pattern, texture)

def show_interface():
    ui = PokeballUI()
    ui.show()

def create_pokeball(size, pattern, texture_path):
    # Définir la couleur en fonction du type de Pokéball
    if pattern == "Pokeball":
        color = (1.0, 0.0, 0.0)  # Rouge
    elif pattern == "Superball":
        color = (0.0, 0.0, 1.0)  # Bleu
    elif pattern == "Hyperball":
        color = (0.0, 0.0, 0.0)  # Noir
    elif pattern == "Masterball":
        color = (0.4, 0.0, 0.7)  # Violet
    else:
        color = (1.0, 1.0, 1.0)  # Blanc par défaut

    # Générer des noms uniques pour les Pokéballs
    pokeball_name = pattern + "_" + str(len(existing_positions) + 1)

    # Créer la Pokéball
    sphere = cmds.polySphere(r=size, name=pokeball_name)[0]
    shader = cmds.shadingNode('lambert', asShader=True, name=f'{pokeball_name}_shader')
    shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f'{pokeball_name}_shadingGroup')
    cmds.connectAttr(f'{shader}.outColor', f'{shading_group}.surfaceShader', force=True)
    cmds.setAttr(f'{shader}.color', *color, type='double3')
    cmds.select(sphere)
    cmds.hyperShade(assign=shader)

    if texture_path and os.path.exists(texture_path):
        # Créer un fichier de texture
        file_node = cmds.shadingNode('file', asTexture=True, name=f'{pokeball_name}_texture')
        cmds.setAttr(f'{file_node}.fileTextureName', texture_path, type="string")

        # Créer un place2dTexture node et connecter les attributs nécessaires
        place2d = cmds.shadingNode('place2dTexture', asUtility=True)
        cmds.connectAttr(f'{place2d}.coverage', f'{file_node}.coverage')
        cmds.connectAttr(f'{place2d}.translateFrame', f'{file_node}.translateFrame')
        cmds.connectAttr(f'{place2d}.rotateFrame', f'{file_node}.rotateFrame')
        cmds.connectAttr(f'{place2d}.mirrorU', f'{file_node}.mirrorU')
        cmds.connectAttr(f'{place2d}.mirrorV', f'{file_node}.mirrorV')
        cmds.connectAttr(f'{place2d}.stagger', f'{file_node}.stagger')
        cmds.connectAttr(f'{place2d}.wrapU', f'{file_node}.wrapU')
        cmds.connectAttr(f'{place2d}.wrapV', f'{file_node}.wrapV')
        cmds.connectAttr(f'{place2d}.repeatUV', f'{file_node}.repeatUV')
        cmds.connectAttr(f'{place2d}.offset', f'{file_node}.offset')
        cmds.connectAttr(f'{place2d}.rotateUV', f'{file_node}.rotateUV')
        cmds.connectAttr(f'{place2d}.noiseUV', f'{file_node}.noiseUV')
        cmds.connectAttr(f'{place2d}.vertexUvOne', f'{file_node}.vertexUvOne')
        cmds.connectAttr(f'{place2d}.vertexUvTwo', f'{file_node}.vertexUvTwo')
        cmds.connectAttr(f'{place2d}.vertexUvThree', f'{file_node}.vertexUvThree')
        cmds.connectAttr(f'{place2d}.vertexCameraOne', f'{file_node}.vertexCameraOne')
        cmds.connectAttr(f'{place2d}.outUV', f'{file_node}.uvCoord')
        cmds.connectAttr(f'{place2d}.outUvFilterSize', f'{file_node}.uvFilterSize')

        # Connecter le fichier de texture au shader
        cmds.connectAttr(f'{file_node}.outColor', f'{shader}.color')

    # Appliquer une animation simple
    animate_appearance(sphere)

    # Placer la Pokéball aléatoirement dans la scène sans collision
    position = get_non_colliding_position(size)
    cmds.move(position[0], position[1], position[2], sphere)
    existing_positions.append(position)

def animate_appearance(object_name):
    # Animation de mise à l'échelle rapide
    cmds.setKeyframe(object_name, attribute='scaleX', t=0, v=0.1)
    cmds.setKeyframe(object_name, attribute='scaleY', t=0, v=0.1)
    cmds.setKeyframe(object_name, attribute='scaleZ', t=0, v=0.1)
    cmds.setKeyframe(object_name, attribute='scaleX', t=10, v=1)
    cmds.setKeyframe(object_name, attribute='scaleY', t=10, v=1)
    cmds.setKeyframe(object_name, attribute='scaleZ', t=10, v=1)

    # S'assurer que l'animation ne boucle pas
    cmds.playbackOptions(loop='once')

def get_non_colliding_position(size):
    # Essayer de trouver une position non-collision
    max_attempts = 100
    for attempt in range(max_attempts):
        x = random.uniform(-10, 10)
        y = random.uniform(0, 5)
        z = random.uniform(-10, 10)
        collides = False
        for pos in existing_positions:
            if distance(pos, (x, y, z)) < size * 2:
                collides = True
                break
        if not collides:
            return (x, y, z)
    # Si aucune position non-collision n'a été trouvée, retourner une position par défaut
    return (0, size, 0)

def distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2 + (pos1[2] - pos2[2])**2)

def hex_to_rgb(hex_color):
    hex_color = hex_color.strip()
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]
        return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    else:
        return (1.0, 1.0, 1.0)  # Default white color if parsing fails

if __name__ == "__main__":
    show_interface()
