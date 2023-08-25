import os
import time
import uuid

import edsdk
from edsdk import (
    CameraCommand,
    ObjectEvent,
    PropID,
    FileCreateDisposition,
    Access,
    SaveTo,
    EdsObject,
    DriveMode,
    Av,
    ApertureValue,
)

if os.name == "nt":
    # If you're using the EDSDK on Windows,
    # you have to have a Windows message loop in your main thread,
    # otherwise callbacks won't happen.
    # (This is because the EDSDK uses the obsolete COM STA threading model
    # instead of real threads.)
    import pythoncom


def save_image(object_handle: EdsObject, save_to: str) -> int:
    dir_item_info = edsdk.GetDirectoryItemInfo(object_handle)
    out_stream = edsdk.CreateFileStream(
        os.path.join(save_to, str(uuid.uuid4()) + ".raw"),
        FileCreateDisposition.CreateAlways,
        Access.ReadWrite)
    edsdk.Download(object_handle, dir_item_info["size"], out_stream)
    edsdk.DownloadComplete(object_handle)
    return 0


def callback_property(event, property_id: PropID, parameter: int) -> int:
    print("event: ", event)
    print("Property changed:", property_id)
    print("Parameter:", parameter)
    return 0


def callback_object(event: ObjectEvent, object_handle: EdsObject) -> int:
    print("event: ", event, "object_handle:", object_handle)
    if event == ObjectEvent.DirItemRequestTransfer:
        save_image(object_handle, ".")
    return 0


if __name__ == "__main__":
    edsdk.InitializeSDK()
    cam_list = edsdk.GetCameraList()
    nr_cameras = edsdk.GetChildCount(cam_list)

    if nr_cameras == 0:
        print("No cameras connected")
        exit(1)

    cam = edsdk.GetChildAtIndex(cam_list, 0)
    edsdk.OpenSession(cam)
    edsdk.SetObjectEventHandler(cam, ObjectEvent.All, callback_object)
    edsdk.SetPropertyData(cam, PropID.SaveTo, 0, SaveTo.Camera)
    edsdk.SetPropertyData(cam, PropID.DriveMode, 0, DriveMode.SingleShooting)

    r = edsdk.GetPropertyDesc(cam, PropID.Av)
    print(r)

    valid_avs = set(r["propDesc"])

    if ApertureValue.F_1 in valid_avs:
        print(" is supported")

    if ApertureValue.F_2 in valid_avs:
        print(f"F{Av[ApertureValue.F_2]} is supported")



    if os.name == "nt":
        pythoncom.PumpWaitingMessages()

    edsdk.TerminateSDK()
