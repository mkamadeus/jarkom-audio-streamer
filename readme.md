# Simple Python Audio Streamer

> Socket programming in Python using datagram sockets.

## Requirements

- Having Python 3, preferably version 3.8 and upwards.

## Running

1. Create a venv using this command:

```bash
python3 -m venv venv
```

2. Create two terminals; one for the client and one for the server. For each of the terminals, enter the venv using this command:

```bash
source "./venv/bin/activate"
```

3. Run the client on one terminal, and run the server on the other. Run them using provided shell file.

```bash
./run-server.sh <port> <audio-in-folder>
./run-gui-client.sh <ip-address> <port>
```

Note that ip-address of client GUI is not necessary, as autodiscovery has been implemented.

4. Enjoy?

## Troubleshooting Related to Libraries

To install PyAudio, in Ubuntu/Linux distributions you need to install several packages if an error occurs:

```bash
sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
```

pysimplegui requirements:

```bash
sudo apt-get install python3-tk
```
