#!/bin/bash

# ================================================================================
# 英语文章高亮展示页 - 服务器端部署脚本（在服务器上运行）
# 功能：清理旧部署并配置nginx反向代理
# 注意：此脚本应在服务器上运行，frontend 文件夹已存在于服务器上
# 服务器IP: 106.13.190.227
# 服务器端口: 8097
# 部署目录: /srv/users/lyktt/highlight_words_display/
# ================================================================================

# 设置错误处理：遇到错误立即退出
set -e

# 配置变量
SERVER_PORT="8097"
PROJECT_NAME="highlight_words_display"
DEPLOY_BASE_PATH="/srv/users/lyktt"
DEPLOY_PATH="${DEPLOY_BASE_PATH}/${PROJECT_NAME}"
FRONTEND_PATH="${DEPLOY_PATH}/frontend"
NGINX_CONFIG_FILE="/etc/nginx/sites-available/${PROJECT_NAME}"
NGINX_ENABLED_FILE="/etc/nginx/sites-enabled/${PROJECT_NAME}"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 日志函数
log_info() {
    echo -e "${GREEN}[✓ INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[⚠ WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗ ERROR]${NC} $1"
}

log_title() {
    echo -e "${BLUE}========== $1 ==========${NC}"
}

# ================================================================================
# 第一步：验证环境
# ================================================================================
log_title "开始部署流程"
log_info "服务器端口: ${SERVER_PORT}"
log_info "部署路径: ${DEPLOY_PATH}"
log_info "前端目录: ${FRONTEND_PATH}"
echo ""

# 检查frontend目录是否存在
log_info "检查前端目录..."
if [ ! -d "${FRONTEND_PATH}" ]; then
    log_error "前端目录不存在: ${FRONTEND_PATH}"
    log_info "当前部署路径内容："
    ls -la "${DEPLOY_PATH}/" || echo "部署路径不存在"
    exit 1
else
    log_info "前端目录验证成功"
    # 统计前端文件
    frontend_files=$(find "${FRONTEND_PATH}" -type f 2>/dev/null | wc -l)
    log_info "检测到 $frontend_files 个前端文件"
fi
echo ""

# 检查Nginx是否已安装
log_info "检查Nginx安装状态..."
if ! command -v nginx &> /dev/null; then
    log_error "Nginx未安装"
    log_info "请先安装Nginx: sudo apt-get update && sudo apt-get install -y nginx"
    exit 1
fi
log_info "Nginx已安装"
echo ""

# ================================================================================
# 第二步：设置文件权限
# ================================================================================
log_title "设置文件权限"

log_info "设置前端目录权限..."
sudo chown -R www-data:www-data "${FRONTEND_PATH}"
sudo chmod -R 755 "${FRONTEND_PATH}"
sudo chmod 755 "${DEPLOY_PATH}"
sudo chmod 755 "${DEPLOY_BASE_PATH}"

log_info "文件权限设置完成"
echo ""

# ================================================================================
# 第三步：配置Nginx反向代理
# ================================================================================
log_title "配置Nginx反向代理"

# 生成Nginx配置文件内容
read -r -d '' NGINX_CONFIG << 'EOF' || true
# ================================================================================
# Nginx配置 - 英语文章高亮展示页
# 服务器: 106.13.190.227:8097
# ================================================================================

server {
    listen 8097;
    listen [::]:8097;

    server_name 106.13.190.227;

    # 设置根目录
    root /srv/users/lyktt/highlight_words_display/frontend;
    index class-article.html index.html index.htm;

    # 访问日志
    access_log /var/log/nginx/highlight_words_display_access.log;
    error_log /var/log/nginx/highlight_words_display_error.log;

    # 前端静态文件服务
    location / {
        # 尝试访问请求的文件，如果不存在则返回class-article.html（用于SPA应用）
        try_files $uri $uri/ /class-article.html;

        # 缓存配置
        expires 1d;
        add_header Cache-Control "public, max-age=86400";
    }

    # 静态资源缓存配置（长期缓存）
    location ~* \.(css|js|jpg|jpeg|png|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 30d;
        add_header Cache-Control "public, max-age=2592000, immutable";
        access_log off;
    }

    # JSON数据文件缓存
    location ~* \.json$ {
        expires 1h;
        add_header Cache-Control "public, max-age=3600";
        add_header Access-Control-Allow-Origin "*";
    }

    # CSV数据文件缓存
    location ~* \.csv$ {
        expires 1h;
        add_header Cache-Control "public, max-age=3600";
        add_header Access-Control-Allow-Origin "*";
    }

    # 拒绝访问隐藏文件和备份文件
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }

    location ~ ~$ {
        deny all;
        access_log off;
        log_not_found off;
    }
}
EOF

log_info "生成Nginx配置，准备上传到服务器..."

# 移除已存在的链接（如果有）
if [ -L "${NGINX_ENABLED_FILE}" ]; then
    log_info "删除已存在的符号链接..."
    sudo rm -f "${NGINX_ENABLED_FILE}"
fi

# 创建Nginx配置
log_info "创建Nginx配置文件..."
sudo bash -c "cat > ${NGINX_CONFIG_FILE}" << 'EOF'
# ================================================================================
# Nginx配置 - 英语文章高亮展示页
# 服务器: 106.13.190.227:8097
# ================================================================================

server {
    listen 8097;
    listen [::]:8097;

    server_name 106.13.190.227;

    # 设置根目录
    root /srv/users/lyktt/highlight_words_display/frontend;
    index class-article.html index.html index.htm;

    # 访问日志
    access_log /var/log/nginx/highlight_words_display_access.log;
    error_log /var/log/nginx/highlight_words_display_error.log;

    # 前端静态文件服务
    location / {
        # 尝试访问请求的文件，如果不存在则返回class-article.html（用于SPA应用）
        try_files $uri $uri/ /class-article.html;

        # 缓存配置
        expires 1d;
        add_header Cache-Control "public, max-age=86400";
    }

    # 静态资源缓存配置（长期缓存）
    location ~* \.(css|js|jpg|jpeg|png|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 30d;
        add_header Cache-Control "public, max-age=2592000, immutable";
        access_log off;
    }

    # JSON数据文件缓存
    location ~* \.json$ {
        expires 1h;
        add_header Cache-Control "public, max-age=3600";
        add_header Access-Control-Allow-Origin "*";
    }

    # CSV数据文件缓存
    location ~* \.csv$ {
        expires 1h;
        add_header Cache-Control "public, max-age=3600";
        add_header Access-Control-Allow-Origin "*";
    }

    # 拒绝访问隐藏文件和备份文件
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }

    location ~ ~$ {
        deny all;
        access_log off;
        log_not_found off;
    }
}
EOF

log_info "Nginx配置文件已创建"

# 检查sites-enabled目录
if [ ! -d /etc/nginx/sites-enabled ]; then
    log_info "创建sites-enabled目录..."
    sudo mkdir -p /etc/nginx/sites-enabled
fi

# 创建符号链接
log_info "创建符号链接..."
sudo ln -s "${NGINX_CONFIG_FILE}" "${NGINX_ENABLED_FILE}"

log_info "检查Nginx配置语法..."
if sudo nginx -t 2>&1; then
    log_info "Nginx配置验证成功"
else
    log_error "Nginx配置验证失败"
    exit 1
fi
echo ""

# ================================================================================
# 第四步：重启Nginx服务
# ================================================================================
log_title "重启Nginx服务"

log_info "重启Nginx服务..."
sudo systemctl restart nginx

# 等待服务启动
sleep 2

# 检查Nginx状态
if sudo systemctl is-active --quiet nginx; then
    log_info "Nginx已成功重启并运行中"
else
    log_error "Nginx启动失败"
    exit 1
fi

# 验证Nginx进程
if ps aux | grep -q "[n]ginx"; then
    log_info "Nginx进程已启动"
fi
echo ""

# ================================================================================
# 第五步：验证部署
# ================================================================================
log_title "验证部署"

echo "验证前端文件..."

# 统计前端文件
files_count=$(find "${FRONTEND_PATH}" -type f 2>/dev/null | wc -l)
echo "✓ 前端目录包含 $files_count 个文件"

# 验证关键文件
if [ -f "${FRONTEND_PATH}/class-article.html" ]; then
    echo "✓ 主页面文件 (class-article.html) 存在"
else
    echo "⚠️  警告：主页面文件不存在"
fi

if [ -d "${FRONTEND_PATH}/styles" ]; then
    echo "✓ 样式目录存在"
fi

# 验证Nginx配置
echo ""
echo "验证Nginx配置..."

if [ -f "${NGINX_CONFIG_FILE}" ]; then
    echo "✓ Nginx配置文件存在"
else
    echo "✗ Nginx配置文件不存在"
    exit 1
fi

if [ -L "${NGINX_ENABLED_FILE}" ]; then
    echo "✓ Nginx已启用站点配置"
else
    echo "⚠️  Nginx站点配置未启用"
fi

# 检查8097端口
echo ""
echo "检查服务端口..."
if ss -tuln 2>/dev/null | grep -q ":8097" || netstat -tuln 2>/dev/null | grep -q ":8097"; then
    echo "✓ 端口8097已监听"
else
    echo "⚠️  端口8097未监听，可能需要检查防火墙"
fi

echo ""
log_info "部署验证完成"
echo ""

# ================================================================================
# 第六步：部署完成总结
# ================================================================================
log_title "部署完成"
echo ""
echo "✓✓✓ 部署完成 ✓✓✓"
echo ""
echo "📍 服务访问地址："
echo "   http://106.13.190.227:${SERVER_PORT}"
echo ""
echo "📂 部署信息："
echo "   前端路径: ${FRONTEND_PATH}"
echo "   Nginx配置: ${NGINX_CONFIG_FILE}"
echo "   Nginx启用: ${NGINX_ENABLED_FILE}"
echo ""
echo "🔧 常用命令："
echo "   1. 查看实时访问日志:"
echo "      tail -f /var/log/nginx/highlight_words_display_access.log"
echo ""
echo "   2. 查看错误日志:"
echo "      tail -f /var/log/nginx/highlight_words_display_error.log"
echo ""
echo "   3. 重启Nginx服务:"
echo "      sudo systemctl restart nginx"
echo ""
echo "   4. 检查Nginx状态:"
echo "      sudo systemctl status nginx"
echo ""
echo "   5. 测试Nginx配置:"
echo "      sudo nginx -t"
echo ""
echo "   6. 查看前端文件:"
echo "      ls -lah ${FRONTEND_PATH}"
echo ""
echo "💡 提示："
echo "   - 首次访问可能需要等待缓存加载"
echo "   - 静态资源会被缓存30天，如需更新请清除浏览器缓存"
echo "   - 遇到403错误表示目录权限问题"
echo ""
echo "=========================================="
echo "✓ 部署脚本执行完成！"
echo "=========================================="
