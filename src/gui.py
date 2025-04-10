import tkinter as tk
from analyzer import AugmentAnalyzer


def create_overlay():
    # 创建分析器实例
    analyzer = AugmentAnalyzer()

    # 创建主窗口
    root = tk.Tk()
    root.overrideredirect(True)  # 去掉窗口边框和标题栏
    root.attributes("-topmost", True)  # 窗口始终置顶
    root.attributes("-alpha", 0.5)  # 设置窗口透明度 (0.0 完全透明, 1.0 完全不透明)

    # 设置窗口背景颜色为浅灰色
    root.configure(bg="#F0F0F0")

    # 获取屏幕尺寸并设置窗口位置
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 300
    window_height = 500
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # 鼠标拖动窗口的变量
    drag_data = {"x": 0, "y": 0}

    # 鼠标按下事件
    def start_drag(event):
        drag_data["x"] = event.x
        drag_data["y"] = event.y

    # 鼠标移动事件
    def on_drag(event):
        deltax = event.x - drag_data["x"]
        deltay = event.y - drag_data["y"]
        x = root.winfo_x() + deltax
        y = root.winfo_y() + deltay
        root.geometry(f"+{x}+{y}")

    # 绑定鼠标事件
    root.bind("<ButtonPress-1>", start_drag)  # 按下鼠标左键
    root.bind("<B1-Motion>", on_drag)  # 拖动鼠标

    # 创建一个Frame来容纳文本区域和滚动条
    text_frame = tk.Frame(root, bg="#F0F0F0")
    text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    text_frame.pack_propagate(False)  # 防止frame自动调整大小
    text_frame.configure(height=400)  # 设置固定高度

    # 创建滚动条
    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # 添加文字标签，并启用自动换行
    label_text = tk.StringVar(value="点击开始进行强化符文分析")
    label = tk.Label(
        text_frame,
        textvariable=label_text,  # 使用 StringVar 动态更新文本
        font=("Arial", 12),
        fg="blue",  # 文字颜色
        bg="#F0F0F0",  # 背景颜色
        wraplength=window_width - 40,  # 设置自动换行的最大宽度
        justify=tk.LEFT  # 左对齐文本
    )
    label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))

    # 配置滚动条
    label.bind('<Configure>', lambda e: scrollbar.set(0, 1.0))
    scrollbar.config(command=lambda *args: label.yview(*args))

    # 创建一个容器 Frame 来放置按钮，设置固定高度
    button_frame = tk.Frame(root, bg="#F0F0F0", height=50)
    button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
    button_frame.pack_propagate(False)  # 防止frame自动调整大小

    # 分析状态标志
    analyzing = False

    # 启动按钮的功能：截图并分析
    def analyze_screenshot():
        nonlocal analyzing
        if analyzing:  # 如果正在分析中，直接返回
            return
        analyzing = True
        start_button.config(state=tk.DISABLED)  # 禁用按钮
        label_text.set("正在分析中...")
        root.update()
        try:
            # 截图
            image = analyzer.capture_screen()
            # 分析图片
            result = analyzer.analyze_augment(image)
            if result:
                label_text.set(result)
            else:
                label_text.set("分析失败，请重试")
        finally:
            analyzing = False
            start_button.config(state=tk.NORMAL)  # 恢复按钮

    # 添加启动按钮
    start_button = tk.Button(
        button_frame,
        text="开始",
        font=("Arial", 12),
        bg="#4CAF50",  # 按钮背景颜色（绿色）
        fg="white",  # 按钮文字颜色
        relief=tk.FLAT,  # 去掉按钮边框
        command=analyze_screenshot  # 绑定截图分析功能
    )
    start_button.pack(side=tk.LEFT, padx=5)

    # 添加关闭按钮
    close_button = tk.Button(
        button_frame,
        text="关闭",
        font=("Arial", 12),
        bg="#FF6347",  # 按钮背景颜色（红色）
        fg="white",  # 按钮文字颜色
        relief=tk.FLAT,  # 去掉按钮边框
        command=root.destroy  # 点击按钮关闭窗口
    )
    close_button.pack(side=tk.RIGHT, padx=5)

    # 运行主循环
    root.mainloop()


if __name__ == "__main__":
    create_overlay()