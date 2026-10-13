#include "lopus_native/system.hpp"

#include <stdexcept>

#ifdef _WIN32
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#endif

namespace lopus_native {

bool gui_input_supported() {
#ifdef _WIN32
    return true;
#else
    return false;
#endif
}

std::pair<int, int> cursor_position() {
#ifdef _WIN32
    POINT point{};
    if (!::GetCursorPos(&point)) {
        throw std::runtime_error("GetCursorPos falhou no backend nativo.");
    }
    return {static_cast<int>(point.x), static_cast<int>(point.y)};
#else
    throw std::runtime_error(
        "Leitura do cursor nativo ainda está disponível apenas no Windows."
    );
#endif
}

bool move_cursor(const int x, const int y) {
#ifdef _WIN32
    if (!::SetCursorPos(x, y)) {
        throw std::runtime_error("SetCursorPos falhou no backend nativo.");
    }
    return true;
#else
    (void)x;
    (void)y;
    throw std::runtime_error(
        "Movimento do cursor nativo ainda está disponível apenas no Windows."
    );
#endif
}

std::pair<int, int> primary_screen_size() {
#ifdef _WIN32
    const int width = ::GetSystemMetrics(SM_CXSCREEN);
    const int height = ::GetSystemMetrics(SM_CYSCREEN);
    if (width <= 0 || height <= 0) {
        throw std::runtime_error(
            "Não foi possível obter o tamanho da tela principal."
        );
    }
    return {width, height};
#else
    throw std::runtime_error(
        "Consulta de tela nativa ainda está disponível apenas no Windows."
    );
#endif
}

}  // namespace lopus_native
