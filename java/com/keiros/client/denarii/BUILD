package(default_visibility = ["//visibility:public"])

java_library(
    name = "denarii_client",
    srcs = ["DenariiClient.java"],
    data = [
        "//client/Denarii:denarii_client_so",
    ],
    deps = [
        "//utils/gui:wallet_java_proto",
        "//java/com/keiros/tools/general/strings:hex",
        "@com_google_protobuf//:protobuf_java",
    ],
)
