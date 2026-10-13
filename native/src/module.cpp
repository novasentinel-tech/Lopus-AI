#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "lopus_native/system.hpp"

namespace py = pybind11;

PYBIND11_MODULE(lopus_native, module) {
    module.doc() = "Backend C++ de baixo nível do Lopus-AI";
    module.attr("__version__") = "0.1.0";

    module.def(
        "platform_name",
        &lopus_native::platform_name,
        "Retorna a plataforma detectada pelo backend nativo."
    );
    module.def(
        "process_id",
        &lopus_native::process_id,
        "Retorna o PID do processo atual."
    );
    module.def(
        "gui_input_supported",
        &lopus_native::gui_input_supported,
        "Informa se as operações nativas de entrada gráfica estão disponíveis."
    );
    module.def(
        "cursor_position",
        &lopus_native::cursor_position,
        "Retorna a posição atual do cursor como (x, y)."
    );
    module.def(
        "move_cursor",
        &lopus_native::move_cursor,
        py::arg("x"),
        py::arg("y"),
        "Move o cursor do sistema para a coordenada informada."
    );
    module.def(
        "primary_screen_size",
        &lopus_native::primary_screen_size,
        "Retorna a resolução da tela principal como (largura, altura)."
    );
}
