pip install osascript
sudo cp ancyterm.py /usr/local/bin/ancyterm && sudo chmod +x /usr/local/bin/ancyterm
sudo cp backend.py /usr/local/bin/backend && sudo chmod +x /usr/local/bin/backend
sudo cp iTerm2_Backend.py /usr/local/bin/iTerm2_Backend && sudo chmod +x /usr/local/bin/iTerm2_Backend
echo '[context]' >> ~/.pwn.conf
echo 'terminal=["ancyterm","-e"]' >> ~/.pwn.conf
echo "[Unit]
Description=Backend Service
After=network.target

[Service]
Type=simple
User=`whoami`
ExecStart=/usr/local/bin/backend
Restart=on-failure

[Install]
WantedBy=multi-user.target" > ./backend.service
sudo cp ./backend.service /etc/systemd/system/
sudo systemctl enable backend.service