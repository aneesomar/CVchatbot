#!/bin/bash
# DigitalOcean ChatBot Management Script
# Run this on your DigitalOcean server for maintenance

echo "🌊 DigitalOcean ChatBot Manager"
echo "==============================="

case "$1" in
    status)
        echo "📊 Service Status:"
        systemctl status chatbot.service
        echo ""
        echo "🔥 Resource Usage:"
        echo "Memory: $(free -h | grep Mem | awk '{print $3"/"$2}')"
        echo "Disk: $(df -h / | tail -1 | awk '{print $3"/"$2" ("$5" used)"}')"
        echo "CPU Load: $(uptime | awk -F'load average:' '{print $2}')"
        ;;
    
    logs)
        echo "📝 Real-time logs (Press Ctrl+C to exit):"
        journalctl -u chatbot.service -f
        ;;
    
    restart)
        echo "🔄 Restarting ChatBot..."
        systemctl restart chatbot.service
        sleep 3
        systemctl status chatbot.service --no-pager
        ;;
    
    update)
        echo "⬆️  Updating ChatBot..."
        sudo -u chatbot bash << 'EOF'
        cd /home/chatbot/CVchatbot
        git pull origin master
        source venv/bin/activate
        pip install -r requirements.txt --upgrade
EOF
        systemctl restart chatbot.service
        echo "✅ Update complete!"
        ;;
    
    backup)
        echo "💾 Creating backup..."
        DATE=$(date +%Y%m%d_%H%M%S)
        tar -czf /root/chatbot_backup_$DATE.tar.gz /home/chatbot/CVchatbot
        echo "✅ Backup saved as: /root/chatbot_backup_$DATE.tar.gz"
        ;;
    
    ssl)
        echo "🔒 Setting up SSL certificate..."
        apt install -y nginx certbot python3-certbot-nginx
        
        # Get domain name
        read -p "Enter your domain name (e.g., mychatbot.com): " DOMAIN
        
        # Configure Nginx
        cat > /etc/nginx/sites-available/chatbot << EOF
server {
    listen 80;
    server_name $DOMAIN;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF
        
        ln -sf /etc/nginx/sites-available/chatbot /etc/nginx/sites-enabled/
        nginx -t && systemctl reload nginx
        
        # Get SSL certificate
        certbot --nginx -d $DOMAIN
        
        echo "✅ SSL setup complete! Your site is now available at https://$DOMAIN"
        ;;
    
    *)
        echo "Usage: $0 {status|logs|restart|update|backup|ssl}"
        echo ""
        echo "Commands:"
        echo "  status   - Show service status and resource usage"
        echo "  logs     - View real-time application logs"
        echo "  restart  - Restart the chatbot service"
        echo "  update   - Update chatbot code from GitHub"
        echo "  backup   - Create backup of chatbot files"
        echo "  ssl      - Set up SSL certificate with custom domain"
        echo ""
        echo "Examples:"
        echo "  ./manage.sh status"
        echo "  ./manage.sh logs"
        echo "  ./manage.sh ssl"
        ;;
esac
