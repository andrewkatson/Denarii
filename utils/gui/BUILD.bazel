package(default_visibility = ["//visibility:public"])

py_binary(
    name = "gui",
    srcs = ["gui_main.py"],
    deps = ["//:workspace_path_finder", "//utils/gui/Proto:gui_user_py_proto"],
    imports = ["//utils/gui/Proto:gui_user_py_proto",],
    main = "gui_main.py"
)