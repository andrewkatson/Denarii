# Denariid GUI

## Running 

`bazel run utils/gui`

## Considerations

* You need to have a built `denariid` and a `denarii_wallet_rpc_server` in the same folder as `gui_main.py` if you want it to run properly.
* You need to either have a `denarii_client.py` or have `KeirosPublic` repo in your filesystem.
* Between runs you will need to kill `denarii_wallet_rpc_server` sometimes because it can get orphaned. But if you re-run it will just work so you don't *have* to kill it.