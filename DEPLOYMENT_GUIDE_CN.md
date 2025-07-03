# Tiledesk 一站式智能客服平台 - 中文部署指南

## 1. 引言

本文档旨在为 Tiledesk 开源项目提供一份详尽的、从零开始的中文部署指南。Tiledesk 是一个功能强大的一站式智能客服平台，集成了在线聊天、对话机器人、工单系统和知识库。

本指南将采用官方推荐的 **Docker Compose** 方式进行部署，这是在您自己的服务器上运行 Tiledesk 的最简单、最可靠的方法。

**目标读者**: 希望私有化部署 Tiledesk 的开发者、运维工程师或 IT 管理员。
**最终目标**: 在您的服务器上成功运行一个功能完整的 Tiledesk 实例，并了解如何进行基础配置和管理。

---

## 2. 环境与系统要求

在开始之前，请确保您的服务器满足以下最低要求：

*   **操作系统**: 一个支持 Docker 的现代 Linux 发行版 (例如 Ubuntu 20.04+ / Debian 10+ / CentOS 7+)。
*   **CPU**: 至少 **2 核** CPU。
*   **内存 (RAM)**: 至少 **4 GB** 内存。
*   **存储**: 至少 **20 GB** 可用磁盘空间。
*   **软件**:
    *   **Docker**: 最新稳定版。
    *   **Docker Compose**: 最新稳定版 (v2.x+)。
    *   **Git**: 用于克隆仓库。

---

## 3. 部署步骤

我们将按照以下步骤完成部署：

1.  克隆您的 Tiledesk 仓库。
2.  配置必要的环境变量。
3.  使用 Docker Compose 启动所有服务。
4.  进行首次运行的初始化配置。

### 步骤 3.1: 克隆仓库与准备文件

首先，通过 SSH 或 HTTPS 克隆您 fork 的 Tiledesk 仓库到您的服务器上。

```bash
# 切换到您希望安装 Tiledesk 的目录
cd /opt

# 克隆您的仓库
git clone https://github.com/unkaku-1/tiledesk.git

# 进入 docker-compose 目录
# 这是所有部署文件的所在地
cd tiledesk/docker-compose/
```

现在，您需要从官方示例创建一个 `.env` 文件，这个文件将掌管 Tiledesk 的所有关键配置。

```bash
# 复制 .env.sample 文件为 .env
cp .env.sample .env
```

### 步骤 3.2: 配置环境变量 (`.env` 文件)

使用您喜欢的文本编辑器（如 `nano` 或 `vim`）打开刚刚创建的 `.env` 文件。

```bash
nano .env
```

您需要关注并修改以下**核心配置项**：

#### **A. 基础配置 (必须修改)**

*   `BASE_URL`: **极其重要**。将其修改为您服务器的**公网 IP 地址**或**域名**。所有服务都将依赖这个地址进行通信。
    *   示例 (使用 IP): `BASE_URL=http://159.89.204.13`
    *   示例 (使用域名): `BASE_URL=https://support.yourcompany.com`

*   `MONGODB_URI`: MongoDB 的连接地址。**通常无需修改**，因为 Docker Compose 会自动处理。
    *   默认值: `MONGODB_URI=mongodb://mongodb:27017/tiledesk`

*   `GLOBAL_SECRET`: 用于生成和验证 JWT (JSON Web Tokens) 的全局密钥。请务_**务必**_将其修改为一个**长且随机的字符串**，以确保安全。
    *   您可以使用以下命令生成一个随机密钥：
        ```bash
        # 在终端中运行此命令，并将输出结果粘贴到 .env 文件中
        openssl rand -base64 32
        ```
    *   示例: `GLOBAL_SECRET=aVeryStrongAndRandomSecretKeyGeneratedByOpenSSL`

#### **B. 邮件服务配置 (强烈建议配置)**

Tiledesk 需要邮件服务来发送用户邀请、密码重置和通知。

*   `EMAIL_ENABLED`: 设为 `true` 来启用邮件功能。
    *   `EMAIL_ENABLED=true`

*   `EMAIL_HOST`: 您的 SMTP 服务器地址。
    *   示例: `EMAIL_HOST=smtp.your-email-provider.com`

*   `EMAIL_PORT`: 您的 SMTP 端口 (通常是 `587` 或 `465`)。

*   `EMAIL_USERNAME`: 您的 SMTP 用户名。

*   `EMAIL_PASSWORD`: 您的 SMTP 密码。

*   `EMAIL_FROM_ADDRESS`: 您希望邮件显示的发件人地址。
    *   示例: `EMAIL_FROM_ADDRESS=no-reply@yourcompany.com`

#### **C. 初始管理���账户 (可选)**

您可以预设第一个管理员账户的凭据。

*   `ADMIN_EMAIL`: 初始管理员的邮箱地址。
    *   默认: `ADMIN_EMAIL=admin@tiledesk.com`

*   `ADMIN_PASSWORD`: 初始管理员的密码。
    *   默认: `ADMIN_PASSWORD=adminadmin`

**完成修改后，请保存并关闭 `.env` 文件。**

### 步骤 3.3: 启动 Tiledesk 服务

现在，一切准备就绪。在 `tiledesk/docker-compose/` 目录下，执行以下命令来构建并启动所有 Tiledesk 服务。

```bash
# --build 参数会确保根据最新代码构建镜像
# -d 参数会让服务在后台运行
sudo docker compose up --build -d
```

这个过程可能需要 5 到 15 分钟，因为它会下载所有必需的 Docker 镜像（MongoDB, RabbitMQ, Node.js 应用等）并构建 Tiledesk 的服务。

**如何检查服务状态？**

运行以下命令来查看所有容器是否都已正常启动并处于 `running` 状态：

```bash
sudo docker compose ps
```

您应该能看到类似 `tiledesk-server`, `tiledesk-dashboard`, `tiledesk-mongodb` 等多个服务。

### 步骤 3.4: 初始化与首次登录

服务启动后，您就可以通过浏览器访问 Tiledesk 了。

1.  **访问控制台**:
    *   打开浏览器，输入您在 `.env` 文件中配置的 `BASE_URL`。
    *   例如: `http://159.89.204.13` �� `https://support.yourcompany.com`。

2.  **创建您的第一个项目**:
    *   首次访问时，系统会引导您创建一个新的项目。请跟随向导完成项目创建。

3.  **登录**:
    *   使用您在 `.env` 文件中配置的管理员邮箱和密码 (`ADMIN_EMAIL`, `ADMIN_PASSWORD`) 登录系统。

**恭喜！您已经成功部署了属于您自己的 Tiledesk 实例！**

---

## 4. 常用管理命令

所有管理命令都应在 `tiledesk/docker-compose/` 目录下执行。

*   **查看所有服务日志**:
    ```bash
    sudo docker compose logs -f
    ```

*   **查看特定服务的日志** (例如 `tiledesk-server`):
    ```bash
    sudo docker compose logs -f tiledesk-server
    ```

*   **停止所有服务**:
    ```bash
    sudo docker compose down
    ```

*   **重启所有服务**:
    ```bash
    sudo docker compose restart
    ```

*   **更新 Tiledesk 版本**:
    ```bash
    # 1. 从您的 Git 仓库拉取最新代码
    git pull

    # 2. 重新构建并启动服务
    sudo docker compose up --build -d
    ```

---

## 5. 故障排查

*   **问题: 容器无法启动或反复重启。**
    *   **解决方案**: 使用 `sudo docker compose logs -f <service_name>` 查看具体服务的日志，找到错误原因。最常见的原因是 `.env` 文件���置错误（例如 `BASE_URL` 不正确）或端口冲突。

*   **问题: 访问 `BASE_URL` 显示 "502 Bad Gateway"。**
    *   **解决方案**: 这通常意味着后端的 `tiledesk-server` 服务没有正常启动。请检查其日志。也可能是 `tiledesk-proxy` (Nginx) 无法连接到后端服务，请检查 Docker 网络配置。

*   **问题: 忘记管理员密码。**
    *   **解决方案**: 您可以在 `.env` 文件中重新设置 `ADMIN_EMAIL` 和 `ADMIN_PASSWORD`，然后重启 Tiledesk 服务 (`sudo docker compose restart tiledesk-server`)。

希望这份指南能帮助您顺利完成 Tiledesk 的部署！
