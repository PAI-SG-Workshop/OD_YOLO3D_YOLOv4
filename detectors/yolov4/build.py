"""
YOLOv4 builders for the three tasks (Darknet yolov4.cfg from the Legacy v4 projects).

Architecture (algorithm-specific, this folder):
    CSPDarknet53 backbone (Mish) + SPP + PANet neck, three scales
    (strides 8, 16, 32), anchors kept from the Legacy v4 cfg files.

Detection layers: reused unchanged from detectors/yolov3 (maximum code reuse).
    image   -> Image YOLO layer   (global 9-anchor matching)
    complex -> Complex-YOLO layer (E-RPN im/re angle)      - paper: YOLOv2-based
    yolo3d  -> YOLO3D layer       (direct yaw, z, h)        - paper: YOLOv2-based

Not used from the Legacy v4 projects (so v4 differs from v3 in architecture only):
    - Image v4 GIoU "global loss" layer  -> shared Image YOLO layer
    - [yolo] scale_x_y (grid sensitivity) -> ignored by the shared layers
    - Mosaic / other training tricks      -> common protocol
"""

from pathlib import Path

from common.darknet import Darknet
from detectors.yolov3.build import yolo3d_factory

CFG_DIR = Path(__file__).resolve().parent / "cfg"

SPECS = {
    "yolo3d":  ("yolo3d_yolov4.cfg",  yolo3d_factory,  8),
}


def build_model(task, num_classes):
    cfg_name, factory, num_box_attr = SPECS[task]
    return Darknet(CFG_DIR / cfg_name, factory, num_classes, num_box_attr)
