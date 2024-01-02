#!/bin/bash
#######################
# Autor: Marcilio Ramos
# Data: 28.12.2023
# Versão: 1.0
# Finalidade: Configuração do ambiente para prover a api do wpp
########################


# ATUALIZANDO O S.O E INSTALANDO DEPENDÊNCIAS
sudo apt update
sudo apt upgrade -y
sudo apt -y install npm curl dirmngr apt-transport-https lsb-release ca-certificates wget
curl -sL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt -y install nodejs
sudo apt install -y libgbm-dev unzip fontconfig locales gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils libxss-dev libappindicator1 libu2f-udev

# INSTALANDO O CHROME
wget -c https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f
sudo apt update 

# INSTALANDO E INICIANDO O WPP CONNECT
cd ~ || exit
git clone https://github.com/wppconnect-team/wppconnect-server.git
cd wppconnect-server || exit
npm install
npm run build
sudo npm install -g pm2
pm2 start npm --name wpp -- start

# CONFIGURANDO NGINX
sudo apt install nginx
sudo rm /etc/nginx/sites-enabled/default
sudo bash -c 'cat <<EOF > /etc/nginx/sites-available/wpp
server {
  server_name api.seudominioaqui.com.br;

  location / {
    proxy_pass http://127.0.0.1:21465;
    proxy_http_version 1.1;
    proxy_set_header Upgrade \$http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_set_header Host \$host;
    proxy_set_header X-Real-IP \$remote_addr;
    proxy_set_header X-Forwarded-Proto \$scheme;
    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    proxy_cache_bypass \$http_upgrade;
  }
}
EOF'

sudo ln -s /etc/nginx/sites-available/wpp /etc/nginx/sites-enabled 
sudo nginx -t
sudo service nginx restart


# ABRINDO PORTAS NO FIREWALL
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo service ufw restart

# INSTALANDO SNAP E CERTBOT (OPCIONAL)
#sudo apt install snapd
#sudo snap install notes


#read -p "Deseja instalar o Certbot para configuração do SSL? (s/n): " install_certbot

#if [ "$install_certbot" = "s" ]; then
#    sudo snap install --classic certbot
#    show_progress
#    # PROSSEGUINDO COM O CERTBOT (SUBSTITUA "seudominioaqui.com.br" PELO SEU DOMÍNIO)
#    sudo certbot --nginx -d api.seudominioaqui.com.br
#fi
