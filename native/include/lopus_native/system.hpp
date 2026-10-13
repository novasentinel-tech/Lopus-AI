#pragma once

#include <cstdint>
#include <string>
#include <utility>

namespace lopus_native {

std::string platform_name();
std::uint64_t process_id();

bool gui_input_supported();
std::pair<int, int> cursor_position();
bool move_cursor(int x, int y);
std::pair<int, int> primary_screen_size();

}  // namespace lopus_native
