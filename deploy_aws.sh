#!/bin/bash
# AWS EC2 Free Tier Deployment Guide for ChatBot
# 12 months FREE with new AWS account!

echo "☁️  AWS EC2 Free Tier ChatBot Deployment"
echo "========================================"
echo ""
echo "💰 AWS Free Tier Includes:"
echo "   → 750 hours/month EC2 t2.micro instance (12 months)"
echo "   → 1GB RAM, 1 vCPU, 8GB storage"
echo "   → Enough for your chatbot + Ollama!"
echo ""
echo "🚀 Step-by-Step Setup:"
echo ""

echo "STEP 1: Create AWS Account"
echo "-------------------------"
echo "→ Go to https://aws.amazon.com"
echo "→ Click 'Create AWS Account'"
echo "→ Use your email + credit card (won't be charged in free tier)"
echo "→ Verify phone number"
echo ""

echo "STEP 2: Launch EC2 Instance"
echo "---------------------------"
echo "→ Login to AWS Console"
echo "→ Go to EC2 Dashboard"
echo "→ Click 'Launch Instance'"
echo ""
echo "Configuration:"
echo "  • Name: ChatBot-Server"
echo "  • OS: Ubuntu Server 22.04 LTS (64-bit x86)"
echo "  • Instance Type: t2.micro (Free tier eligible)"
echo "  • Key Pair: Create new (download .pem file!)"
echo "  • Security Group: Allow SSH (22) + HTTP (80) + Custom (8501)"
echo "  • Storage: 8 GB gp2 (default - free)"
echo ""

echo "STEP 3: Connect to Your Server"
echo "------------------------------"
echo "After launch, note your PUBLIC IP address"
echo ""
echo "# Make key file secure"
echo "chmod 400 your-key.pem"
echo ""
echo "# Connect via SSH"
echo "ssh -i your-key.pem ubuntu@YOUR_PUBLIC_IP"
echo ""

echo "STEP 4: Install Everything (Run on AWS server)"
echo "----------------------------------------------"

# Create the complete installation script
cat << 'INSTALL_SCRIPT'

# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv git curl htop

# Install Ollama
echo "Installing Ollama..."
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
sudo systemctl start ollama
sudo systemctl enable ollama

# Clone your repository
echo "Cloning ChatBot repository..."
git clone https://github.com/aneesomar/CVchatbot.git
cd CVchatbot

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Download the LLM model (this takes a few minutes)
echo "Downloading AI model..."
ollama pull llama3.2:1b

# Create systemd service for auto-startup
sudo tee /etc/systemd/system/chatbot.service << 'EOF'
[Unit]
Description=ChatBot Streamlit Application
After=network.target ollama.service
Wants=ollama.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/CVchatbot
Environment=PATH=/home/ubuntu/CVchatbot/venv/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=/home/ubuntu/CVchatbot/venv/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true --logger.level=error
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and start services
sudo systemctl daemon-reload
sudo systemctl enable chatbot.service
sudo systemctl start chatbot.service

# Configure firewall
sudo ufw allow ssh
sudo ufw allow 8501
sudo ufw --force enable

# Show status
echo ""
echo "🎉 Installation Complete!"
echo "========================="
echo ""
echo "Your ChatBot is running at:"
echo "http://$(curl -s http://checkip.amazonaws.com):8501"
echo ""
echo "Service Status:"
sudo systemctl status chatbot.service --no-pager -l
echo ""
echo "To check logs:"
echo "sudo journalctl -u chatbot.service -f"

INSTALL_SCRIPT

echo ""
echo "STEP 5: Security Group Configuration"
echo "------------------------------------"
echo "In AWS Console → EC2 → Security Groups:"
echo "  • SSH (22): Your IP only"
echo "  • Custom TCP (8501): Anywhere (0.0.0.0/0)"
echo "  • Optional: HTTP (80) for future SSL setup"
echo ""

echo "STEP 6: Access Your ChatBot"
echo "---------------------------"
echo "After installation completes:"
echo "→ http://YOUR_AWS_PUBLIC_IP:8501"
echo "→ Available 24/7!"
echo "→ No laptop needed!"
echo ""

echo "💡 Pro Tips:"
echo "============"
echo "• AWS assigns new IP when you stop/start instance"
echo "• Use Elastic IP (free if attached) for fixed IP"
echo "• Monitor usage in AWS Billing Dashboard"
echo "• Instance auto-starts chatbot on boot"
echo ""

echo "📊 Free Tier Limits:"
echo "==================="
echo "• 750 hours/month EC2 usage (enough for 24/7)"
echo "• 15GB outbound data transfer"
echo "• Valid for 12 months from signup"
echo ""

echo "🔧 Management Commands:"
echo "======================"
echo "# Check chatbot status"
echo "sudo systemctl status chatbot"
echo ""
echo "# View logs"
echo "sudo journalctl -u chatbot -f"
echo ""
echo "# Restart chatbot"
echo "sudo systemctl restart chatbot"
echo ""
echo "# Stop instance (saves money)"
echo "# Go to EC2 Console → Stop Instance"
echo ""

echo "💰 After Free Tier (12 months):"
echo "==============================="
echo "t2.micro cost: ~$8.50/month"
echo "Still cheaper than most hosting platforms!"
echo ""

echo "🚀 Ready to deploy? Copy the installation script above!"
