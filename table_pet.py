import os
import math
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk


class TablePet:
    def __init__(self):
        self.root = TkinterDnD.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-transparentcolor', '#2b2b2b')
        self.root.configure(bg='#2b2b2b')
        self.win_size = 200
        self.root.geometry(f"{self.win_size}x{self.win_size}+800+400")

        # 拖动状态
        self._drag_x = 0
        self._drag_y = 0
        self.is_dragging = False

        # 浮动动画基准位置
        self.base_x = 800
        self.base_y = 400
        self._offset = 0

        self.pet_image = self.load_pet_image()
        self.setup_ui()
        self.bind_events()

        # 启动浮动动画
        self.animate()

    def load_pet_image(self):
        img_path = os.path.join("assets", "pet.png")
        if os.path.exists(img_path):
            try:
                img = Image.open(img_path).convert("RGBA")
                img = img.resize((self.win_size, self.win_size), Image.LANCZOS)
                return ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"图片加载失败：{e}")
        print("未找到 assets/pet.png，使用 emoji 代替")
        return None

    def setup_ui(self):
        if self.pet_image:
            self.pet_label = tk.Label(self.root, image=self.pet_image, bg='#2b2b2b', bd=0)
        else:
            self.pet_label = tk.Label(self.root, text="🐾", font=("Arial", 80),
                                      bg='#2b2b2b', fg='#00ffcc', bd=0)
        self.pet_label.pack(expand=True, fill='both')

        self.status_label = tk.Label(self.root, text="拖PDF给我翻译", font=("微软雅黑", 9),
                                     bg='#2b2b2b', fg='#00ffcc', bd=0)
        self.status_label.place(relx=0.5, rely=0.92, anchor='center')

    def bind_events(self):
        # 鼠标拖动窗口
        self.pet_label.bind("<ButtonPress-1>", self.on_press)
        self.pet_label.bind("<B1-Motion>", self.on_drag)
        self.pet_label.bind("<ButtonRelease-1>", self.on_release)

        # 右键菜单
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="退出", command=self.root.destroy)
        self.pet_label.bind("<Button-3>", self.show_menu)

        # 文件拖拽绑定
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_drop)
        self.pet_label.drop_target_register(DND_FILES)
        self.pet_label.dnd_bind('<<Drop>>', self.on_drop)

    def show_menu(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def on_press(self, event):
        self.is_dragging = True
        self._drag_x = event.x_root
        self._drag_y = event.y_root

    def on_drag(self, event):
        dx = event.x_root - self._drag_x
        dy = event.y_root - self._drag_y
        self.root.geometry(f"+{self.root.winfo_x() + dx}+{self.root.winfo_y() + dy}")
        self._drag_x = event.x_root
        self._drag_y = event.y_root

    def on_release(self, event):
        self.base_x = self.root.winfo_x()
        self.base_y = self.root.winfo_y()
        self._offset = 0
        self.is_dragging = False

    def on_drop(self, event):
        file_path = event.data.strip('{}')
        filename = os.path.basename(file_path)
        print(f"收到文件：{file_path}")

        if not filename.lower().endswith('.pdf'):
            self.status_label.config(text="只支持PDF哦")
            return

        self.status_label.config(text=f"提取中：{filename}")
        self.root.update()

        try:
            from pdf_reader import extract_text_from_pdf
            text = extract_text_from_pdf(file_path)
        except Exception as e:
            print(f"提取模块报错：{e}")
            self.status_label.config(text="提取模块未准备好")
            return

        if not text:
            self.status_label.config(text="提取失败（可能是扫描版）")
            return

        self.status_label.config(text="百度翻译中，请稍候...")
        self.root.update()

        try:
            from translator import translate_text
            translated = translate_text(text)
        except Exception as e:
            print(f"翻译模块报错：{e}")
            self.status_label.config(text="翻译模块未准备好")
            return

        if not translated:
            self.status_label.config(text="翻译失败")
            return

        out_dir = os.path.join(os.path.dirname(__file__), "output")
        os.makedirs(out_dir, exist_ok=True)
        out_name = os.path.splitext(filename)[0] + "_中文.txt"
        out_path = os.path.join(out_dir, out_name)

        try:
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(translated)
            self.status_label.config(text=f"完成！{out_name}")
            print(f"已保存：{out_path}")
        except Exception as e:
            print(f"写入文件失败：{e}")
            self.status_label.config(text="保存失败")

    def animate(self):
        if not self.is_dragging:
            self._offset += 1
            dy = int(math.sin(self._offset * 0.1) * 5)
            self.root.geometry(f"+{self.base_x}+{self.base_y + dy}")
        self.root.after(50, self.animate)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    pet = TablePet()
    pet.run()