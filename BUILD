package(default_visibility = ["//visibility:public"])

platform(
  name = "x64_windows-clang-cl",
  constraint_values = [
      "@platforms//cpu:x86_64",
      "@platforms//os:windows",
      "@bazel_tools//tools/cpp:clang-cl",
  ],
)

py_binary(
    name = "configure",
    srcs = ["configure.py"],
    imports = [":workspace_path_finder", ":common"],
    deps = [":workspace_path_finder", ":common"],
)

py_binary(
    name = "configure_win",
    srcs = ["configure_win.py"],
    imports = [":workspace_path_finder", ":common"],
    deps = [":workspace_path_finder", ":common"],
)

py_library(
  name = "workspace_path_finder",
  srcs = ["workspace_path_finder.py"],
  deps = [],
)

py_library(
  name = "common",
  srcs = ["common.py"],
  deps = []
)