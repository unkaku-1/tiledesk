import yaml
import socket
import subprocess
import os
import sys

def is_port_in_use(port: int) -> bool:
    """检查指定端口是否被占用。"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def find_available_port(start_port: int) -> int:
    """从起始端口开始查找一个可用端口。"""
    port = start_port
    while is_port_in_use(port):
        port += 1
    return port

def main():
    """主执行函数。"""
    compose_file = 'docker-compose.yml'
    modified_compose_file = 'docker-compose.modified.yml'
    
    print(f"正在读取 '{compose_file}'...")
    try:
        with open(compose_file, 'r') as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"错误: '{compose_file}' 未找到。请确保此脚本与 docker-compose.yml 在同一目录下运行。")
        sys.exit(1)
    except Exception as e:
        print(f"读取或解析YAML文件时出错: {e}")
        sys.exit(1)

    if 'services' not in data:
        print("错误: 'docker-compose.yml' 文件中未找到 'services' 部分。")
        sys.exit(1)

    print("正在检查端口占用情况...")
    changes_made = False
    for service_name, service_config in data.get('services', {}).items():
        if 'ports' in service_config:
            new_ports = []
            for port_mapping in service_config.get('ports', []):
                try:
                    host_port_str, container_port_str = str(port_mapping).split(':')
                    host_port = int(host_port_str)
                    
                    if is_port_in_use(host_port):
                        print(f"端口 {host_port} (服务: {service_name}) 已被占用。正在寻找可用端口...")
                        new_port = find_available_port(host_port)
                        print(f"找到可用端口: {new_port}。正在重新映射...")
                        new_ports.append(f"{new_port}:{container_port_str}")
                        changes_made = True
                    else:
                        new_ports.append(port_mapping)
                except ValueError:
                    # 处理没有主机端口的情况，例如 "80"
                    new_ports.append(port_mapping)
                    print(f"警告: 服务 '{service_name}' 的端口映射 '{port_mapping}' 格式不标准，已跳过检查。")

            service_config['ports'] = new_ports

    if changes_made:
        print(f"端口已修改，正在将新配置写入 '{modified_compose_file}'...")
        try:
            with open(modified_compose_file, 'w') as f:
                yaml.dump(data, f, default_flow_style=False)
        except Exception as e:
            print(f"写入修改后的YAML文件时出错: {e}")
            sys.exit(1)
        compose_to_use = modified_compose_file
    else:
        print("所有端口均可用，无需修改。")
        compose_to_use = compose_file

    print("\n正在停止并清理旧的容器（如果存在）...")
    subprocess.run(['docker-compose', '-f', compose_file, 'down', '--remove-orphans'], check=False)

    print(f"\n正在使用 '{compose_to_use}' 启动 Tiledesk 服务...")
    try:
        subprocess.run(['docker-compose', '-f', compose_to_use, 'up', '-d'], check=True)
        print("\n部署成功！Tiledesk 正在后台运行。")
    except subprocess.CalledProcessError as e:
        print(f"\n部署失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    # 确保脚本在 docker-compose 文件所在的目录中运行
    script_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_dir)
    main()
