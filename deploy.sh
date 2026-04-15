sudo apt update
sudo apt upgrade -y
sudo apt install -y git docker.io docker-compose-v2
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER
newgrp docker

git clone https://github.com/FerGem33/Noona-s-Backend.git
cd Noona-s-Backend/

docker compose -f docker-compose.prod.yml up -d --build
