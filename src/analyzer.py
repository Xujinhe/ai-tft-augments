import json
import keyboard
import pyautogui
import base64
import os
from pathlib import Path
from openai import OpenAI
from io import BytesIO
import time

class AugmentAnalyzer:
    def __init__(self, config_path=None):
        self.config = self._load_config(config_path)
        self.augments_data = self._load_augments_data()

    def _load_config(self, config_path=None):
        """加载配置文件"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / 'config.json'
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _load_augments_data(self):
        """加载强化符文数据"""
        data_path = Path(__file__).parent.parent / 'augments_merged.json'
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def capture_screen(self):
        """截取当前屏幕"""
        screenshot = pyautogui.screenshot()
        return screenshot
    
    def analyze_augment(self, image):
        """调用多模态模型API分析强化符文"""
        # 记录开始时间
        start_time = time.time()
        
        # 将PIL图像转换为base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        # 创建OpenAI客户端
        client = OpenAI(
            api_key=self.config['api_key'],
            base_url=self.config['api_endpoint']
        )
        
        try:
            # 构建系统提示，包含完整的强化符文数据
            system_prompt = {
                "role": "你是一个专门分析云顶之弈强化符文的助手，",
                "task": "我将给你一张云顶之弈强化符文选择界面的截图，请只关注图片中间的3个强化符文，无视其它无关内容。图片中的强化符文是中文名称，你需要提取名称后返回JSON数据，名称后出现的编号使用多个I组成，注意区分名称后出现的I和！。",
                "format": "严格遵照返回格式返回纯文本的JSON，禁止使用Markdown代码块包裹JSON，无需进行其它解释,返回格式示例：[{\"中文名称\":\"强化名称1\"},{\"中文名称\":\"强化名称\"},{\"中文名称\":\"强化名称2\"},{\"中文名称\":\"强化名称3\"}]"
            }
            
            # 构建消息
            completion = client.chat.completions.create(
                model=self.config['model'],
                messages=[
                    {
                        "role": "system",
                        "content": [{"type":"text","text": json.dumps(system_prompt, ensure_ascii=False)}]
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/png;base64,{base64_image}"}
                            },
                            {"type": "text", "text": "请获取这张图片中的强化符文。"}
                        ]
                    }
                ]
            )
            
            response_content = completion.choices[0].message.content
            cleaned_output = clean_json_output(response_content)
            # 计算耗时
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            # 解析JSON数据
            augments = json.loads(cleaned_output)
            
            # 构建输出结果
            output_lines = []
            for i, augment in enumerate(augments, 1):
                chinese_name = augment.get('中文名称', '').replace(' ', '')

                # 在augments_data中查找匹配项
                matched_augment = None
                for aug in self.augments_data['augments']:
                    if aug['中文名称'].replace(' ', '') == chinese_name:
                        matched_augment = aug
                        break
                
                # 构建输出字符串
                if i > 1:  # 从第二个强化符文开始，先添加空行
                    output_lines.append('')
                output_lines.append(f'强化符文 {i}：')
                output_lines.append(f'- 名称：{chinese_name}')
                if matched_augment:
                    output_lines.append(f'- 英文名称：{matched_augment["英文名称"]}')
                    output_lines.append(f'- 强度等级：{matched_augment["强度等级"]}')
                else:
                    output_lines.append('- 英文名称：未知')
                    output_lines.append('- 强度等级：未知')
            
            # 合并输出结果
            output = '\n'.join(output_lines)
            output += f'\n\n分析耗时：{elapsed_time:.2f}秒'
            print(output)

            return output
            
        except Exception as e:
            print(f'API请求失败: {e}')
            return None
    
    def start_monitoring(self, hotkey='ctrl+alt+t'):
        """开始监听快捷键"""
        print(f'按下 {hotkey} 开始分析强化符文...')
        
        def on_triggered():
            # 截图
            print(f'截图成功')
            image = self.capture_screen()
            # 分析图片
            print(f'开始分析强化符文')
            result = self.analyze_augment(image)
            if result:
                print('分析结果:')
                print(result)

        
        # 注册快捷键
        keyboard.add_hotkey(hotkey, on_triggered)
        keyboard.wait()

def clean_json_output(raw_output):
    # 移除可能存在的Markdown代码块标记
    if raw_output.startswith("```json"):
        raw_output = raw_output[len("```json"):]
    if raw_output.endswith("```"):
        raw_output = raw_output[:-3]
    # 去除首尾空白字符
    raw_output = raw_output.strip()
    return raw_output

def main():
    # 创建分析器实例
    analyzer = AugmentAnalyzer()
    
    # 开始监听快捷键
    analyzer.start_monitoring()

if __name__ == '__main__':
    main()