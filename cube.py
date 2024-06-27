import maya.cmds as cmds
import os

def create_textured_cube(texture_path):
    # Vérifiez si le chemin de la texture existe
    if not os.path.exists(texture_path):
        print(f"Texture path {texture_path} does not exist.")
        return

    # Créer le cube
    cube = cmds.polyCube(w=1, h=1, d=1, name="TexturedCube")[0]
    
    # Créer un shader Lambert
    shader = cmds.shadingNode('lambert', asShader=True, name='cube_shader')
    shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name='cube_shadingGroup')
    cmds.connectAttr(f'{shader}.outColor', f'{shading_group}.surfaceShader', force=True)
    
    # Créer un fichier de texture
    file_node = cmds.shadingNode('file', asTexture=True, name='cube_texture')
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
    
    # Appliquer le shader au cube
    cmds.select(cube)
    cmds.hyperShade(assign=shader)

# Remplacez ce chemin par le chemin de votre fichier de texture
texture_path = "C:/Users/Badro/Pictures/fond-ecran/ronona-zoro-one-piece-thumb.jpg"
create_textured_cube(texture_path)
