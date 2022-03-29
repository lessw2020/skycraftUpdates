from ursina import *

hotbar=Entity(model='quad',parent=camera.ui)
hotbar.scale_y=0.08
hotbar.scale_x=0.8
hotbar.y=-0.5+(hotbar.scale_y*0.5)
hotbar.color=color.dark_gray

def inv_input(key,subject,mouse):
    if key=='e'and subject.enabled:
        subject.disable()
        mouse.locked=False
    elif key=='e'and not subject.enabled:
        subject.enable()
        mouse.locked=True
    