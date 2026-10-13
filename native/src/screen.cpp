#include "lopus_native/system.hpp"

#include <cstdint>
#include <cstring>
#include <stdexcept>
#include <vector>

#ifdef _WIN32
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#endif

namespace lopus_native {

bool screen_capture_supported() {
#ifdef _WIN32
    return true;
#else
    return false;
#endif
}

std::vector<std::uint8_t> capture_primary_screen_bmp() {
#ifdef _WIN32
    const int width = ::GetSystemMetrics(SM_CXSCREEN);
    const int height = ::GetSystemMetrics(SM_CYSCREEN);
    if (width <= 0 || height <= 0) {
        throw std::runtime_error("Não foi possível obter o tamanho da tela principal.");
    }

    HDC screen_dc = ::GetDC(nullptr);
    if (screen_dc == nullptr) {
        throw std::runtime_error("GetDC falhou ao capturar a tela.");
    }

    HDC memory_dc = ::CreateCompatibleDC(screen_dc);
    if (memory_dc == nullptr) {
        ::ReleaseDC(nullptr, screen_dc);
        throw std::runtime_error("CreateCompatibleDC falhou ao capturar a tela.");
    }

    HBITMAP bitmap = ::CreateCompatibleBitmap(screen_dc, width, height);
    if (bitmap == nullptr) {
        ::DeleteDC(memory_dc);
        ::ReleaseDC(nullptr, screen_dc);
        throw std::runtime_error("CreateCompatibleBitmap falhou ao capturar a tela.");
    }

    HGDIOBJ previous = ::SelectObject(memory_dc, bitmap);
    if (previous == nullptr || previous == HGDI_ERROR) {
        ::DeleteObject(bitmap);
        ::DeleteDC(memory_dc);
        ::ReleaseDC(nullptr, screen_dc);
        throw std::runtime_error("SelectObject falhou ao capturar a tela.");
    }

    const BOOL copied = ::BitBlt(
        memory_dc,
        0,
        0,
        width,
        height,
        screen_dc,
        0,
        0,
        SRCCOPY | CAPTUREBLT
    );
    if (!copied) {
        ::SelectObject(memory_dc, previous);
        ::DeleteObject(bitmap);
        ::DeleteDC(memory_dc);
        ::ReleaseDC(nullptr, screen_dc);
        throw std::runtime_error("BitBlt falhou ao capturar a tela.");
    }

    BITMAPINFO info{};
    info.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
    info.bmiHeader.biWidth = width;
    info.bmiHeader.biHeight = -height;  // top-down: coordenadas equivalem à tela
    info.bmiHeader.biPlanes = 1;
    info.bmiHeader.biBitCount = 32;
    info.bmiHeader.biCompression = BI_RGB;

    const std::size_t pixel_bytes =
        static_cast<std::size_t>(width) * static_cast<std::size_t>(height) * 4U;
    std::vector<std::uint8_t> pixels(pixel_bytes);

    const int rows = ::GetDIBits(
        memory_dc,
        bitmap,
        0,
        static_cast<UINT>(height),
        pixels.data(),
        &info,
        DIB_RGB_COLORS
    );

    ::SelectObject(memory_dc, previous);
    ::DeleteObject(bitmap);
    ::DeleteDC(memory_dc);
    ::ReleaseDC(nullptr, screen_dc);

    if (rows != height) {
        throw std::runtime_error("GetDIBits falhou ao extrair pixels da captura.");
    }

    BITMAPFILEHEADER file_header{};
    file_header.bfType = 0x4D42;  // BM
    file_header.bfOffBits = sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);
    file_header.bfSize = static_cast<DWORD>(file_header.bfOffBits + pixel_bytes);

    BITMAPINFOHEADER dib_header = info.bmiHeader;
    dib_header.biSizeImage = static_cast<DWORD>(pixel_bytes);

    std::vector<std::uint8_t> bmp(static_cast<std::size_t>(file_header.bfSize));
    std::memcpy(bmp.data(), &file_header, sizeof(file_header));
    std::memcpy(
        bmp.data() + sizeof(file_header),
        &dib_header,
        sizeof(dib_header)
    );
    std::memcpy(
        bmp.data() + file_header.bfOffBits,
        pixels.data(),
        pixel_bytes
    );
    return bmp;
#else
    throw std::runtime_error(
        "Captura nativa de tela ainda está disponível apenas no Windows."
    );
#endif
}

}  // namespace lopus_native
