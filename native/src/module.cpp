#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "lopus_native/system.hpp"

namespace py = pybind11;

PYBIND11_MODULE(lopus_native, module) {
    module.doc() = "Backend C++ de baixo nível do Lopus-AI";
    module.attr("__version__") = "0.2.0";

    module.def("platform_name", &lopus_native::platform_name);
    module.def("process_id", &lopus_native::process_id);
    module.def("gui_input_supported", &lopus_native::gui_input_supported);
    module.def("screen_capture_supported", &lopus_native::screen_capture_supported);
    module.def("cursor_position", &lopus_native::cursor_position);
    module.def("move_cursor", &lopus_native::move_cursor, py::arg("x"), py::arg("y"));
    module.def("click_mouse", &lopus_native::click_mouse, py::arg("button") = "left");
    module.def("type_text_utf8", &lopus_native::type_text_utf8, py::arg("text"));
    module.def("primary_screen_size", &lopus_native::primary_screen_size);
    module.def(
        "capture_primary_screen_bmp",
        []() {
            const auto bmp = lopus_native::capture_primary_screen_bmp();
            return py::bytes(
                reinterpret_cast<const char*>(bmp.data()),
                static_cast<py::ssize_t>(bmp.size())
            );
        },
        "Captura a tela principal e retorna um BMP codificado em bytes."
    );
}
