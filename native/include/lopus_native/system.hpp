#pragma once

#include <cstdint>
#include <string>
#include <utility>
#include <vector>

namespace lopus_native {

std::string platform_name();
std::uint64_t process_id();

bool gui_input_supported();
std::pair<int, int> cursor_position();
bool move_cursor(int x, int y);
bool click_mouse(const std::string& button);
bool type_text_utf8(const std::string& text);
bool press_key(const std::string& key);
bool hotkey(const std::vector<std::string>& keys);
std::pair<int, int> primary_screen_size();

bool screen_capture_supported();
std::vector<std::uint8_t> capture_primary_screen_bmp();

}  // namespace lopus_native
