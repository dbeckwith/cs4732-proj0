#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import math

from PyQt5 import QtCore, QtGui, QtWidgets, Qt3DCore, Qt3DRender, Qt3DExtras

from .animation import Animation
from . import util


class Proj0Ani(Animation):
    def __init__(self, frame_rate, run_time):
        super().__init__('CS 4732 Project 0 by Daniel Beckwith', frame_rate, run_time)

        self.setup_scene(
            background_color=util.hsl(0, 0, 0),
            camera_position=QtGui.QVector3D(0.0, 0.0, -10.0),
            camera_lookat=QtGui.QVector3D(0.0, 0.0, 0.0))

    def make_scene(self):
        cube_entity = Qt3DCore.QEntity(self.scene)
        cube_mesh = Qt3DExtras.QCuboidMesh()
        cube_mesh.setXExtent(1.0)
        cube_mesh.setYExtent(1.0)
        cube_mesh.setZExtent(1.0)
        cube_entity.addComponent(cube_mesh)
        self.cube_transform = Qt3DCore.QTransform()
        cube_entity.addComponent(self.cube_transform)
        self.cube_material = Qt3DExtras.QPhongMaterial(self.scene)
        self.cube_material.setSpecular(util.hsl(0, 0, 100))
        self.cube_material.setShininess(0.0)
        cube_entity.addComponent(self.cube_material)

        self.add_light(util.hsl(0, 0, 100), 1.0, QtGui.QVector3D(-20.0, 20.0, -20.0))
        self.add_light(util.hsl(0, 0, 100), 0.5, QtGui.QVector3D(20.0, 10.0, -20.0))

    def update(self, frame, t, dt):
        self.cube_transform.setRotation(QtGui.QQuaternion.fromEulerAngles(
            util.rad2deg(math.atan(1 / math.sqrt(2))),
            util.lerp(t, 0, 1, 0, 90),
            45))
        hue = util.lerp(t, 0, self.run_time, 0, 360) + 180
        self.cube_material.setAmbient(util.hsl(hue, 100, 10))
        self.cube_material.setDiffuse(util.hsl(hue, 100, 50))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser('proj0')
    args = parser.parse_args()

    app = QtWidgets.QApplication([])

    ani = Proj0Ani(
        frame_rate=100.0,
        run_time=10.0)
    ani.run()

    sys.exit(app.exec_())
