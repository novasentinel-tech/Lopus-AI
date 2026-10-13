#include "lopus_native/system.hpp"

#include <algorithm>
#include <cctype>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

#ifdef _WIN32
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#endif

namespace lopus_native {

#ifdef _WIN32
namespace {

std::string normalized_key_name(std::string key) {
    std::transform(
        key.begin(),
        key.end(),
        key.begin(),
        [](const unsigned char value) { return static_cast<char>(std::tolower(value)); }
    );
    return key;
}

WORD virtual_key_from_name(const std::string& raw_key) {
    const std::string key = normalized_key_name(raw_key);
    static const std::unordered_map<std::string, WORD> named_keys{
        {"ctrl", VK_CONTROL}, {"control", VK_CONTROL},
        {"shift", VK_SHIFT}, {"alt", VK_MENU},
        {"win", VK_LWIN}, {"windows", VK_LWIN}, {"meta", VK_LWIN},
        {"enter", VK_RETURN}, {"return", VK_RETURN},
        {"tab", VK_TAB}, {"escape", VK_ESCAPE}, {"esc", VK_ESCAPE},
        {"backspace", VK_BACK}, {"delete", VK_DELETE}, {"del", VK_DELETE},
        {"insert", VK_INSERT}, {"home", VK_HOME}, {"end", VK_END},
        {"pageup", VK_PRIOR}, {"pagedown", VK_NEXT},
        {"up", VK_UP}, {"down", VK_DOWN}, {"left", VK_LEFT}, {"right", VK_RIGHT},
        {"space", VK_SPACE},
    };

    const auto found = named_keys.find(key);
    if (found != named_keys.end()) {
        return found->second;
    }

    if (key.size() == 1) {
        const unsigned char value = static_cast<unsigned char>(key[0]);
        if (std::isalpha(value)) {
            return static_cast<WORD>(std::toupper(value));
        }
        if (std::isdigit(value)) {
            return static_cast<WORD>(value);
        }
    }

    if (key.size() >= 2 && key[0] == 'f') {
        try {
            const int number = std::stoi(key.substr(1));
            if (number >= 1 && number <= 24) {
                return static_cast<WORD>(VK_F1 + number - 1);
            }
        } catch (const std::exception&) {
            // cai no erro claro abaixo
        }
    }

    throw std::invalid_argument("Tecla não suportada pelo Native Core: " + raw_key);
}

INPUT make_key_input(const WORD virtual_key, const bool key_up) {
    INPUT input{};
    input.type = INPUT_KEYBOARD;
    input.ki.wVk = virtual_key;
    input.ki.dwFlags = key_up ? KEYEVENTF_KEYUP : 0;
    return input;
}

void send_inputs(std::vector<INPUT>& inputs, const char* error_message) {
    if (inputs.empty()) {
        return;
    }
    const UINT expected = static_cast<UINT>(inputs.size());
    const UINT sent = ::SendInput(expected, inputs.data(), sizeof(INPUT));
    if (sent != expected) {
        throw std::runtime_error(error_message);
    }
}

}  // namespace
#endif

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

    send_inputs(inputs, "SendInput falhou ao digitar texto Unicode.");
    return true;
#else
    (void)text;
    throw std::runtime_error(
        "Digitação nativa ainda está disponível apenas no Windows."
    );
#endif
}

bool press_key(const std::string& key) {
#ifdef _WIN32
    const WORD virtual_key = virtual_key_from_name(key);
    std::vector<INPUT> inputs{
        make_key_input(virtual_key, false),
        make_key_input(virtual_key, true),
    };
    send_inputs(inputs, "SendInput falhou ao pressionar a tecla.");
    return true;
#else
    (void)key;
    throw std::runtime_error(
        "Pressionamento nativo de teclas ainda está disponível apenas no Windows."
    );
#endif
}

bool hotkey(const std::vector<std::string>& keys) {
#ifdef _WIN32
    if (keys.size() < 2 || keys.size() > 5) {
        throw std::invalid_argument("Hotkey deve possuir entre 2 e 5 teclas.");
    }

    std::vector<WORD> virtual_keys;
    virtual_keys.reserve(keys.size());
    for (const auto& key : keys) {
        virtual_keys.push_back(virtual_key_from_name(key));
    }

    std::vector<INPUT> inputs;
    inputs.reserve(virtual_keys.size() * 2);
    for (const WORD virtual_key : virtual_keys) {
        inputs.push_back(make_key_input(virtual_key, false));
    }
    for (auto it = virtual_keys.rbegin(); it != virtual_keys.rend(); ++it) {
        inputs.push_back(make_key_input(*it, true));
    }

    send_inputs(inputs, "SendInput falhou ao executar a hotkey.");
    return true;
#else
    (void)keys;
    throw std::runtime_error(
        "Hotkeys nativas ainda estão disponíveis apenas no Windows."
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
