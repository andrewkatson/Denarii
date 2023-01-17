# Denarii GUI

## Building 

The below assumes you have all the necessary files in one folder. The configuration script should do that for you. 

* pyinstaller gui_main.py --onefile

## Running 

### Windows 

Right click on `gui_main.exe` and run as administrator.

### Linux

`bazel run utils/gui` or `./gui_main` wherever that file is located.

### Mac

`./gui_main` wherever that file is located.

## Considerations
* Between runs you will need to kill `denarii_wallet_rpc_server` sometimes because it can get orphaned on Linux. But if you re-run it will just work so you don't *have* to kill it.
* On Windows `denariid.exe` will fail to connect to the network and will be auto restarted by the GUI so be patient before attempting to mine 
* There is currently no way beyond looking at the terminal to see how far along synchronization is.