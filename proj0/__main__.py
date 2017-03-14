#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import math

from OpenGL import GL
from PyQt5 import QtCore, QtGui, QtWidgets, Qt3DCore, Qt3DRender, Qt3DExtras


def lerp(x, old_min, old_max, new_min, new_max):
    return (x - old_min) / (old_max - old_min) * (new_max - new_min) + new_min


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser('proj0')
    args = parser.parse_args()

    app = QtWidgets.QApplication([])

    view = Qt3DExtras.Qt3DWindow()
    view.setTitle('CS 4732 Project 0 by Daniel Beckwith')

    view.defaultFrameGraph().setClearColor(QtGui.QColor.fromHsvF(0/360, 0.00, 0.00))

    scene = Qt3DCore.QEntity()

    material = Qt3DExtras.QPhongMaterial(scene)
    material.setAmbient(QtGui.QColor.fromHsvF(180/360, 1.00, 0.50))

    cube_entity = Qt3DCore.QEntity(scene)
    cube_mesh = Qt3DExtras.QCuboidMesh()
    cube_mesh.setXExtent(1.0)
    cube_mesh.setYExtent(1.0)
    cube_mesh.setZExtent(1.0)
    cube_transform = Qt3DCore.QTransform()
    cube_entity.addComponent(cube_mesh)
    cube_entity.addComponent(cube_transform)
    cube_entity.addComponent(material)

    light_entity = Qt3DCore.QEntity(scene)
    light = Qt3DRender.QPointLight(light_entity)
    light.setColor(QtGui.QColor.fromHsvF(0/360, 0.00, 1.00))
    light.setIntensity(1.0)
    light_transform = Qt3DCore.QTransform()
    light_transform.setTranslation(QtGui.QVector3D(-20.0, 20.0, -20.0))
    light_entity.addComponent(light)
    light_entity.addComponent(light_transform)

    camera = view.camera()
    # camera.lens().setPerspectiveProjection(45.0, 1.0, 0.1, 1000.0)
    camera.setPosition(QtGui.QVector3D(0.0, 0.0, -10.0))
    camera.setViewCenter(QtGui.QVector3D(0.0, 0.0, 0.0))

    frame_rate = 100
    run_time = 10.0
    frame = 0
    def update():
        global frame
        t = lerp(frame, 0, frame_rate, 0, 1)

        cube_transform.setRotation(QtGui.QQuaternion.fromEulerAngles(
            math.atan(1 / math.sqrt(2)) * 180 / math.pi,
            lerp(t, 0, 1, 0, 90),
            45.0))

        if t >= run_time:
            animation_timer.stop()
            view.close()
        frame += 1

    animation_timer = QtCore.QTimer(view)
    animation_timer.setInterval(1000 / frame_rate)
    animation_timer.timeout.connect(update)
    animation_timer.start()

    # cam_ctrl = Qt3DExtras.QOrbitCameraController(scene)
    # cam_ctrl.setLinearSpeed(50.0)
    # cam_ctrl.setLookSpeed(180.0)
    # cam_ctrl.setCamera(camera)

    view.setRootEntity(scene)

    view.show()

    sys.exit(app.exec_())
