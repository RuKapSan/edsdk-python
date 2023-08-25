import logging

import os
from edsdk import *
from utils.Wrappers import safe_api_access
from time import sleep

from logging import info, debug, warning, error, critical
class Camera:
    """
    Wrapper for the camera edsdk object, handles the session and provides an interface to the camera
    """
    if os.name == "nt":
        import pythoncom

    def __init__(self):
        """Initializes the camera and opens a session"""
        self.cam_list = GetCameraList()
        if GetChildCount(self.cam_list) == 0:
            print("No cameras connected, retrying in 5 seconds")
            sleep(5)
        self.cam = GetChildAtIndex(self.cam_list, 0)
        if GetChildCount(self.cam_list) > 1:
            print("More than one camera connected, using first one")
        OpenSession(self.cam)
        debug("Camera session opened successfully")

        self.valid_avs = None


    # Setters
    @safe_api_access
    def set_drive_mode(self, drive_mode: DriveMode):
        SetPropertyData(self.cam, PropID.DriveMode, 0, drive_mode)

    @safe_api_access
    def set_image_destination(self, save_to: SaveTo):
        SetPropertyData(self.cam, PropID.SaveTo, 0, save_to)

    @safe_api_access
    def set_image_quality(self, quality: ImageQuality):
        SetPropertyData(self.cam, PropID.ImageQuality, 0, quality)

    @safe_api_access
    def set_iso(self, iso: ISOSpeedCamera):
        SetPropertyData(self.cam, PropID.ISOSpeed, 0, iso)
        debug(f"ISO set to {iso}")

    @safe_api_access
    def set_metering_mode(self, metering_mode: MeteringMode):
        SetPropertyData(self.cam, PropID.MeteringMode, 0, metering_mode)
        debug(f"Metering mode set to {Me[metering_mode]}")

    @safe_api_access
    def set_af_mode(self, af_mode: AFMode):
        SetPropertyData(self.cam, PropID.AFMode, 0, af_mode)
        debug(f"AF mode set to {af_mode}")

    @safe_api_access
    def set_aperture(self, aperture: ApertureValue):
        if self.valid_avs is None:
            self.valid_avs = set(GetPropertyDesc(self.cam, PropID.Av)["propDesc"])

        if aperture not in self.valid_avs:
            raise ValueError(f"Aperture {Av[aperture]} is not supported by the camera")

        SetPropertyData(self.cam, PropID.Av, 0, aperture)
        debug(f"Aperture set to {Av[aperture]}")

