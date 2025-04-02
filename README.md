# Pi GPIO Server

This project contains a small HTTP Server to toggle GPIOs on a Raspberry Pi.

## Setup the Pi
You will need
- A Raspberry Pi
- A Micro SD Card with at least 16 GB 

First download the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) and install it. Insert the MicroSD Card into your PC. Open the Raspberry Pi Imager, select the right model, Raspberry Pi OS as operating system and the MicroSD cart as and hit next.
Select edit settings and set a Hostname, e.g. *agbspi3*, Username *pi*, password *pi* and the right timezone and keyboard layout. Save these values and finishe the installation. After the card is ready, insert it into the Pi and connect it to a powersupply and network. 

## Connect to the device
Open up [Visual Studio Code](https://code.visualstudio.com/) and click the small ![](assets/images/vscode-connect-to-host.PNG) button in the bottom left corner.

Select *Connect to host*  pi@**\<hostname selected during setup\>**.bs.etit.tu-dortmund.de, when promted select Linux and accept the fingerprint. Enter *pi* as password. VS Code will take a moment to setup the connection. 

## Setup the server environment

