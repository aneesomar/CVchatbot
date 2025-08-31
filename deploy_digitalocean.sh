#!/bin/bash
# DigitalOcean Deployment Script for ChatBot
# Creates a $4/month Ubuntu server that runs 24/7

echo "🌊 DigitalOcean Deployment Guide"
echo "================================"
echo ""
echo "1. Create Account:"
echo "   → Go to https://digitalocean.com"
echo "   → Sign up (get $200 credit with GitHub student pack)"
echo ""
echo "2. Create Droplet:"
echo "   → Choose Ubuntu 22.04"
echo "   → Select 'Basic' plan"
echo "   → $4/month (1GB RAM, 25GB SSD)"
echo "   → Choose datacenter near you"
echo ""
echo "3. Connect via SSH:"
echo "   → ssh root@YOUR_SERVER_IP"
echo ""
echo "4. Run this installation:"

cat << 'EOF'
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv git curl -y

# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Clone your repository
git clone https://github.com/aneesomar/CVchatbot.git
cd CVchatbot

# Set up Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Download LLM model
ollama pull llama3.2:1b

# Create systemd service for auto-start
sudo tee /etc/systemd/system/chatbot.service << 'SERVICE'
[Unit]
Description=ChatBot Streamlit App
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/CVchatbot
Environment=PATH=/root/CVchatbot/venv/bin
ExecStart=/root/CVchatbot/venv/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true
Restart=always

[Install]
WantedBy=multi-user.target
SERVICE

# Start and enable service
sudo systemctl daemon-reload
sudo systemctl enable chatbot
sudo systemctl start chatbot

# Configure firewall
sudo ufw allow 22
sudo ufw allow 8501
sudo ufw --force enable

echo "✅ ChatBot is now running at http://YOUR_SERVER_IP:8501"
EOF

echo ""
echo "5. Access Your ChatBot:"
echo "   → http://YOUR_SERVER_IP:8501"
echo "   → Available 24/7 without Ngrok!"
echo ""
echo "6. Optional - Add Custom Domain:"
echo "   → Point your domain to server IP"
echo "   → Set up SSL with Let's Encrypt"
echo ""
echo "Monthly Cost: $4 (vs $0 but laptop must stay on)"
