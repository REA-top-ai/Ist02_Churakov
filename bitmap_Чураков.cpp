#include <filesystem>
#include <fstream>
#include <iostream>

static bool load_file_bytes(const char* path, unsigned char* headers,
const int size) {
    std::ifstream file(path, std::ios::binary);
    if (!file) {
        return false;
    }
    file.read(reinterpret_cast<char*>(headers), size);
    return true;
}

int main(const int argc, char** argv) {
    const char* path = argc > 1 ? argv[1] : "/Users/ivan/Downloads/images/lena.bmp";

    unsigned char buffer[54] {};

    if (!load_file_bytes(path, buffer, 54)) {
        printf("Failed to load file \n: %s",path);
    }
    bool check_signature = (buffer[0] == 'B' && buffer[1] == 'M');
    if (!check_signature) {
        printf("Failed to load file \n: %s",path);
    }
    int *file_size = (int*)(buffer+2);
    int *reserved = (int*)(buffer+6);
    int *dataoffset = (int*)(buffer+10);
    int *size = (int*)(buffer+14);
    int *width = (int*)(buffer+18);
    int *height = (int*)(buffer+22);
    short *planes = (short*)(buffer+26);
    short *bitcount = (short*)(buffer+28);
    int *compression = (int*)(buffer+30);
    int *imagesize = (int*)(buffer+34);
    int *xpixelsperm = (int*)(buffer+38);
    int *ypixelsperm = (int*)(buffer+42);
    int *colorsused = (int*)(buffer+46);
    int *colorsimportant = (int*)(buffer+50);
    std::cout << *file_size       << ' '
              << *reserved        << ' '
              << *dataoffset      << ' '
              << *size            << ' '
              << *width           << ' '
              << *height          << ' '
              << *planes          << ' '
              << *bitcount        << ' '
              << *compression     << ' '
              << *imagesize       << ' '
              << *xpixelsperm     << ' '
              << *ypixelsperm     << ' '
              << *colorsused      << ' '
              << *colorsimportant << std::endl;
    return 0;
}