load("@com_github_grpc_grpc//bazel:python_rules.bzl", "py_proto_library")

package(default_visibility = ["//visibility:public"])

py_proto_library(
  name = "gui_user_py_proto",
  deps = [":gui_user_proto"],
)

proto_library(
  name = "gui_user_proto",
  srcs = ["gui_user.proto"],
  deps = ["@keiros_public//Proto:wallet_proto"],
)