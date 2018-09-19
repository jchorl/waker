# Waker

## Set up the memory card
```bash
sudo dd if=Armbian_5.38_Orangepizero_Debian_stretch_next_4.14.14.img of=/dev/sdb
```

## Initial Setup
```bash
ssh root@ip
```

## Update
```bash
sudo apt-get update; sudo apt-get upgrade
```

## Enable audio
```bash
sudo armbian-config
```
Add overlays=analog-codec in System > BootEnv

## Install Docker
```bash
sudo armbian-config
```
Software > Softy > Docker

## Get waker running
```bash
make img-build
make prod
```

## Install Raspotify
```bash
curl -sL https://dtcooper.github.io/raspotify/install.sh > install_raspotify.sh
chmod +x install_raspotify.sh
# remove the rpi check
./install_raspotify.sh
sudo vim /etc/default/raspotify
```
