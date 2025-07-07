# Tiledesk 一键部署指南

本指南将引导您完成使用提供的 `deploy_tiledesk.bat` 脚本在 Windows 上部署 Tiledesk 的过程。

## 先决条件

在开始之前，请确保您的系统上已安装并运行以下软件：

1.  **Git**: 用于克隆 Tiledesk 部署仓库。
2.  **Docker Desktop**: 用于运行 Tiledesk 的 Docker 容器。**在运行部署脚本之前，请确保 Docker Desktop 正在运行。**

## 部署步骤

1.  **克隆仓库**:
    打开命令提示符或 PowerShell，并运行以下命令来克隆 Tiledesk 部署仓库：
    ```sh
    git clone https://github.com/unkaku-1/tiledesk.git tiledesk-deployment
    ```

2.  **导航到目录**:
    使用以下命令进入克隆的目录：
    ```sh
    cd tiledesk-deployment
    ```

3.  **运行部署脚本**:
    执行 `deploy_tiledesk.bat` 脚本以启动部署过程：
    ```sh
    deploy_tiledesk.bat
    ```
    该脚本将自动执行以下操作：
    - 停止并删除任何现有的 Tiledesk 容器和卷，以确保一个干净的环境。
    - 检查 Docker 是否正在运行。
    - 使用 `docker-compose` 启动所有 Tiledesk 服务。

## 验证部署

部署完成后，您可以通过以下方式验证 Tiledesk 是否正在运行：

1.  **检查 Docker 容器**:
    打开一个新的命令提示符或 PowerShell 窗口，并运行以下命令：
    ```sh
    docker ps
    ```
    您应该会看到多个正在运行的 Tiledesk 相关容器。

2.  **访问 Tiledesk 仪表板**:
    打开您的网络浏览器，并访问以下 URL：
    [http://localhost:4200](http://localhost:4200)

    您应该会看到 Tiledesk 的登录页面。

## 停止 Tiledesk

要停止 Tiledesk，请在 `tiledesk-deployment\docker-compose` 目录中运行以下命令：
```sh
docker-compose down
```
