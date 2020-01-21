#!/usr/bin/env python3

class Cam():
    """
    Base class for camera
    """
    cam_count = 0

    def __init__(self, ip, fulladress, nr, instances):
        self.ip = ip
        self.fulladress = fulladress
        self.nr = nr
        self.instances = instances
