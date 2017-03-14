# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets, Qt3DCore, Qt3DRender, Qt3DExtras

from . import util


class Animation(object):
    def __init__(self, title, frame_rate, run_time):
        self.title = title
        self.frame_rate = frame_rate
        self.run_time = run_time

        self.frame = 0
        self.prev_update_time = None

        from OpenGL import GL
        self.view = Qt3DExtras.Qt3DWindow()
        self.view.setTitle(self.title)

    def add_light(self, color, intensity, position):
        light_entity = Qt3DCore.QEntity(self.scene)
        light = Qt3DRender.QPointLight(light_entity)
        light.setColor(color)
        light.setIntensity(intensity)
        light_transform = Qt3DCore.QTransform()
        light_transform.setTranslation(position)
        light_entity.addComponent(light)
        light_entity.addComponent(light_transform)

    def setup_scene(self, background_color, camera_position, camera_lookat):
        self.view.defaultFrameGraph().setClearColor(background_color)
        self.scene = Qt3DCore.QEntity()

        self.make_scene()

        camera = self.view.camera()
        camera.setPosition(camera_position)
        camera.setViewCenter(camera_lookat)

        self.view.setRootEntity(self.scene)

    def make_scene(self):
        raise NotImplementedError()

    def _update(self):
        t = util.lerp(self.frame, 0, self.frame_rate, 0, 1)
        dt = 1 / self.frame_rate if self.prev_update_time is None else t - self.prev_update_time
        self.update(self.frame, t, dt)

        if t >= self.run_time:
            self.animation_timer.stop()
            self.view.close()

        self.prev_update_time = t
        self.frame += 1

    def update(self, frame, t, dt):
        raise NotImplementedError()

    def run(self):
        self.animation_timer = QtCore.QTimer(self.view)
        self.animation_timer.setInterval(1000 / self.frame_rate)
        self.animation_timer.timeout.connect(self._update)
        self.animation_timer.start()

        self.view.show()
