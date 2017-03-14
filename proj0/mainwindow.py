import numpy as np
from pyrr import Vector3, Vector4, Matrix44
import OpenGL
OpenGL.ERROR_CHECKING = True
OpenGL.FULL_LOGGING = True
from OpenGL.GL import *
from OpenGL.GL import shaders
from PyQt5 import QtCore, QtGui, QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('CS 4732 Project 0 by Daniel Beckwith')

        self.canvas = GLWidget(self)

        self.setCentralWidget(self.canvas)

        self.canvas.gl_initialized.connect(self.__show_gl_version)

    def __show_gl_version(self):
        version_str = str(glGetString(GL_VERSION), 'utf-8')
        shader_version_str = str(glGetString(GL_SHADING_LANGUAGE_VERSION), 'utf-8')
        msg = 'Loaded OpenGL {} with GLSL {}'.format(version_str, shader_version_str)
        print(msg)
        self.statusBar().showMessage(msg)

        print('All supported GLSL versions:')
        num_shading_versions = np.empty((1,), dtype=np.int32)
        glGetIntegerv(GL_NUM_SHADING_LANGUAGE_VERSIONS, num_shading_versions)
        print()
        for i in range(num_shading_versions[0]):
            print(str(glGetStringi(GL_SHADING_LANGUAGE_VERSION, i), 'utf-8'))
        print()

class GLWidget(QtWidgets.QOpenGLWidget):
    vshader_source = """
#version 450

uniform mat4 MVP;

in vec3 position;

void main() {
    gl_Position = MVP * vec4(position, 1.0);
}
"""
    fshader_source = """
#version 450

out vec4 color;

void main() {
    color = vec4(1, 0, 0, 1);
}
"""

    gl_initialized = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)

    def sizeHint(self):
        return QtCore.QSize(800, 500)

    def calc_view_mat(self, eye, at, up):
        zaxis = (at - eye).normalised
        xaxis = up.cross(zaxis).normalised
        yaxis = zaxis.cross(xaxis)
        self.view_mat = Matrix44(
            [[        xaxis.x,         yaxis.x,         zaxis.x, 0],
             [        xaxis.y,         yaxis.y,         zaxis.y, 0],
             [        xaxis.z,         yaxis.z,         zaxis.z, 0],
             [-xaxis.dot(eye), -yaxis.dot(eye), -zaxis.dot(eye), 1]],
            dtype=np.float32)

    def initializeGL(self):
        self.gl_initialized.emit()

        glShadeModel(GL_FLAT)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

        vshader = shaders.compileShader(self.vshader_source, GL_VERTEX_SHADER)
        fshader = shaders.compileShader(self.fshader_source, GL_FRAGMENT_SHADER)
        self.shader = shaders.compileProgram(vshader, fshader)

        self.mvp_loc = glGetAttribLocation(self.shader, 'MVP')
        self.model_mat = Matrix44.identity(dtype=np.float32)
        self.calc_view_mat(
            eye=Vector3([0.0, 0.0, -10.0]),
            at=Vector3([0.0, 0.0, 0.0]),
            up=Vector3([0.0, 1.0, 0.0]))
        self.projection_mat = Matrix44.perspective_projection(
            fovy=45.0,
            aspect=1.0,
            near=0.01,
            far=100.0,
            dtype=np.float32)

        self.vertices = np.array(
            [[-1, -1,  0],
             [ 1, -1,  0],
             [ 0,  1,  0]],
            dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        position_loc = glGetAttribLocation(self.shader, 'position')
        glEnableVertexAttribArray(position_loc)
        glVertexAttribPointer(
            index=position_loc,
            size=self.vertices.shape[-1],
            type=GL_FLOAT,
            normalized=GL_FALSE,
            stride=0,
            pointer=None)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def paintGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(self.shader)

        glBindVertexArray(self.vao)

        mvp = self.projection_mat * self.view_mat * self.model_mat
        glUniformMatrix4fv(self.mvp_loc, 1, GL_FALSE, mvp)
        glDrawArrays(GL_TRIANGLES, 0, self.vertices.shape[0])
        glBindVertexArray(0)

        glUseProgram(0)

    def resizeGL(self, width, height):
        pass
