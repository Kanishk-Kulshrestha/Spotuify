#include <iostream>
#include <cstring>
#include <unistd.h>
#include <arpa/inet.h>

int main() {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    sockaddr_in serv_addr{};
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(65432);
    inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr);

    if (connect(sock, (sockaddr*)&serv_addr, sizeof(serv_addr)) < 0) {
        std::cerr << "Connection failed\n";
        return 1;
    }

    while (true) {
        std::string msg;
        std::cout << "Enter message to Python: ";
        std::getline(std::cin, msg);

        send(sock, msg.c_str(), msg.length(), 0);

        char buffer[1024] = {0};
        int valread = read(sock, buffer, 1024);
        std::cout << "Python replied: " << buffer << std::endl;
    }

    close(sock);
    return 0;
}

