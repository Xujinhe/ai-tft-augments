# AI TFT 助手

这是一个基于AI的云顶之弈(TFT)游戏助手，可以帮助玩家分析强化符文强度。

## 项目结构

```
.
├── src/                          # 源代码目录
│   ├── analyzer.py               # 分析器核心代码
│   └── gui.py                    # 图形界面代码
├── augments_merged.json          # 强化符文数据
├── config.json                   # 配置文件
├── requirements.txt              # 项目依赖
└── README.md                     # 项目说明文档
```

## 环境要求

- Python 3.8 或更高版本
- pip 包管理器

## 安装依赖

在项目根目录下运行以下命令安装所需依赖：

```bash
pip install -r requirements.txt
```

## 配置说明

在运行程序前，需要先配置 `config.json` 文件：

```json
{
    "model": "qwen-vl-max-2025-04-02",    // AI模型名称
    "api_key": "your-api-key",           // 你的API密钥（）
    "api_endpoint": "https://dashscope.aliyuncs.com/compatible-mode/v1"   // API接口地址
}
```

请将上述配置中的参数替换为你的实际配置：
- `model`：替换为你要使用的AI模型名称（如 `qwen-vl-max-lasted`），目前只测试过qwen-vl-max最新版本
- `api_key`：替换为你的API密钥（可以去阿里百炼大模型平台自行注册一个账号，新用户有每个模型一百万token的额度）
- `api_endpoint`：替换为实际的API接口地址

## 运行程序

启动GUI界面：

```bash
python src/gui.py
```

运行后会出现一个半透明的悬浮窗口，可以通过鼠标拖动调整位置，点击开始后分析主屏幕上的强化符文强度。

## 编程小白简易教程
下载AI编程软件，如trae（https://www.trae.com.cn/），并使用Builder模式向AI提问如何启动gui文件