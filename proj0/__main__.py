#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

import sys
import math

from PyQt5 import QtCore, QtGui, QtWidgets, Qt3DCore, Qt3DRender, Qt3DExtras

from .animation import Animation
from . import util


class Proj0Ani(Animation):
    """
    Implements the simple cube animation.
    """

    def __init__(self, frame_rate, run_time):
        super().__init__('CS 4732 Project 0 by Daniel Beckwith', frame_rate, run_time)

        self.setup_scene(
            background_color=util.hsl(0, 0, 0),
            camera_position=QtGui.QVector3D(0.0, 0.0, -10.0),
            camera_lookat=QtGui.QVector3D(0.0, 0.0, 0.0))

    def make_scene(self):
        """
        Overriddes Animation.make_scene
        """
        # create a cube object
        cube_entity = Qt3DCore.QEntity(self.scene)
        cube_mesh = Qt3DExtras.QCuboidMesh()
        cube_mesh.setXExtent(1.0)
        cube_mesh.setYExtent(1.0)
        cube_mesh.setZExtent(1.0)
        cube_entity.addComponent(cube_mesh)
        # transform controls the cube's position, rotation, scale
        self.cube_transform = Qt3DCore.QTransform()
        cube_entity.addComponent(self.cube_transform)
        # material controls the cube's appearence
        self.cube_material = Qt3DExtras.QPhongMaterial(self.scene)
        self.cube_material.setSpecular(util.hsl(0, 0, 100))
        self.cube_material.setShininess(0.0)
        cube_entity.addComponent(self.cube_material)

        # add some lights
        self.add_light(QtGui.QVector3D(-20.0, 20.0, -20.0), 1.0) # upper right key light
        self.add_light(QtGui.QVector3D(20.0, 10.0, -20.0), 0.5) # upper left fill light

    def update(self, frame, t, dt):
        """
        Overriddes Animation.update
        """
        self.cube_transform.setRotation(QtGui.QQuaternion.fromEulerAngles(
            util.rad2deg(math.atan(1 / math.sqrt(2))),
            util.lerp(t, 0, 1, 0, 90),
            45))
        hue = util.lerp(t, 0, self.run_time, 0, 360) + 180
        self.cube_material.setAmbient(util.hsl(hue, 100, 10))
        self.cube_material.setDiffuse(util.hsl(hue, 100, 50))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        prog='proj0',
        description='Animates a simple rotating cube.',
        epilog='Created by Daniel Beckwith for WPI CS 4732.')
    parser.add_argument('--frame_rate', '-f', type=float, default=100.0, help='Number of frames to render per second, default 100 fps.')
    parser.add_argument('--run_time', '-t', type=float, default=10.0, help='Number of seconds to run the animation for, default 10 sec.')
    args = parser.parse_args()

    app = QtWidgets.QApplication([])

    ani = Proj0Ani(
        frame_rate=args.frame_rate,
        run_time=args.run_time)
    ani.run()

    sys.exit(app.exec_())
