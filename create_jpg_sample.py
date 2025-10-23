import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_essay_jpg():
    """创建JPG格式的示例英语作文图片"""
    # 创建白色背景
    width, height = 800, 1000
    image = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    # 添加标题
    cv2.putText(image, "My Favorite Season", (50, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)
    
    # 添加作文内容
    essay_text = [
        "Spring is my favorite season of the year. When spring comes,",
        "the weather becomes warmer and the days get longer. The trees",
        "start to grow new leaves and flowers begin to bloom everywhere.",
        "",
        "I love spring because it brings new life to nature. The birds",
        "return from their winter homes and start singing beautiful songs.",
        "The grass turns green again and the whole world seems to wake up",
        "from its winter sleep.",
        "",
        "In spring, I enjoy going for walks in the park. I can see the",
        "beautiful cherry blossoms and smell the fresh air. Sometimes I",
        "like to have a picnic with my family under the blooming trees.",
        "",
        "Spring also means that summer vacation is coming soon. I look",
        "forward to spending more time outdoors and playing with my friends.",
        "The warm sunshine makes me feel happy and energetic.",
        "",
        "In conclusion, spring is a wonderful season that brings joy and",
        "hope to everyone. It reminds us that after every winter, there",
        "is always a beautiful spring waiting for us."
    ]
    
    # 绘制文本
    y_position = 120
    line_height = 30
    
    for line in essay_text:
        if line.strip():  # 非空行
            cv2.putText(image, line, (50, y_position), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1)
        y_position += line_height
    
    # 添加一些装饰线条
    cv2.line(image, (50, 100), (750, 100), (200, 200, 200), 1)
    cv2.line(image, (50, 950), (750, 950), (200, 200, 200), 1)
    
    return image

def create_sample_highlights():
    """创建示例高亮标记数据"""
    highlight_data = {
        'circle': [
            (200, 150),  # 标记 "Spring"
            (400, 200),  # 标记 "favorite"
            (300, 350),  # 标记 "nature"
        ],
        'single_line': [
            (100, 180), (300, 180),  # 标记第一句
            (100, 250), (400, 250),  # 标记第二句
        ],
        'double_line': [
            (100, 320), (500, 320),  # 标记第三句
            (100, 380), (600, 380),  # 标记第四句
        ],
        'wavy_line': [
            (100, 450), (400, 450),  # 标记第五句
            (100, 520), (500, 520),  # 标记第六句
        ]
    }
    return highlight_data

def create_jpg_demo():
    """创建JPG格式的演示图片"""
    print("正在创建JPG格式的示例英语作文图片...")
    
    # 创建示例图片
    sample_image = create_sample_essay_jpg()
    
    # 保存为JPG格式
    cv2.imwrite("sample_essay.jpg", sample_image, [cv2.IMWRITE_JPEG_QUALITY, 95])
    print("JPG格式示例作文图片已保存为: sample_essay.jpg")
    
    # 创建高亮标记数据
    highlight_data = create_sample_highlights()
    
    # 使用高亮工具处理图片
    from highlight_tool import HighlightTool
    highlight_tool = HighlightTool()
    
    # 处理图片
    processed_image = highlight_tool.process_image_with_highlights("sample_essay.jpg", highlight_data)
    
    # 创建图例
    legend = highlight_tool.create_legend(processed_image.shape[1])
    
    # 组合图片和图例
    final_image = highlight_tool.combine_image_with_legend(processed_image, legend)
    
    # 保存为JPG格式
    cv2.imwrite("sample_essay_with_highlights.jpg", final_image, [cv2.IMWRITE_JPEG_QUALITY, 95])
    print("JPG格式带高亮标记的示例图片已保存为: sample_essay_with_highlights.jpg")
    
    print("\nJPG格式演示完成！")
    print("您可以查看以下文件：")
    print("- sample_essay.jpg: JPG格式原始英语作文图片")
    print("- sample_essay_with_highlights.jpg: JPG格式带高亮标记的图片")
    print("\n运行 python main.py 启动图形界面进行交互式标记")

if __name__ == "__main__":
    create_jpg_demo()
