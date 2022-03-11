package(default_visibility = ["//visibility:public"])

py_library(
  name = "daemon",
  srcs = ["daemon.py"],
  deps = [":rpc"],
  imports = [":rpc"],
)

py_library(
  name = "wallet",
  srcs = ["wallet.py"],
  deps = [":rpc"],
  imports = [":rpc"]
)

py_library(
  name = "rpc",
  srcs = ["rpc.py"],
  deps = [],
  imports = [],
)