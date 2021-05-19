# MicroGUI
The MicroGUI project is a user interface and hardware integration project for the FAR-IR beamline of the Canadian Light Source Inc.. The platform integrates with the facilities EPICS distributed control system, FLIR Blackfly camera and THORLABS motor stage to allow for remote control of the FAR-IR infrared horizontal microscope.

# Dependencies
In addition to imported Python libraries, the microgui project has various software dependencies that require instillation for successful hardware integration. Specifically, the THORLABS APT software and the FLIR Spinnaker SDK.

## THORLABS Dependency Configuration
Begin by downloading and installing the appropriate APT software from the follwofing link:
* **THORLABS APT:** https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control&viewtab=1

To allow for the microgui program to use the *thorlabs_apt* library, they *APT.dll* file from the THORLABS APT software should be copied over to the *thorlabs_apt* folder. Note that with default instillation, the *APT.dll* file can be found in the following path, *C:\Program Files\Thorlabs\APT\APT Server*.

## FLIR Dependency Configuration
From the Spinnaker SDK download website, download and install the Spinnaker software that matches your operating system and architechture. Additionally, doownload and unzip the latest Python Spinnaker (PySpin) that matches your python version.
* **Spinnaker SDK:** https://flir.app.boxcn.net/v/SpinnakerSDK

Navigate to the PySpin directory in a terminal and install the WHL file using the following commands:
```Terminal
$ cd <PySpin_whl_unzip_destination>
$ pip install --user <PySpin_ehl_file>
```

# Run
To run the microgui project, ensure you are running on the FAR-IR desktop (either directly or remotely) and run the main.py file.

# Conditions on Use
In addition to having dependencies installed, various points of consideration should be made to ensure proper operation of the microgui.
* All hardware should be connected before program initiation.
* Thorlabs Kinesis software should not be operational when instantiating the program.
