# serProg
serT 固件下载烧写客户端示例, 依赖esptool工具

serProg 是一个使用python便携的命令行工具, 用于serT的烧写, 用户也可以简单修改后,用于其他平台esp8266/esp8285芯片的烧写.

主要功能:
1. 从云端下载最新固件及校验.
2. 向导式生成serT使用的配置文件config.json.
3. 将固件与配置文件烧入芯片.
