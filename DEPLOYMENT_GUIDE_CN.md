# Tiledesk 一站式智能客服平台 - 中文部署指南 (Windows 虚拟机版)

## 1. 引言

本文档旨在为在 **Windows Server 2019** 主机上，通过 **Windows 10 Pro 虚拟机** 部署 Tiledesk 开源项目，提供一份详尽的、从零开始的中文部署指南。

Tiledesk 是一个功能强大的一站式智能客服平台，集成了在线聊天、对话机器人、工单系统和知识库。本指南将采用官方推荐的 **Docker Compose** 方式进行部署，这是在您自己的服务器上运行 Tiledesk 的最简单、最可靠的方法。

**目标读者**: 希望在 Windows 虚拟化环境中私有化部署 Tiledesk 的开发者、运维工程师或 IT 管理员。
**最终目标**: 在您的 Windows 10 虚拟机上成功运行一个功能完整的 Tiledesk 实例，并能从局域网或公网访问。

---

## 2. 环境与系统要求

### 2.1 Windows Server 2019 主机
*   **操作系统**: Windows Server 2019 Standard 或 Datacenter。
*   **虚拟化**: 已安装并启用 **Hyper-V** 角色。

### 2.2 Windows 10 Pro 虚拟机
*   **操作系统**: Windows 10 Pro (22H2 或更高版本)。
*   **CPU**: 至少 **4 虚拟核心** 分配给虚拟机。
*   **内存 (RAM)**: 至少 **8 GB** 内存分配给虚拟机。
*   **存储**: 至少 **40 GB** 可用磁盘空间。
*   **软件**:
    *   **Docker Desktop**: 最新稳定版，并启用 WSL2 后端。
    *   **WSL2**: 已安装并运行一个 Linux 发行版 (如 Ubuntu)。
    *   **Git**: 用于克隆仓库。
    *   **文本编辑器**: 如 VS Code, Notepad++。

---

## 3. 部署步骤

### 步骤 3.1: 虚拟机网络配置 (关键步骤)

为了让外部能够访问在虚拟机内部运行的 Tiledesk 服务，您需要正确配置虚拟机的网络。

1.  **使用外部虚拟交换机**:
    *   在 Hyper-V 管理器中，确保您的 Windows 10 虚拟机使用的是**“外部”**类型的虚拟交换机。
    *   这会使您的虚拟机像一台独立的物理机一样，直接连接到您的局域网，并从您的路由器获取一个独立的 IP 地址。

2.  **为虚拟机设置静态 IP**:
    *   在 Windows 10 虚拟机内部，手动为其配置一个**静态 IP 地址** (例如 `192.168.1.110`)。这可以防止因 IP 地址变化导致服务无法访问。
    *   记下这个静态 IP 地址，我们将在后续步骤中称之为 **`<VM_IP>`**。

### 步骤 3.2: 克隆仓库与准备文件

在您的 **Windows 10 虚拟机**内部，打开 **PowerShell** 或 **CMD** 执行以下操作。

```powershell
# 切换到您希望安装 Tiledesk 的目录 (例如 C:\Projects)
cd C:\Projects

# 克隆您的仓库
git clone https://github.com/unkaku-1/tiledesk.git

# 进入 docker-compose 目录
# 这是所有部署文件的所在地
cd tiledesk\docker-compose\
```

现在，您需要从官方示例创建一个 `.env` 文件。

```powershell
# 复制 .env.sample 文件为 .env
copy .env.sample .env
```

### 步骤 3.3: 配置环境变量 (`.env` 文件)

使用文本编辑器 (如 Notepad++ 或 VS Code) 打开刚刚创建的 `.env` 文件。

您需要关注并修改以下**核心配置项**：

#### **A. 基础配置 (必须修改)**

*   `BASE_URL`: **极其重要**。将其修改为您虚拟机的**静态 IP 地址 `<VM_IP>`** 或未来要解析到该 IP 的**域名**。
    *   示例 (使用虚拟机 IP): `BASE_URL=http://192.168.1.110`
    *   示例 (使用域名): `BASE_URL=https://support.yourcompany.com`

*   `MONGODB_URI`: MongoDB 的连接地址。**通常无需修改**。

*   `GLOBAL_SECRET`: 用于身份验证的全局密钥。请务_**务必**_将其修改为一个**长且随机的字符串**。
    *   您可以在 PowerShell 中运行以下命令生成一个随机密钥：
        ```powershell
        # 运行此命令，并将输出结果粘贴到 .env 文件中
        [Convert]::ToBase64String((1..32 | % {Get-Random -Minimum 0 -Maximum 255}))
        ```
    *   示例: `GLOBAL_SECRET=aVeryStrongAndRandomSecretKeyGeneratedInPowerShell`

#### **B. 邮件服务配置 (强烈建议配置)**

Tiledesk 需要邮件服务来发送用户邀请、密码重置等。

*   `EMAIL_ENABLED=true`
*   `EMAIL_HOST`: 您的 SMTP 服务器地址。
*   `EMAIL_PORT`: 您的 SMTP 端口。
*   `EMAIL_USERNAME`: 您的 SMTP 用户名。
*   `EMAIL_PASSWORD`: 您的 SMTP 密码。
*   `EMAIL_FROM_ADDRESS`: 您希望邮件显示的发件人地址。

**完成修改后，请保存并关闭 `.env` 文件。**

### 步骤 3.4: 启动 Tiledesk 服务

在 `tiledesk\docker-compose\` 目录下，打开 **PowerShell** 并执行以下命令来构建和启动所有 Tiledesk 服务。

```powershell
# --build 参数会确保根据最新代码构建镜像
# -d 参数会让服务在后台运行
docker compose up --build -d
```

这个过程可能需要 5 到 15 分钟，因为它会下载所有必需的 Docker 镜像并构建服务。

**如何检查服务状态？**

运行以下命令来查看所有容器是否都已正常启动并处于 `running` 状态：

```powershell
docker compose ps
```

### 步骤 3.5: 配置 Windows 防火墙

为了让局域网内的其他计算机（包括您的 Windows Server 主机）能够访问虚拟机中的 Tiledesk，您需要在 **Windows 10 虚拟机内部** 配置防火墙。

1.  打开 "Windows Defender 防火墙"。
2.  点击 "高级设置"。
3.  选择 "入站规则"，然后点击 "新建规则..."。
4.  选择 "端口"，点击 "下一步"。
5.  选择 "TCP"，并在 "特定本地端口" 中输入 `80` (Tiledesk 的访问端口)。
6.  选择 "允许连接"，点击 "下一步"。
7.  勾选 "域" 和 "专用"，取消勾选 "公用"。
8.  为规则命名 (例如 "Tiledesk Web Access")，然后点击 "完成"。

### 步骤 3.6: 初始化与首次登录

1.  **访问控制台**:
    *   现在，您可以从**局域网内的任何计算机**（包括您的 Windows Server 主机）的浏览器中，输入您在 `.env` 文件中配置的 `BASE_URL`。
    *   例如: `http://192.168.1.110`。

2.  **创建您的第一个项目**:
    *   首次访问时，系统会引导您创建一个新的项目。请跟随向导完成。

3.  **登录**:
    *   使用您在 `.env` 文件中配置的管理员邮箱和密码 (`ADMIN_EMAIL`, `ADMIN_PASSWORD`) 登录系统。

**恭喜！您已经成功在 Windows 虚拟化环境中部署了 Tiledesk！**

---

## 4. 常用管理命令

所有管理命令都应在 **Windows 10 虚拟机** 的 `tiledesk\docker-compose\` 目录下，使用 PowerShell 执行。

*   **查看所有服务日志**:
    ```powershell
    docker compose logs -f
    ```

*   **停止所有服务**:
    ```powershell
    docker compose down
    ```

*   **更新 Tiledesk 版本**:
    ```powershell
    # 1. 从您的 Git 仓库拉取最新代码
    git pull

    # 2. 重新构建并启动服务
    docker compose up --build -d
    ```

---

## 5. 故障排查

*   **问题: 无法从外部访问 `http://<VM_IP>`。**
    *   **解决方案**:
        1.  确认您虚拟机的网络模式是“外部”。
        2.  确认您在虚拟机内部正确配置了 Windows 防火墙，开放了 80 端口。
        3.  确认 `docker compose ps` 显示所有服务都在 `running` 状态。

*   **问题: 访问后显示 "502 Bad Gateway"。**
    *   **解决方案**: 这通常意味着后端的 `tiledesk-server` 服务没有正常启动。使用 `docker compose logs -f tiledesk-server` 查看其日志以定位问题。