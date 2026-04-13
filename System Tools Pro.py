import tkinter as tk
from tkinter import messagebox
import os, webbrowser, shutil, threading

class SystemToolsApp:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.build_ui()
        self.animate_load()

    def setup_window(self):
        self.root.title("⚡ System Tools Pro")
        self.root.geometry("620x780")
        self.root.configure(bg="#1e1e2f")
        self.root.resizable(False, False)
        # أيقونة اختيارية (يمكنك إزالتها إذا لم تكن موجودة)
        # self.root.iconbitmap("icon.ico")

    def build_ui(self):
        # 🎨 الهيدر
        self.header = tk.Label(self.root, text="🛠️ لوحة التحكم السريعة", 
                               font=("Segoe UI", 24, "bold"), bg="#1e1e2f", fg="#00d4ff")
        self.header.pack(pady=(20, 5))
        self.subheader = tk.Label(self.root, text="أدوات النظام والصيانة في مكان واحد", 
                                  font=("Segoe UI", 11), bg="#1e1e2f", fg="#8a8a9a")
        self.subheader.pack(pady=(0, 20))

        # 📦 حاوية الأقسام
        self.container = tk.Frame(self.root, bg="#1e1e2f")
        self.container.pack(fill="both", expand=True, padx=25)

        self.all_buttons = []
        self.sections = [
            ("🖥️ إعدادات النظام", [
                ("⚡ خيارات الطاقة", lambda: os.system("powercfg.cpl")),
                ("🖥️ إعدادات العرض", lambda: os.system("desk.cpl")),
                ("📦 البرامج المثبتة", lambda: os.system("appwiz.cpl")),
                ("🌐 محولات الشبكة", lambda: os.system("ncpa.cpl")),
                ("🌍 المنطقة واللغة", lambda: os.system("intl.cpl")),
                ("💻 معلومات النظام", lambda: os.system("msinfo32"))
            ]),
            ("🎮 التعريفات والأدوات", [
                ("🎮 تعريفات NVIDIA", lambda: webbrowser.open("https://nvidia.com/drivers")),
                ("🔵 تعريفات AMD", lambda: webbrowser.open("https://amd.com/support")),
                ("⌨️ لوحة المفاتيح", lambda: threading.Thread(target=lambda: os.system("osk.exe")).start())
            ]),
            ("🧹 الصيانة والتنظيف", [
                ("🗑️ حذف الملفات المؤقتة", self.remove_temp),
                ("📊 تنظيف %TEMP%", self.clear_temp_percent)
            ]),
            ("🎨 اختبار الشاشات", [
                ("🔴 شاشة حمراء", lambda: self.test_screen("red")),
                ("🟢 شاشة خضراء", lambda: self.test_screen("green")),
                ("🔵 شاشة زرقاء", lambda: self.test_screen("blue")),
                ("⚪ شاشة بيضاء", lambda: self.test_screen("white"))
            ])
        ]

        for title, items in self.sections:
            self.add_section(title, items)

        # 📊 شريط الحالة
        self.status_var = tk.StringVar(value="✅ جاهز للاستخدام")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, 
                                   font=("Segoe UI", 9), bg="#1e1e2f", fg="#8a8a9a")
        self.status_bar.pack(pady=(10, 15))

    def add_section(self, title, items):
        # عنوان القسم
        header = tk.Label(self.container, text=title, font=("Segoe UI", 13, "bold"), 
                          bg="#2d2d44", fg="#e0e0ff", anchor="w", padx=12, pady=6)
        header.pack(fill="x", pady=(12, 2))

        # إطار الأزرار
        btn_frame = tk.Frame(self.container, bg="#1e1e2f")
        btn_frame.pack(fill="x", pady=(0, 8))

        for i, (txt, cmd) in enumerate(items):
            btn = tk.Button(btn_frame, text=txt, font=("Segoe UI", 10, "bold"), 
                            bg="#3a3a5c", fg="#ffffff", relief="flat", bd=0, 
                            padx=12, pady=9, cursor="hand2", command=cmd)
            btn.grid(row=i//2, column=i%2, padx=6, pady=5, sticky="ew")
            self.all_buttons.append(btn)

        # توسيع الأعمدة تلقائياً
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)

    # ✨ أنيمشن ظهور النافذة
    def animate_load(self):
        self.root.attributes("-alpha", 0)
        def fade(step=0):
            if step <= 10:
                self.root.attributes("-alpha", step/10)
                self.root.after(40, lambda: fade(step+1))
            else:
                self.stagger_buttons()
        fade()

    # ✨ ظهور الأزرار واحداً تلو الآخر
    def stagger_buttons(self):
        for i, btn in enumerate(self.all_buttons):
            btn.config(state="disabled")
            def enable(b=btn):
                b.config(state="normal")
                self.apply_hover_effect(b)
            self.root.after(i * 70, enable)

    # ✨ تأثير Hover + Click
    def apply_hover_effect(self, btn):
        btn.bind("<Enter>", lambda e: btn.config(bg="#4a4a7a"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#3a3a5c"))
        btn.bind("<Button-1>", lambda e: btn.config(bg="#6a6a9a"))
        btn.bind("<ButtonRelease-1>", lambda e: btn.config(bg="#4a4a7a"))

    # 🧹 تنظيف الملفات المؤقتة (يعمل في خلفية غير متزامنة)
    def remove_temp(self):
        if not messagebox.askyesno("⚠️ تأكيد", "هل تريد حذف جميع الملفات المؤقتة؟"):
            return
        self.status_var.set("🔄 جاري الحذف...")
        threading.Thread(target=self._remove_temp_task, daemon=True).start()

    def _remove_temp_task(self):
        paths = [os.environ.get("TEMP"), os.environ.get("TMP"), r"C:\Windows\Temp"]
        f_cnt = d_cnt = 0
        for p in paths:
            if not p or not os.path.exists(p): continue
            for item in os.listdir(p):
                fp = os.path.join(p, item)
                try:
                    if os.path.isfile(fp) or os.path.islink(fp): os.unlink(fp); f_cnt += 1
                    elif os.path.isdir(fp): shutil.rmtree(fp); d_cnt += 1
                except: pass
        self.root.after(0, lambda: self.show_toast(f"✅ تم حذف {f_cnt} ملف و {d_cnt} مجلد"))

    def clear_temp_percent(self):
        if not messagebox.askyesno("⚠️ تأكيد", "هل تريد حذف ملفات %TEMP%؟"):
            return
        self.status_var.set("🔄 جاري الحذف...")
        threading.Thread(target=self._clear_temp_task, daemon=True).start()

    def _clear_temp_task(self):
        temp_path = os.path.expandvars("%TEMP%")
        deleted = 0
        if os.path.exists(temp_path):
            for item in os.listdir(temp_path):
                fp = os.path.join(temp_path, item)
                try:
                    if os.path.isfile(fp) or os.path.islink(fp): os.unlink(fp)
                    else: shutil.rmtree(fp)
                    deleted += 1
                except: pass
        self.root.after(0, lambda: self.show_toast(f"✅ تم حذف {deleted} عنصر"))

    # 📢 إشعار منبثق غير متوقف
    def show_toast(self, msg):
        toast = tk.Toplevel(self.root)
        toast.overrideredirect(True)
        toast.configure(bg="#2d8c4c")
        tk.Label(toast, text=msg, font=("Segoe UI", 10, "bold"), 
                 bg="#2d8c4c", fg="white", padx=15, pady=8).pack()
        x = self.root.winfo_x() + (self.root.winfo_width() - toast.winfo_reqwidth()) // 2
        y = self.root.winfo_y() + self.root.winfo_height() // 2
        toast.geometry(f"+{x}+{y}")
        toast.attributes("-alpha", 0)
        toast.attributes("-topmost", True)

        def fade_in(step=0):
            if step <= 8:
                toast.attributes("-alpha", step/8)
                toast.after(30, lambda: fade_in(step+1))
            else:
                self.root.after(2500, lambda: fade_out(toast))
        fade_in()

        def fade_out(w):
            def step(n=8):
                if n >= 0:
                    w.attributes("-alpha", n/8)
                    w.after(30, lambda: step(n-1))
                else: w.destroy()
            step()
        self.status_var.set("✅ جاهز للاستخدام")

    # 🎨 اختبار الشاشات
    def test_screen(self, color):
        win = tk.Toplevel(self.root)
        win.attributes("-fullscreen", True)
        win.configure(bg=color)
        win.attributes("-alpha", 0)
        def fade(step=0):
            if step <= 10:
                win.attributes("-alpha", step/10)
                win.after(40, lambda: fade(step+1))
        fade()
        btn = tk.Button(win, text="✕ خروج (Esc)", font=("Segoe UI", 12, "bold"),
                        bg="black", fg=color, relief="flat", bd=0, padx=20, pady=10, cursor="hand2")
        btn.pack(side="bottom", pady=30)
        btn.bind("<Button-1>", lambda e: win.destroy())
        win.bind("<Escape>", lambda e: win.destroy())

if __name__ == "__main__":
    root = tk.Tk()
    try:
        app = SystemToolsApp(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("خطأ", f"حدث خطأ غير متوقع:\n{e}")