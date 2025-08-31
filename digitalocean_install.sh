#!/bin/bash
# DigitalOcean Installation Script
# Run this on your DigitalOcean droplet

set -e
echo "🚀 Installing ChatBot on DigitalOcean..."

# Update system
apt update && apt upgrade -y

# Install essential packages
apt install -y python3 python3-pip python3-venv git curl htop ufw

# Install Ollama
echo "📦 Installing Ollama..."
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
systemctl start ollama
systemctl enable ollama

# Create a dedicated user for the chatbot (security best practice)
useradd -m -s /bin/bash chatbot
usermod -aG sudo chatbot

# Switch to chatbot user and set up application
sudo -u chatbot bash << 'EOF'
cd /home/chatbot

# Clone repository
git clone https://github.com/aneesomar/CVchatbot.git
cd CVchatbot

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Download AI model (this takes a few minutes)
echo "🧠 Downloading AI model..."
ollama pull llama3.2:1b

echo "✅ Application setup complete!"
EOF

# Create systemd service
cat > /etc/systemd/system/chatbot.service << 'EOF'
[Unit]
Description=ChatBot Streamlit Application
After=network.target ollama.service
Wants=ollama.service

[Service]
Type=simple
User=chatbot
Group=chatbot
WorkingDirectory=/home/chatbot/CVchatbot
Environment=PATH=/home/chatbot/CVchatbot/venv/bin
Environment=PYTHONPATH=/home/chatbot/CVchatbot
ExecStart=/home/chatbot/CVchatbot/venv/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true --logger.level=error
Restart=always
RestartSec=10
StandardOutput=syslog
StandardError=syslog

[Install]
WantedBy=multi-user.target
EOF

# Configure firewall
ufw allow ssh
ufw allow 8501/tcp
ufw --force enable

# Start and enable chatbot service
systemctl daemon-reload
systemctl enable chatbot.service
systemctl start chatbot.service

# Get public IP
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com)

echo ""
echo "🎉 Installation Complete!"
echo "========================="
echo ""
echo "Your ChatBot is now running at:"
echo "🌍 http://$PUBLIC_IP:8501"
echo ""
echo "Service Status:"
systemctl status chatbot.service --no-pager -l
echo ""
echo "📊 Useful Commands:"
echo "• Check status: systemctl status chatbot"
echo "• View logs: journalctl -u chatbot -f"
echo "• Restart: systemctl restart chatbot"
echo ""
echo "🔧 Server Info:"
echo "• OS: $(lsb_release -d | cut -f2)"
echo "• Memory: $(free -h | grep Mem | awk '{print $2}')"
echo "• Disk: $(df -h / | tail -1 | awk '{print $2}')"
echo ""
echo "💡 Your chatbot will automatically start on server reboot!"
