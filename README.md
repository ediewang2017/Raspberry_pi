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

After connecting in VS Code, open a terminal and enter
`git clone https://gitlab.tu-dortmund.de/agbs/tools/pi-gpio-server.git`. When promted, enter your credentials to authenticate to git. It will automatically download the code. Switch to the Explorer Tab in VS Code, click on *Open Folder* and select *pi-gpio-server*. It will open a new window and ask for the password of the pi again. You will then have entered the code folder of the server. 

## Set the server to autostart
The configuration to use the server as a system service is in [pi-gpio-server.service](pi-gpio-server.service). It is set for the [app.py](app.py) being in the folder `/home/pi/pi-gpio-server`. If you changed the path, you will also have to change `ExecStart` and `WorkingDirectory` accordingly. 

In a terminal run

```sh
sudo cp pi-gpio-server.service /etc/systemd/system/
```
to copy the file to the system directory. 

```sh
sudo systemctl daemon-reload && \
sudo systemctl enable pi-gpio-server && \
sudo systemctl start pi-gpio-server
```
to reload the system and enable the server. 

## Test the server
In a command line run
```sh
curl http://<URL or IP of your Pi>:5000/0F0F
```
When measuring the GPIO Pins, 
- 4,17,18,27 should be `HIGH` 
- 22,23,24,25 should be `LOW`
- 5,6,12,13 should be `HIGH`
- 16,19,20,21 should be `LOW`

and the console should show
```
{"dec":3855,"hex":"0F0F","message":"Set GPIOs to 0b111100001111"}
```

You can test any other number after the `/` and verify the results. 

__*Sometimes connection through URL does not work. Try IPv4 then instead*__

## Contacting the server from python
In [example.py](example.py) there is a minimalistic example including output and error handling.
The important lines here are 

```py
import requests

...

requests.get(f'{host}/{value:04X}')
```
You need to import the request module and add the value you want to set as hex encoded number. 

## Contacting the server from Matlab

An equivalent to the Python code in Matlab can be found in [example.m](example.m).
The most minimal approach here is
```matlab
value = hex2dec('FFFF');
url = sprintf('http://127.0.0.1:5000/%s', upper(dec2hex(value, 4)));
webread(url);
```

## Bit to Pin Map
| Bit | GPIO |
|-----|------|
|  0  |  4   |
|  1  | 17   |
|  2  | 18   |
|  3  | 27   |
|  4  | 22   |
|  5  | 23   |
|  6  | 24   |
|  7  | 25   |
|  8  |  5   |
|  9  |  6   |
| 10  | 12   |
| 11  | 13   |
| 12  | 16   |
| 13  | 19   |
| 14  | 20   |
| 15  | 21   |
