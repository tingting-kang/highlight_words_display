import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

class HighlightTool:
    """英语作文高亮标记工具"""
    
    def __init__(self):
        # 定义四种高亮颜色和样式
        self.highlight_styles = {
            'circle': {
                'color': (255, 0, 0),  # 红色
                'name': '圆圈标记',
                'symbol': '●'
            },
            'single_line': {
                'color': (0, 0, 255),  # 蓝色
                'name': '横线标记',
                'symbol': '━'
            },
            'double_line': {
                'color': (0, 255, 0),  # 绿色
                'name': '双横线标记',
                'symbol': '═'
            },
            'wavy_line': {
                'color': (0, 255, 255),  # 黄色
                'name': '波浪线标记',
                'symbol': '∿'
            }
        }
        
    def add_circle_highlight(self, image, points, thickness=3):
        """添加圆圈高亮标记"""
        color = self.highlight_styles['circle']['color']
        for point in points:
            cv2.circle(image, point, 15, color, thickness)
        return image
    
    def add_single_line_highlight(self, image, points, thickness=3):
        """添加横线高亮标记"""
        color = self.highlight_styles['single_line']['color']
        for i in range(0, len(points)-1, 2):
            if i+1 < len(points):
                cv2.line(image, points[i], points[i+1], color, thickness)
        return image
    
    def add_double_line_highlight(self, image, points, thickness=2):
        """添加双横线高亮标记"""
        color = self.highlight_styles['double_line']['color']
        for i in range(0, len(points)-1, 2):
            if i+1 < len(points):
                # 绘制两条平行线
                cv2.line(image, points[i], points[i+1], color, thickness)
                # 向下偏移几个像素绘制第二条线
                offset_points = [(p[0], p[1] + 5) for p in [points[i], points[i+1]]]
                cv2.line(image, offset_points[0], offset_points[1], color, thickness)
        return image
    
    def add_wavy_line_highlight(self, image, points, thickness=2):
        """添加波浪线高亮标记"""
        color = self.highlight_styles['wavy_line']['color']
        for i in range(0, len(points)-1, 2):
            if i+1 < len(points):
                start_point = points[i]
                end_point = points[i+1]
                
                # 计算波浪线的控制点
                mid_x = (start_point[0] + end_point[0]) // 2
                mid_y = (start_point[1] + end_point[1]) // 2
                
                # 创建波浪线路径
                wave_points = []
                steps = 20
                for j in range(steps + 1):
                    t = j / steps
                    x = int(start_point[0] + t * (end_point[0] - start_point[0]))
                    y = int(start_point[1] + t * (end_point[1] - start_point[1]))
                    # 添加波浪效果
                    wave_offset = int(8 * np.sin(t * np.pi * 3))
                    y += wave_offset
                    wave_points.append((x, y))
                
                # 绘制波浪线
                for k in range(len(wave_points) - 1):
                    cv2.line(image, wave_points[k], wave_points[k+1], color, thickness)
        return image
    
    def process_image_with_highlights(self, image_path, highlight_data):
        """
        处理图片并添加高亮标记
        
        Args:
            image_path: 图片路径
            highlight_data: 高亮数据字典，格式：
            {
                'circle': [(x1, y1), (x2, y2), ...],
                'single_line': [(x1, y1), (x2, y2), ...],
                'double_line': [(x1, y1), (x2, y2), ...],
                'wavy_line': [(x1, y1), (x2, y2), ...]
            }
        """
        # 读取图片 - 使用numpy和PIL处理中文路径
        import numpy as np
        from PIL import Image
        
        # 使用PIL读取图片（支持中文路径）
        pil_image = Image.open(image_path)
        # 转换为OpenCV格式
        image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        if image is None:
            raise ValueError(f"无法读取图片: {image_path}")
        
        # 添加各种高亮标记
        for style, points in highlight_data.items():
            if style == 'circle' and points:
                image = self.add_circle_highlight(image, points)
            elif style == 'single_line' and points:
                image = self.add_single_line_highlight(image, points)
            elif style == 'double_line' and points:
                image = self.add_double_line_highlight(image, points)
            elif style == 'wavy_line' and points:
                image = self.add_wavy_line_highlight(image, points)
        
        return image
    
    def create_legend(self, image_width, legend_height=100):
        """创建图例"""
        # 创建图例画布
        legend = np.ones((legend_height, image_width, 3), dtype=np.uint8) * 255
        
        # 计算每个图例项的宽度
        item_width = image_width // 4
        start_x = 20
        
        for i, (style_key, style_info) in enumerate(self.highlight_styles.items()):
            x = start_x + i * item_width
            y = legend_height // 2
            
            # 绘制示例标记
            if style_key == 'circle':
                cv2.circle(legend, (x, y), 15, style_info['color'], 3)
            elif style_key == 'single_line':
                cv2.line(legend, (x-15, y), (x+15, y), style_info['color'], 3)
            elif style_key == 'double_line':
                cv2.line(legend, (x-15, y-3), (x+15, y-3), style_info['color'], 2)
                cv2.line(legend, (x-15, y+3), (x+15, y+3), style_info['color'], 2)
            elif style_key == 'wavy_line':
                # 绘制波浪线示例
                wave_points = []
                for j in range(30):
                    t = j / 29
                    px = int(x - 15 + t * 30)
                    py = int(y + 8 * np.sin(t * np.pi * 3))
                    wave_points.append((px, py))
                for k in range(len(wave_points) - 1):
                    cv2.line(legend, wave_points[k], wave_points[k+1], style_info['color'], 2)
            
            # 添加文字说明
            text = style_info['name']
            font_scale = 0.6
            font_thickness = 1
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)[0]
            text_x = x - text_size[0] // 2
            text_y = y + 35
            
            cv2.putText(legend, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 
                       font_scale, (0, 0, 0), font_thickness)
        
        return legend
    
    def combine_image_with_legend(self, image, legend):
        """将图片和图例组合"""
        # 确保图例宽度与图片宽度一致
        if legend.shape[1] != image.shape[1]:
            legend = cv2.resize(legend, (image.shape[1], legend.shape[0]))
        
        # 垂直拼接图片和图例
        combined = np.vstack([image, legend])
        return combined
    
    def save_result(self, image, output_path):
        """保存结果图片"""
        # 根据文件扩展名选择保存格式
        file_ext = os.path.splitext(output_path)[1].lower()
        if file_ext in ['.jpg', '.jpeg']:
            # JPG格式保存，设置高质量
            cv2.imwrite(output_path, image, [cv2.IMWRITE_JPEG_QUALITY, 95])
        else:
            # 其他格式保存
            cv2.imwrite(output_path, image)
        print(f"结果已保存到: {output_path}")
