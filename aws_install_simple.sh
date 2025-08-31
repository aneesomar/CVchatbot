#!/bin/bash
# Simple AWS Installation Script - Copy and paste this on your AWS server

set -e  # Exit on any error

echo "🚀 Installing ChatBot on AWS EC2..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install packages
sudo apt install -y python3 python3-pip python3-venv git curl

# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh
sudo systemctl start ollama
sudo systemctl enable ollama

# Clone repository
git clone https://github.com/aneesomar/CVchatbot.git
cd CVchatbot

# Setup Python environment  
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Download AI model
ollama pull llama3.2:1b

# Create service file
sudo tee /etc/systemd/system/chatbot.service << 'EOF'
[Unit]
Description=ChatBot Streamlit App
After=network.target ollama.service
Wants=ollama.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/CVchatbot
Environment=PATH=/home/ubuntu/CVchatbot/venv/bin
ExecStart=/home/ubuntu/CVchatbot/venv/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Start services
sudo systemctl daemon-reload
sudo systemctl enable chatbot
sudo systemctl start chatbot

# Configure firewall
sudo ufw allow ssh
sudo ufw allow 8501
sudo ufw --force enable

echo ""
echo "✅ Installation complete!"
echo ""
echo "Your ChatBot URL:"
echo "http://$(curl -s http://checkip.amazonaws.com):8501"
echo ""
echo "Check status: sudo systemctl status chatbot"
