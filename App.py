import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Frame, Tk

from Converter_Multi import Converter


# from tkinter.scrolledtext import ScrolledText

# from Converter_Async import Converter


class App(Converter, ttk.Frame):

    def __init__(self, folder_path, save_path, master=None):
        Converter.__init__(self, folder_path, save_path)
        ttk.Frame.__init__(self, master)
        self.switch = None
        self.tab1 = None
        self.tab2 = None
        self.tab3 = None
        self.tab4 = None
        self.tab5 = None
        self.tab6 = None
        self.notebook_style = None
        self.notebook_01 = None
        self.btn06 = None
        self.folder = None
        self.tree_frame = None
        self.canvas = None
        self.scrollbar = None
        self.label_tip4 = None
        self.file_path = None
        self.btn05 = None
        self.btn04 = None
        self.label_tip3 = None
        self.label_tip2 = None
        self.label_tip1 = None
        self.btn03 = None
        self.btn02 = None
        self.btn01 = None
        self.tree = None
        self.root = None
        self.label01 = None
        self.check_mutil = None
        self.check_ncm = None
        self.check_mgg = None
        self.check_kgm = None
        self.check_uc = None
        self.check_meta = None
        self.mode = 'audio'
        self.master = master

        self.__author__ = 'Jerry Liao'
        self.__version__ = 'Ver 2.1.0'
        self.__data__ = '2023-11-19'
        self.create_widgets()
        self.pack()

    # TODO: 创建组件
    def create_widgets(self):
        self.label01 = ttk.Label(self, text=f'{" " * 10}音频格式转换器{" " * 10}', font=('微软雅黑', 20),
                                 background='#F5F5F5')
        self.label01.pack(pady=10)
        style_switch = ttk.Style()
        style_switch.configure("Switch.TCheckbutton", font=('微软雅黑', 10))

        self.switch = ttk.Checkbutton(
            self, text="网易云模式", style="Switch.TCheckbutton", variable=self.netease_mode,
            command=self.netease_mode_switch
        )

        self.switch.place(x=0, y=15)

        def tree():
            self.tree_frame = Frame(self)

            style = ttk.Style()
            style.configure("Treeview", font=('微软雅黑', 10), width=100)
            scroll_bar = ttk.Scrollbar(self.tree_frame)
            scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
            self.tree = ttk.Treeview(self.tree_frame, height=8, style="Treeview",
                                     columns=("column1",), yscrollcommand=scroll_bar.set)
            self.tree_frame.pack()

            style_head = ttk.Style()
            style_head.configure("Treeview.Heading", font=("黑体", 10), backgroud='gray')
            # 设置每一列的标题
            self.tree.heading("#0", text="音频文件树形图", anchor='center')
            self.tree.column("#0", width=855, stretch=True)
            self.tree.pack(expand=True, fill='both', pady=10)
            scroll_bar.config(command=self.tree.yview)
            self.tree_view()

        def notebook_set():
            # 创建Style对象
            self.notebook_style = ttk.Style(self)
            # 设置标签页的大小
            # 创建Notebook
            self.notebook_style.configure('TNotebook.Tab', font=('华文细黑', 12), background='white')
            self.notebook_01 = ttk.Notebook(self, height=200, width=500)
            self.notebook_01.pack(fill="both", expand=True)

            # 创建标签页
            self.tab1 = ttk.Frame(self.notebook_01, borderwidth=2, relief='flat', style='TNotebook.Tab')
            self.tab2 = ttk.Frame(self.notebook_01, borderwidth=2, relief='flat', style='TNotebook.Tab')
            self.tab3 = ttk.Frame(self.notebook_01, borderwidth=2, relief='flat', style='TNotebook.Tab')
            self.tab4 = ttk.Frame(self.notebook_01, borderwidth=2, relief='flat', style='TNotebook.Tab')
            self.tab5 = ttk.Frame(self.notebook_01, borderwidth=2, relief='flat', style='TNotebook.Tab')
            self.tab6 = ttk.Frame(self.notebook_01, borderwidth=2, relief='flat', style='TNotebook.Tab')
            self.notebook_01.add(self.tab1, text='控制')
            self.notebook_01.add(self.tab6, text='路径')
            self.notebook_01.add(self.tab3, text='选项')
            # self.notebook_01.add(self.tab5, text='输出')
            self.notebook_01.add(self.tab2, text='关于')
            self.notebook_01.add(self.tab4, text='日志')

            style_btn = ttk.Style()
            style_btn.configure('TButton', font=('黑体', 15), padding=9)

        def tag_operate():
            label_op = ttk.Label(self.tab1, text='--------控制--------', font=('华文细黑', 15),
                                 background='#E6E6E6')
            label_op.pack(pady=(20, 25))

            tab1_frame = ttk.Frame(self.tab1, style="Info.TLabel")
            tab1_frame.pack()
            self.btn01 = ttk.Button(tab1_frame, text='开始转换', style='TButton',
                                    command=lambda: self.new_thread(self.main))
            self.btn01.pack(side='left', padx=(25, 5), pady=5)

            self.btn02 = ttk.Button(tab1_frame, text='添加目录', style='TButton',
                                    command=lambda: self.new_thread(self.select_dir))
            self.btn02.pack(side='left', padx=5)

            self.btn04 = ttk.Button(tab1_frame, text='使用须知', style='TButton',
                                    command=lambda: self.show_info('使用须知',
                                                                   f'被转换的文件需要被放在{self.folder_path}目录下, 转换后的文件会保存在{self.save_path}目录下'))
            self.btn04.pack(side='left', padx=5)

            self.btn05 = ttk.Button(tab1_frame, text='切换目录', style='TButton',
                                    command=lambda: self.new_thread(self.change_tree_mode))
            self.btn05.pack(side='left', padx=5)
            self.btn06 = ttk.Button(tab1_frame, text='清空目录', style='TButton',
                                    command=lambda: self.new_thread(self.del_dir()))
            self.btn06.pack(side='left', padx=5)

            self.btn03 = ttk.Button(tab1_frame, text='退  出', style='TButton', command=self.master.destroy)
            self.btn03.pack(side='left', padx=5)

        def tag_options():
            self.check_frame = ttk.Frame(self.tab3, style='Info.TLabel')
            label_opt = ttk.Label(self.check_frame, text='--------选项--------', font=('华文细黑', 15),
                                  background='#E6E6E6')
            label_opt.pack(pady=(20, 25))
            self.check_frame.pack(fill='both', expand=True)
            child_frame = ttk.Frame(self.check_frame, style='Info.TLabel')
            child_frame.pack()
            self.check_btn = ttk.Style()
            self.check_btn.configure('Check.TCheckbutton', background='#E6E6E6')
            self.check_mutil = ttk.Checkbutton(
                child_frame, text="多线程运行", variable=self.multithread, style='Check.TCheckbutton'
            )
            self.check_mutil.pack(side='left', anchor='center')

            self.check_ncm = ttk.Checkbutton(
                child_frame, text="Ncm转换", variable=self.ncm_execute, style='Check.TCheckbutton'
            )
            self.check_ncm.pack(side='left')

            self.check_mgg = ttk.Checkbutton(
                child_frame, text="Mgg转换", variable=self.qqm_execute, style='Check.TCheckbutton'
            )
            self.check_mgg.pack(side='left')

            self.check_kgm = ttk.Checkbutton(
                child_frame, text="Kgm转换", variable=self.kgm_execute, style='Check.TCheckbutton'
            )
            self.check_kgm.pack(side='left')
            self.check_uc = ttk.Checkbutton(
                child_frame, text="Uc转换", variable=self.uc_execute, style='Check.TCheckbutton'
            )
            self.check_uc.pack(side='left')

            self.check_meta = ttk.Checkbutton(
                child_frame, text="提取元数据", variable=self.mata_execute, style='Check.TCheckbutton'
            )
            self.check_meta.pack(side='left')

        def tag_info():
            self.label_style = ttk.Style()
            self.label_style.configure('Info.TLabel', background='#E6E6E6')
            label_opt = ttk.Label(self.tab2, text='--------关于--------', font=('华文细黑', 15),
                                  background='#E6E6E6')
            label_opt.pack(pady=(20, 25))
            self.label_tip1 = ttk.Label(self.tab2, text='本程序支持对ncm, kgm, mgg加密格式的转换', font=('宋体', 15),
                                        style='Info.TLabel')
            self.label_tip1.pack(pady=(4, 7), anchor='s')

            self.label_tip3 = ttk.Label(self.tab2, text=f'作者: {self.__author__}', font=('宋体', 15),
                                        style='Info.TLabel')
            self.label_tip3.pack(pady=7)

            self.label_tip4 = ttk.Label(self.tab2, text=f'当前版本: {self.__version__}', font=('宋体', 15),
                                        style='Info.TLabel')
            self.label_tip4.pack(pady=7)

        def tag_log():
            label_op = ttk.Label(self.tab4, text='--------日志--------', font=('华文细黑', 15),
                                 background='#E6E6E6')
            label_op.pack(pady=(20, 15))
            update_log = (f"""
            {self.__version__} ({self.__data__}):
                1. 全面更新了UI设计
                2. 自定义性增强
                3. 增加了对网易云uc缓存格式的支持
                4. 实现了路径的显式变更
            """)

            label_log = ttk.Label(self.tab4, text=update_log, font=('宋体', 15), style='Info.TLabel')
            label_log.pack(side='left', padx=200, anchor='n')

        def tab_path():
            label_path = ttk.Label(self.tab6, text='--------路径--------', font=('华文细黑', 15),
                                   background='#E6E6E6')
            label_path.pack(pady=(20, 15))

            def set_path():
                ori_folder = self.folder_path
                ori_save = self.save_path
                if os.path.isdir(entry_input_path.get().strip('"')) and os.path.isdir(
                        entry_output_path.get().strip('"')):
                    self.folder_path = entry_input_path.get().strip('"')
                    self.save_path = entry_output_path.get().strip('"')
                    messagebox.showinfo('提示', '成功!')
                    self.tree.delete(*self.tree.get_children())
                    self.tree_view()
                else:
                    messagebox.showinfo('提示', '请正确输入路径!')
                    text_clear(entry_input_path)
                    text_clear(entry_output_path)
                    entry_input_path.insert(0, ori_folder)
                    entry_output_path.insert(0, ori_save)
                # print(entry_input_path.get())
                # print(entry_output_path.get(), type(entry_output_path.get()))

            def text_clear(button):
                button.delete(0, tk.END)

            button_style = ttk.Style()
            button_style.configure('Tab.TButton', font=('华文细黑', 12))

            frame_input = ttk.Frame(self.tab6, style='Info.TLabel')
            frame_input.pack(pady=7)
            label_input = ttk.Label(frame_input, text='输入路径: ', font=('黑体', 12), background='#E6E6E6')
            label_input.pack(side='left')
            entry_input_path = ttk.Entry(frame_input, style='Tab.TEntry')
            entry_input_path.insert(0, self.folder_path)
            entry_input_path.pack(side='left')
            button_input_clear = ttk.Button(
                frame_input, text='清空', width=4, padding=2, style='Tab.TButton',
                command=lambda: text_clear(entry_input_path)
            )
            button_input_clear.pack(side='left', padx=3)

            frame_output = ttk.Frame(self.tab6, style='Info.TLabel')
            frame_output.pack(pady=10)
            label_output = ttk.Label(frame_output, text='输出路径: ', font=('黑体', 12), background='#E6E6E6')
            label_output.pack(side='left')
            entry_output_path = ttk.Entry(frame_output, style='Tab.TEntry')
            entry_output_path.insert(0, self.save_path)
            entry_output_path.pack(side='left')
            button_output_clear = ttk.Button(
                frame_output, text='清空', width=4, padding=2, style='Tab.TButton',
                command=lambda: text_clear(entry_output_path)
            )
            button_output_clear.pack(side='left', padx=3)

            button_confirm = ttk.Button(self.tab6, text='确定', style='Tab.TButton', command=set_path, padding=2)
            button_confirm.pack()

        # def tag_output():
        #     text_area = ScrolledText(self.tab5, wrap='word', width=120, height=10, state='disabled', background='gray')
        #     text_area.insert(tk.INSERT, 'Hello World')
        #     text_area.pack(pady=20)
        #     text_area.focus_set()
        # text_area.mainloop()

        # 设置树形图
        tree()
        # 设置标签格
        notebook_set()
        # 设置"控 制"标签
        tag_operate()
        # 设置"选 项"标签
        tag_options()
        # 设置"关 于"标签
        tag_info()
        # 设置"日 志"标签
        tag_log()
        # 设置"路 径"标签
        tab_path()
        # 设置"输 出"标签
        # tag_output()

    # TODO: 设置网易云模式切换按钮
    def netease_mode_switch(self):
        if messagebox.askquestion(
                '提示', f'''
                你确定要进入网易云模式吗?
                网易云模式将针对网易云缓存UA格式进行专门转换
                并通过Internet获取音乐信息并改名
                '''
        ) == 'yes':

            self.label01['background'] = 'red'
            self.label01['foreground'] = 'white'
            label_ne_mode = ttk.Label(self.tab3, text='网易云模式已开启', font=('宋体', 12), background='#E6E6E6')
            label_ne_mode.pack(pady=0)

            def disabled(check: ttk.Checkbutton, var: tk.BooleanVar):
                check['state'] = "disabled"
                var.set(False)

            check_var_list = [
                (self.check_mgg, self.qqm_execute),
                (self.check_kgm, self.kgm_execute),
                (self.check_ncm, self.ncm_execute)
            ]
            for tp in check_var_list:
                disabled(check=tp[0], var=tp[1])
            self.switch['state'] = 'disabled'
            self.check_meta['state'] = 'disabled'
            self.check_uc['state'] = 'disabled'
            self.check_mutil['state'] = 'disabled'
        else:
            self.netease_mode.set(False)

    # TODO: 改变树形图文件内容
    def change_tree_mode(self):
        def change():
            if self.mode == 'audio':
                self.mode = 'save'
            else:
                self.mode = 'audio'
            try:
                self.tree_view(True)
            except tk.TclError:
                pass

        self.new_thread(change)

    # TODO: 创建树形图
    def tree_view(self, remake=False):

        if self.mode == 'audio':
            self.folder = self.folder_path
        else:
            self.folder = self.save_path

        def load_tree(parent, path):
            count = 0
            for filepath in os.listdir(path):
                # 文件的绝对路径
                abs_file_path = os.path.join(path, filepath)

                # 判断是否是目录,是目录再去添加树枝,使用递归
                if os.path.isdir(abs_file_path):
                    # 插入树枝
                    tree = self.tree.insert(parent, "end", text=get_last_path(filepath), tags="separator")
                    load_tree(tree, abs_file_path)
            # 再处理没有子树的文件
            for filepath in sorted(os.listdir(path)):
                # 文件的绝对路径
                abs_file_path = os.path.join(path, filepath)

                # 判断是否是目录,是目录已经处理过了，不再处理
                if not os.path.isdir(abs_file_path):
                    # 插入树枝
                    self.tree.insert(parent, "end", text=get_last_path(filepath))
                    count += 1
                    if count == 50:
                        break

        # 求文件的最后一个名字
        def get_last_path(path):
            path_list = os.path.split(path)
            return path_list[-1]

        self.root = self.tree.insert("", "end", text=get_last_path(self.folder), open=True)
        if not remake:
            load_tree(self.root, self.folder)
        else:
            self.tree.delete(*self.tree.get_children())
            self.root = self.tree.insert("", "end", text=get_last_path(self.folder), open=True)
            load_tree(self.root, self.folder)

    @staticmethod
    def show_info(title, content):
        messagebox.showinfo(title, content)

    # TODO: "添加文件"功能
    def select_dir(self):
        file_path = filedialog.askdirectory()
        if file_path:
            try:
                for root, dirs, files in os.walk(file_path):
                    for file in files:
                        src_file = os.path.join(root, file)  # 构造源文件路径
                        rel_path = os.path.relpath(src_file, file_path)  # 获取源文件相对于源目录的路径
                        dst_file = os.path.join(self.folder_path, rel_path)  # 构造目标文件路径
                        os.makedirs(os.path.dirname(dst_file), exist_ok=True)  # 创建目标文件所在的目录
                        shutil.copy(src_file, dst_file)  # 复制文件
                self.tree_view(True)
            except FileNotFoundError as e:
                print(f"FileNotFoundError: {e}")
            except FileExistsError as e:
                print(f"FileExistsError: {e}")
            except PermissionError as e:
                print(f"PermissionError: {e}")
                messagebox.showinfo('警告', '权限不足, 请尝试手动复制')

    # TODO: 清空目录
    def del_dir(self):
        if messagebox.askquestion('提示', f'你确定要清空目录{self.folder}吗?') == 'yes':
            # 获取目录下所有文件名
            file_list = os.listdir(self.folder)
            error = False
            # 遍历文件列表并删除文件
            for file_name in file_list:
                file_path = os.path.join(self.folder, file_name)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        # 如果是目录，则递归删除其内容
                        shutil.rmtree(file_path)
                except PermissionError:
                    error = True
                    messagebox.showinfo('提示', '部分文件权限不足, 请手动删除!')
            if not error:
                messagebox.showinfo('提示', f'目录{self.folder}已清空')
            self.tree_view(True)


window = Tk()


def main(dir_input, dir_output):
    global window
    try:
        window.call('source', r'Azure-ttk-theme-main\azure.tcl')
        window.call('set_theme', 'light')
    except tk.TclError:
        pass
    window.geometry('870x550+500+250')
    window.title('AutoMusicConverter')
    window.resizable(False, False)
    # 设置图标
    # window.iconbitmap('AutoMusicConv-Icon.ico')
    conv = App(dir_input, dir_output, master=window)
    conv.mainloop()
