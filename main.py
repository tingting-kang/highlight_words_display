import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
import numpy as np
from PIL import Image, ImageTk
import os
from highlight_tool import HighlightTool

class HighlightApp:
    """英语作文高亮标记应用程序"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("英语作文高亮标记工具")
        self.root.geometry("1000x700")
        
        # 初始化高亮工具
        self.highlight_tool = HighlightTool()
        
        # 当前图片路径
        self.current_image_path = None
        self.current_image = None
        self.display_image = None
        
        # 高亮数据
        self.highlight_data = {
            'circle': [],
            'single_line': [],
            'double_line': [],
            'wavy_line': []
        }
        
        # 当前选择的标记类型
        self.current_mark_type = tk.StringVar(value='circle')
        
        # 创建界面
        self.create_widgets()
        
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 顶部控制面板
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 文件操作按钮
        ttk.Button(control_frame, text="选择图片", command=self.load_image).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="保存结果", command=self.save_result).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="清除标记", command=self.clear_marks).pack(side=tk.LEFT, padx=(0, 10))
        
        # 标记类型选择
        mark_frame = ttk.LabelFrame(control_frame, text="选择标记类型")
        mark_frame.pack(side=tk.RIGHT)
        
        mark_types = [
            ('圆圈标记', 'circle'),
            ('横线标记', 'single_line'),
            ('双横线标记', 'double_line'),
            ('波浪线标记', 'wavy_line')
        ]
        
        for text, value in mark_types:
            ttk.Radiobutton(mark_frame, text=text, variable=self.current_mark_type, 
                           value=value).pack(side=tk.LEFT, padx=5)
        
        # 图片显示区域
        image_frame = ttk.Frame(main_frame)
        image_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建滚动条
        canvas_frame = ttk.Frame(image_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg='white')
        self.scrollbar_v = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar_h = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=self.scrollbar_v.set, xscrollcommand=self.scrollbar_h.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar_h.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 绑定鼠标事件
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        
        # 状态栏
        self.status_var = tk.StringVar(value="请选择一张图片开始标记")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, pady=(10, 0))
        
        # 拖拽状态
        self.drag_start = None
        self.drag_end = None
        
    def load_image(self):
        """加载图片"""
        file_path = filedialog.askopenfilename(
            title="选择英语作文图片",
            filetypes=[
                ("JPG图片", "*.jpg *.jpeg"),
                ("PNG图片", "*.png"),
                ("所有图片", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            try:
                self.current_image_path = file_path
                
                # 使用PIL读取图片（支持中文路径）
                from PIL import Image
                pil_image = Image.open(file_path)
                # 转换为OpenCV格式
                self.current_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
                
                if self.current_image is None:
                    messagebox.showerror("错误", "无法读取图片文件")
                    return
                
                # 清除之前的标记
                self.clear_marks()
                
                # 显示图片
                self.display_image_on_canvas()
                self.status_var.set(f"已加载图片: {os.path.basename(file_path)}")
                
            except Exception as e:
                messagebox.showerror("错误", f"加载图片时出错: {str(e)}")
    
    def display_image_on_canvas(self):
        """在画布上显示图片"""
        if self.current_image is None:
            return
        
        # 转换为PIL图像
        image_rgb = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image_rgb)
        
        # 调整图片大小以适应画布
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width > 1 and canvas_height > 1:
            # 计算缩放比例
            img_width, img_height = pil_image.size
            scale_x = canvas_width / img_width
            scale_y = canvas_height / img_height
            self.scale = min(scale_x, scale_y, 1.0)  # 不放大图片
            
            new_width = int(img_width * self.scale)
            new_height = int(img_height * self.scale)
            
            pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # 转换为Tkinter图像
        self.display_image = ImageTk.PhotoImage(pil_image)
        
        # 清除画布并显示图片
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.display_image)
        
        # 更新滚动区域
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        # 重新绘制所有标记
        self.redraw_marks()
    
    def on_canvas_click(self, event):
        """画布点击事件"""
        if self.current_image is None:
            return
        
        # 获取画布坐标
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        # 转换为图片坐标
        if hasattr(self, 'scale'):
            img_x = int(canvas_x / self.scale)
            img_y = int(canvas_y / self.scale)
            
            # 添加标记点
            mark_type = self.current_mark_type.get()
            self.highlight_data[mark_type].append((img_x, img_y))
            
            # 重新绘制标记
            self.redraw_marks()
            
            self.status_var.set(f"已添加{self.highlight_tool.highlight_styles[mark_type]['name']}")
    
    def on_canvas_drag(self, event):
        """画布拖拽事件"""
        if self.current_image is None:
            return
        
        # 获取画布坐标
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        if self.drag_start is None:
            self.drag_start = (canvas_x, canvas_y)
        else:
            self.drag_end = (canvas_x, canvas_y)
            
            # 清除临时线条
            self.canvas.delete("temp_line")
            
            # 绘制临时线条
            mark_type = self.current_mark_type.get()
            color = self.highlight_tool.highlight_styles[mark_type]['color']
            
            if mark_type in ['single_line', 'double_line', 'wavy_line']:
                self.canvas.create_line(self.drag_start[0], self.drag_start[1], 
                                      self.drag_end[0], self.drag_end[1], 
                                      fill=f"#{color[2]:02x}{color[1]:02x}{color[0]:02x}", 
                                      width=3, tags="temp_line")
    
    def on_canvas_release(self, event):
        """画布释放事件"""
        if self.current_image is None or self.drag_start is None:
            return
        
        # 获取画布坐标
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        # 转换为图片坐标
        if hasattr(self, 'scale'):
            start_img_x = int(self.drag_start[0] / self.scale)
            start_img_y = int(self.drag_start[1] / self.scale)
            end_img_x = int(canvas_x / self.scale)
            end_img_y = int(canvas_y / self.scale)
            
            # 添加线条标记
            mark_type = self.current_mark_type.get()
            if mark_type in ['single_line', 'double_line', 'wavy_line']:
                self.highlight_data[mark_type].extend([(start_img_x, start_img_y), (end_img_x, end_img_y)])
            
            # 清除临时线条
            self.canvas.delete("temp_line")
            
            # 重新绘制标记
            self.redraw_marks()
            
            self.status_var.set(f"已添加{self.highlight_tool.highlight_styles[mark_type]['name']}")
        
        # 重置拖拽状态
        self.drag_start = None
        self.drag_end = None
    
    def redraw_marks(self):
        """重新绘制所有标记"""
        if self.current_image is None or not hasattr(self, 'scale'):
            return
        
        # 清除现有标记
        self.canvas.delete("mark")
        
        # 绘制所有标记
        for mark_type, points in self.highlight_data.items():
            if not points:
                continue
                
            color = self.highlight_tool.highlight_styles[mark_type]['color']
            color_hex = f"#{color[2]:02x}{color[1]:02x}{color[0]:02x}"
            
            if mark_type == 'circle':
                for point in points:
                    canvas_x = point[0] * self.scale
                    canvas_y = point[1] * self.scale
                    self.canvas.create_oval(canvas_x-15, canvas_y-15, canvas_x+15, canvas_y+15,
                                          outline=color_hex, width=3, tags="mark")
            elif mark_type in ['single_line', 'double_line']:
                for i in range(0, len(points)-1, 2):
                    if i+1 < len(points):
                        start_x = points[i][0] * self.scale
                        start_y = points[i][1] * self.scale
                        end_x = points[i+1][0] * self.scale
                        end_y = points[i+1][1] * self.scale
                        
                        self.canvas.create_line(start_x, start_y, end_x, end_y,
                                              fill=color_hex, width=3, tags="mark")
                        
                        if mark_type == 'double_line':
                            # 绘制第二条线
                            offset = 5
                            self.canvas.create_line(start_x, start_y+offset, end_x, end_y+offset,
                                                  fill=color_hex, width=2, tags="mark")
            elif mark_type == 'wavy_line':
                for i in range(0, len(points)-1, 2):
                    if i+1 < len(points):
                        start_x = points[i][0] * self.scale
                        start_y = points[i][1] * self.scale
                        end_x = points[i+1][0] * self.scale
                        end_y = points[i+1][1] * self.scale
                        
                        # 绘制波浪线
                        steps = 20
                        for j in range(steps):
                            t1 = j / steps
                            t2 = (j + 1) / steps
                            
                            x1 = start_x + t1 * (end_x - start_x)
                            y1 = start_y + t1 * (end_y - start_y) + 8 * np.sin(t1 * np.pi * 3)
                            x2 = start_x + t2 * (end_x - start_x)
                            y2 = start_y + t2 * (end_y - start_y) + 8 * np.sin(t2 * np.pi * 3)
                            
                            self.canvas.create_line(x1, y1, x2, y2,
                                                  fill=color_hex, width=2, tags="mark")
    
    def clear_marks(self):
        """清除所有标记"""
        self.highlight_data = {
            'circle': [],
            'single_line': [],
            'double_line': [],
            'wavy_line': []
        }
        self.canvas.delete("mark")
        self.status_var.set("已清除所有标记")
    
    def save_result(self):
        """保存结果"""
        if self.current_image is None:
            messagebox.showwarning("警告", "请先加载图片")
            return
        
        # 检查是否有标记
        has_marks = any(self.highlight_data.values())
        if not has_marks:
            messagebox.showwarning("警告", "请先添加一些标记")
            return
        
        # 选择保存路径
        file_path = filedialog.asksaveasfilename(
            title="保存结果",
            defaultextension=".jpg",
            filetypes=[
                ("JPG文件", "*.jpg"),
                ("PNG文件", "*.png"),
                ("JPEG文件", "*.jpeg"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            try:
                # 处理图片并添加标记
                processed_image = self.highlight_tool.process_image_with_highlights(
                    self.current_image_path, self.highlight_data
                )
                
                # 创建图例
                legend = self.highlight_tool.create_legend(processed_image.shape[1])
                
                # 组合图片和图例
                final_image = self.highlight_tool.combine_image_with_legend(processed_image, legend)
                
                # 保存结果
                # 根据文件扩展名选择保存格式
                file_ext = os.path.splitext(file_path)[1].lower()
                if file_ext in ['.jpg', '.jpeg']:
                    # JPG格式保存
                    cv2.imwrite(file_path, final_image, [cv2.IMWRITE_JPEG_QUALITY, 95])
                else:
                    # 其他格式保存
                    cv2.imwrite(file_path, final_image)
                
                messagebox.showinfo("成功", f"结果已保存到: {file_path}")
                self.status_var.set(f"结果已保存: {os.path.basename(file_path)}")
                
            except Exception as e:
                messagebox.showerror("错误", f"保存时出错: {str(e)}")

def main():
    """主函数"""
    root = tk.Tk()
    app = HighlightApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
