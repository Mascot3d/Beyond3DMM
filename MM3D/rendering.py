#!/usr/bin/env python3
# coding: utf-8

import sys

import os
import os.path as osp
from glob import glob

from .lighting import RenderPipeline
import numpy as np
import scipy.io as sio
import imageio
import matplotlib.pyplot as plt

cfg = {
    'intensity_ambient': 0.3,
    'color_ambient': (1, 1, 1),
    'intensity_directional': 0.6,
    'color_directional': (1, 1, 1),
    'intensity_specular': 0.1,
    'specular_exp': 5,
    'light_pos': (0, 0, 5),
    'view_pos': (0, 0, 5)
}


def _to_ctype(arr):
    if not arr.flags.c_contiguous:
        return arr.copy(order='C')
    return arr

def DrawHeadMesh(vertex_in, tri, img):
    vertex = vertex_in.copy()
    [height, width, nChannels] = img.shape
    triangles = _to_ctype(tri.T).astype(np.int32)  # for type compatible
    vertex[1,:] = -vertex[1,:] + height
    vertex = _to_ctype(vertex.T).astype(np.float32)
    app = RenderPipeline(**cfg)
    img_render = app(vertex, triangles, img)
    img_render = img_render.astype(np.float32) / 255.
    temp = img * 0.5 + img_render * 0.5
    plt.imshow(temp)




def obama_demo():
    wd = 'obama_res@dense_py'
    if not osp.exists(wd):
        os.mkdir(wd)

    app = RenderPipeline(**cfg)
    img_fps = sorted(glob('obama/*.jpg'))
    triangles = sio.loadmat('tri_refine.mat')['tri']  # mx3
    triangles = _to_ctype(triangles).astype(np.int32)  # for type compatible

    for img_fp in img_fps[:]:
        vertices = sio.loadmat(img_fp.replace('.jpg', '_0.mat'))['vertex'].T  # mx3
        img = imageio.imread(img_fp).astype(np.float32) / 255.

        # end = time.clock()
        img_render = app(vertices, triangles, img)
        # print('Elapse: {:.1f}ms'.format((time.clock() - end) * 1000))

        img_wfp = osp.join(wd, osp.basename(img_fp))
        imageio.imwrite(img_wfp, img_render)
        print('Writing to {}'.format(img_wfp))


if __name__ == '__main__':
    obama_demo()
