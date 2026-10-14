# table_pet.py
import os
import math
import threading
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
        self.is_processing = False

        # 浮动动画
        self.base_x = 800
        self.base_y = 400
        self._offset = 0

        self.pet_image = self.load_pet_image()
        self.setup_ui()
        self.bind_events()
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

        self.status_label = tk.Label(self.root, text="拖 PDF 给我翻译",
                                     font=("微软雅黑", 9),
                                     bg='#2b2b2b', fg='#00ffcc', bd=0)
        self.status_label.place(relx=0.5, rely=0.92, anchor='center')

    def bind_events(self):
        self.root.bind("<ButtonPress-1>", self.on_press)
        self.root.bind("<B1-Motion>", self.on_drag)
        self.root.bind("<ButtonRelease-1>", self.on_release)
        self.root.bind("<Button-3>", self.show_menu)

        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="退出", command=self.root.destroy)

        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_drop)

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
        if self.is_processing:
            self.status_label.config(text="正在处理，请稍候...")
            return
        file_path = event.data.strip('{}')
        if not file_path.lower().endswith('.pdf'):
            self.status_label.config(text="只支持 PDF")
            return

        self.is_processing = True
        threading.Thread(target=self._process_pdf, args=(file_path,), daemon=True).start()

    def _process_pdf(self, file_path):
        """后台线程：提取 + 翻译 + 导出"""
        filename = os.path.basename(file_path)
        title = os.path.splitext(filename)[0]

        try:
            from pdf_reader import extract_text_from_pdf
            from translator import translate_text
            from exporter import export_markdown, export_pdf

            # 1. 提取
            self._set_status("提取中...")
            text = extract_text_from_pdf(file_path)
            if not text:
                self._set_status("提取失败（可能是扫描版）")
                return

            # 2. 翻译
            self._set_status("翻译中...")
            translated, stats = translate_text(text)

            # 3. 导出
            self._set_status("导出中...")
            out_dir = os.path.join(os.path.dirname(__file__), "output")
            os.makedirs(out_dir, exist_ok=True)

            md_path = os.path.join(out_dir, f"{title}_中文.md")
            pdf_path = os.path.join(out_dir, f"{title}_中文.pdf")

            export_markdown(translated, stats, title, md_path)
            export_pdf(translated, stats, title, pdf_path)

            # 4. 显示状态
            self._set_status(f"{stats['status']} {stats['success']}/{stats['total']}")
            print(f"已保存：{md_path}")
            print(f"已保存：{pdf_path}")

        except Exception as e:
            print(f"处理失败：{e}")
            self._set_status("处理失败")
        finally:
            self.is_processing = False

    def _set_status(self, text):
        """线程安全地更新状态栏"""
        self.root.after(0, lambda: self.status_label.config(text=text))

    def animate(self):
        """桌宠浮动动画（拖动时暂停）——频率与最初第一版一致"""
        if not self.is_dragging:
            self._offset += 1
            dy = int(math.sin(self._offset * 0.1) * 5)
            self.root.geometry(f"+{self.base_x}+{self.base_y + dy}")
        self.root.after(50, self.animate)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    TablePet().run()