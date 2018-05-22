# Python - Health Client

Rationale:
This application is dedicated to monitoring BLE Mesh network based on reports send by Health Servers. 
Application requires UART Modem device with firmware version >= 2.7.0.

Short instruction describing how to run Health Client:
1. Create virtualenv with command `virtualenv -p python3.6 venv`
2. Activate virtualenv `source venv/bin/activate.sh`
3. Install required dependecies `pip install --process-dependency-links .`
4. Run Health Client `python main.py --port /dev/ttyUSB0`
5. Type `help` and press enter to get list of available commands.

# FAQ

Question:
I've got UART Error! InvalidState what to do?
Answer:
Probably subscriber has not been set. Please make sure that Health Client model has been registered (information in logs).
