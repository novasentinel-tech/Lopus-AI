#include "lopus_native/system.hpp"

#include <stdexcept>
#include <string>
#include <vector>

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

bool click_mouse(const std::string& button) {
#ifdef _WIN32
    DWORD down_flag = 0;
    DWORD up_flag = 0;
    if (button == "left") {
        down_flag = MOUSEEVENTF_LEFTDOWN;
        up_flag = MOUSEEVENTF_LEFTUP;
    } else if (button == "right") {
        down_flag = MOUSEEVENTF_RIGHTDOWN;
        up_flag = MOUSEEVENTF_RIGHTUP;
    } else if (button == "middle") {
        down_flag = MOUSEEVENTF_MIDDLEDOWN;
        up_flag = MOUSEEVENTF_MIDDLEUP;
    } else {
        throw std::invalid_argument("Botão do mouse inválido: use left, right ou middle.");
    }

    INPUT inputs[2]{};
    inputs[0].type = INPUT_MOUSE;
    inputs[0].mi.dwFlags = down_flag;
    inputs[1].type = INPUT_MOUSE;
    inputs[1].mi.dwFlags = up_flag;

    const UINT sent = ::SendInput(2, inputs, sizeof(INPUT));
    if (sent != 2) {
        throw std::runtime_error("SendInput falhou ao executar o clique do mouse.");
    }
    return true;
#else
    (void)button;
    throw std::runtime_error(
        "Clique nativo ainda está disponível apenas no Windows."
    );
#endif
}

bool type_text_utf8(const std::string& text) {
#ifdef _WIN32
    if (text.empty()) {
        return true;
    }

    const int wide_length = ::MultiByteToWideChar(
        CP_UTF8,
        MB_ERR_INVALID_CHARS,
        text.data(),
        static_cast<int>(text.size()),
        nullptr,
        0
    );
    if (wide_length <= 0) {
        throw std::runtime_error("Falha ao converter texto UTF-8 para UTF-16.");
    }

    std::wstring wide_text(static_cast<std::size_t>(wide_length), L'\0');
    if (::MultiByteToWideChar(
            CP_UTF8,
            MB_ERR_INVALID_CHARS,
            text.data(),
            static_cast<int>(text.size()),
            wide_text.data(),
            wide_length
        ) <= 0) {
        throw std::runtime_error("Falha ao converter texto UTF-8 para UTF-16.");
    }

    std::vector<INPUT> inputs;
    inputs.reserve(wide_text.size() * 2);
    for (const wchar_t unit : wide_text) {
        INPUT down{};
        down.type = INPUT_KEYBOARD;
        down.ki.wScan = static_cast<WORD>(unit);
        down.ki.dwFlags = KEYEVENTF_UNICODE;

        INPUT up = down;
        up.ki.dwFlags = KEYEVENTF_UNICODE | KEYEVENTF_KEYUP;
        inputs.push_back(down);
        inputs.push_back(up);
    }

    const UINT expected = static_cast<UINT>(inputs.size());
    const UINT sent = ::SendInput(expected, inputs.data(), sizeof(INPUT));
    if (sent != expected) {
        throw std::runtime_error("SendInput falhou ao digitar texto Unicode.");
    }
    return true;
#else
    (void)text;
    throw std::runtime_error(
        "Digitação nativa ainda está disponível apenas no Windows."
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
