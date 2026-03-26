import os
import subprocess
import sys

def build_shensist_matrix():
    print("🏛️ [Shensist-AIS] 正在开启 Windows 物理级封装程序...")
    
    # 1. 确保安装了打包工具
    try:
        import PyInstaller
    except ImportError:
        print("🛠️ 正在注入 PyInstaller 依赖...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller", "flask", "flask-cors", "pyautogui"])

    # 2. 定义打包参数
    # --onefile: 封装为单文件
    # --noconsole: 运行时不显示黑色终端窗口（适合专业后台）
    # --icon: 如果你有图标文件，可以添加
    # --name: 最终生成的名称
    
    main_script = "Shensist_Web_Master.py" # 你的主控内核
    dist_name = "Shensist_AirEye_Win"
    
    cmd = [
        'pyinstaller',
        '--onefile',
        '--noconsole',
        f'--name={dist_name}',
        '--clean',
        '--add-data=skills_map.json;.', # 如果有配置文件，物理注入
        main_script
    ]

    print(f"🚀 正在将灵魂注入 {dist_name}.exe ...")
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✅ [Shensist-AIS] 物理封装大功告成！")
        print(f"📂 请在 dist 文件夹下领取你的执行大脑：{dist_name}.exe")
    except subprocess.CalledProcessError as e:
        print(f"❌ 封装中断：{e}")

if __name__ == "__main__":
    build_shensist_matrix()
