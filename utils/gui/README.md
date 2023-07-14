# Denarii GUI

## Building 

The below assumes you have all the necessary files in one folder. The configuration script should do that for you. 

`pip3 install pyinstaller stripe pytest`

### Linux and Windows

`pyinstaller gui_main.py --onefile`

### Mac

`mkdir -p build/gui_main`

`pip3 uninstall pyinstaller` will give you information. look for this pattern `/Users/$USER/Library/Python/3.9/bin/pyinstaller`.

`/Users/$USER/Library/Python/3.9/bin/pyinstaller gui_main.py --onefile`


## Running 

### Flags

If you want to not start up the clients and use a testing client then don't pass any flags to the job. If you want real clients use `denarii_debug=False`.

### Windows 

`start dist/gui_main.exe --denarii_debug=False` and run the command prompt as administrator. Or wherever the file is located.

### Linux

`bazel run :gui -- --denarii_debug=False` or `./dist/gui_main --denarii_debug=False` or wherever that file is located.

### Mac

`./dist/gui_main --denarii_debug=False` or wherever that file is located.

## Considerations
* Between runs you will need to kill `denarii_wallet_rpc_server` sometimes because it can get orphaned on Linux. But if you re-run it will just work so you don't *have* to kill it.
* On Windows `denariid.exe` will fail to connect to the network and will be auto restarted by the GUI so be patient before attempting to mine 
* There is currently no way beyond looking at the terminal to see how far along synchronization is.