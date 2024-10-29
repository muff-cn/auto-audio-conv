import os
import shutil
import subprocess
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from time import time
from tkinter import messagebox
import eyed3
from xm_decrypt import main
from Netease_Mode import info_get

"""
测试情况 (文件数 70) :

进程池 25: 45.607s
进程池 30: 43.543s
进程池 40: 44.885s
进程池 50: 44.107s
进程池 70: 47.103s

结果: 线程池数量: 30
"""


class Converter:

    def __init__(self, folder_path, save_path=None):
        self.folder_path = folder_path
        self.save_path = save_path
        os.makedirs(self.folder_path, exist_ok=True)  # 创建新目录
        os.makedirs(self.save_path, exist_ok=True)  # 创建新目录
        self.mgg_list = list()
        self.uc_list = list()
        self.mp3_list = list()
        self.pool_num = 25
        self.multithread = tk.BooleanVar(value=True)
        self.kgm_execute = tk.BooleanVar(value=True)
        self.ncm_execute = tk.BooleanVar(value=True)
        self.qqm_execute = tk.BooleanVar(value=True)
        self.uc_execute = tk.BooleanVar(value=True)
        self.mata_execute = tk.BooleanVar(value=True)  # 是否元数据提取
        self.netease_mode = tk.BooleanVar(value=False)

    # TODO: 获取各文件的绝对路径
    @staticmethod
    def get_abspath(path):
        return os.path.abspath(path)

    # TODO: 实现对ncm, mgg, kgm加密格式的转换
    def encryption_convert(self):
        # rela_path = r'tools/ffmpeg_x64.exe'
        # abs_path = self.get_abspath(rela_path).replace("""\\""", """\\\\""")
        # AudioSegment.converter = abs_path
        # ncm_path = self.get_abspath('tools\\numdump.exe')
        qmc_path = self.get_abspath(r'tools/um.exe')
        kgm_path = self.get_abspath(r'tools/kgmunlock.exe')

        def conv(file, file_path):
            if os.path.exists(f'{self.save_path}\\{file.split(".")[0]}.mp3') and not self.netease_mode:
                # print(file_path)
                return None
            if file_path.endswith('.ncm'):
                # print(file_path)
                if self.ncm_execute.get():
                    ncm_path = 'tools/ncmdump.exe'
                    process = subprocess.Popen([ncm_path, file_path], shell=False)
                    process.wait()
                    try:
                        shutil.move(os.path.splitext(file_path)[0] + '.mp3',
                                    f'{self.save_path}\\{os.path.splitext(file)[0]}.mp3')
                    except FileNotFoundError:
                        # shutil.move(os.path.splitext(file_path)[0] + '.flac',
                        #             f'{self.save_path}\\{os.path.splitext(file)[0]}.mp3')
                        pass
            elif file_path.endswith('.mgg'):
                self.mgg_list.append(file_path)
                if self.qqm_execute.get():
                    if not os.path.exists(file_path.replace('.mgg', '.ogg')):
                        process = subprocess.Popen([qmc_path, file_path], shell=False)
                        process.wait()
                        try:
                            file = file.split(".")[0] + ".ogg"
                            shutil.move(file, f'{self.folder_path}//{file}')
                        except FileNotFoundError as e:
                            print(f'A error occurs while running mgg codes: {e}')

            elif file_path.endswith('.kgm'):

                if self.kgm_execute.get():
                    process = subprocess.Popen([kgm_path, file_path], shell=False)
                    process.wait()
                    shutil.move(file.replace(".kgm", ".mp3"), f'{self.save_path}\\{os.path.splitext(file)[0]}.mp3')
                    # print(file_path)

            elif file_path.endswith('.uc'):
                if self.uc_execute.get():
                    # 将当前文件按字节与0xA3进行异或，并对文件格式进行修改
                    f_source = open(file_path, 'rb')
                    f_out = open(file_path[:-3] + '.flac', 'wb')
                    content = bytearray(f_source.read())
                    for index in range(len(content)):
                        content[index] ^= 0xA3
                    f_out.write(content)
                    f_source.close()
                    f_out.close()
                    self.uc_list.append(file)
                    print(f'{file_path} Successfully converted')

            elif file_path.endswith('.xm'):
                main(file_path, self.folder_path)
        with ThreadPoolExecutor(self.pool_num) as t:
            for root, dirs, files in os.walk(self.folder_path):
                for _file in files:
                    _file_path = os.path.join(root, _file)
                    if self.multithread.get():
                        t.submit(conv, _file, _file_path)
                    else:
                        conv(_file, _file_path)

    # TODO: 实现对一般音乐格式的转换
    def normal_convert(self):
        # sth = False
        # if sth:
        #     pass
        # else:
        rela_path = r'tools/ffmpeg_x64.exe'
        abs_path = self.get_abspath(rela_path).replace("""\\""", """\\\\""")

        def norm_conv(file, file_path):
            if os.path.exists(f'{self.save_path}\\{file.split(".")[0]}.mp3'):
                return None
            # elif file_path.endswith('.ogg'):
            #     pass
            elif file_path.endswith('.mp3'):
                self.mp3_list.append(file)

            elif not file_path.endswith('.mgg') and not file_path.endswith('.ncm') and not file_path.endswith(
                    '.kgm') and not file_path.endswith('.mp3') and not file_path.endswith('.uc') and not file_path.endswith('.xm'):
                try:
                    cmd = [abs_path, '-i', file_path, '-vn', '-acodec', 'libmp3lame', '-ab', '320k',
                           f'{self.save_path}\\{os.path.splitext(file)[0]}.mp3']
                    subprocess.run(cmd, shell=True, check=True)
                    if file.endswith('.ogg') and file_path.replace('.ogg', '.mgg') in self.mgg_list:
                        os.remove(file_path)

                except Exception or FileNotFoundError as e:
                    print(f'{e} | A error occurs while the program is running!')

        with ThreadPoolExecutor(self.pool_num) as t:
            for root, dirs, files in os.walk(self.folder_path):
                for _file in files:
                    _file_path = os.path.join(root, _file)

                    if self.multithread.get():
                        t.submit(norm_conv, _file, _file_path)
                    else:
                        norm_conv(_file, _file_path)

    # TODO: 提取音乐元数据并加入至文件名并移动至保存目录
    def extract_metadata_and_rename_folder(self):
        for root, dirs, files in os.walk(self.folder_path):
            for filename in files:
                if filename.endswith('.uc'):
                    # print(file_path.replace('.uc', '.flac'))
                    try:
                        new_filename = filename
                        new_filepath = os.path.join(self.folder_path, new_filename)
                        os.remove(new_filepath.replace('.uc', '.flac'))
                    except FileNotFoundError:
                        pass
                if filename.endswith(".mp3"):

                    new_filename = filename
                    new_filepath = os.path.join(self.save_path, new_filename)
                    mp3_file = os.path.join(self.folder_path, filename)
                    if filename not in self.mp3_list:
                        shutil.move(mp3_file, new_filepath)  # 复制文件到新目录
                    else:
                        shutil.copy(mp3_file, new_filepath)

        if self.mata_execute.get():

            def get_mata(_filename, music_id):

                if ' - ' not in _filename:
                    mp3_file_ = os.path.join(self.save_path, _filename)

                    try:

                        # audio = EasyID3(mp3_file_)
                        # title = audio.get('title', [''])[0]
                        # artist = audio.get('artist', [''])[0]
                        if music_id is not None:
                            artist, title = info_get(music_id)
                        else:
                            audio = eyed3.load(mp3_file_)
                            artist = audio.tag.artist.encode('utf-8').decode('utf-8')
                            title = audio.tag.title.encode('utf-8').decode('utf-8')
                    except Exception or NameError:
                        print(_filename, '提取元数据出错')
                        # audio = eyed3.load(mp3_file_)
                        # artist = audio.tag.artist
                        # title = audio.tag.title
                    else:
                        new_filename_ = f"{artist} - {title}.mp3"
                        new_filepath_ = os.path.join(self.save_path, new_filename_)
                        if artist is not None and title is not None:
                            os.rename(mp3_file_, new_filepath_)
                            print(f'{new_filepath_} Successfully renamed')
                else:
                    return None

            with ThreadPoolExecutor(30) as t:
                for filename_ in os.listdir(self.save_path):
                    if os.path.basename(filename_).replace('.mp3', '.uc') in self.uc_list:
                        dirname, name = os.path.split(filename_)
                        # print(dirname, name)
                        song_id = name.split('-')[0]
                    else:
                        song_id = None
                    t.submit(get_mata, filename_, song_id)

    @staticmethod
    def new_thread(func):
        Thread(target=func).start()

    def main(self):
        start = time()
        self.encryption_convert()
        self.normal_convert()
        self.extract_metadata_and_rename_folder()
        end = time()
        run_time = end - start
        print(f'运行用时: {run_time:.3f}s')
        messagebox.showinfo('提示', '转换完成!')
        # self.mgg_list = list()
        # self.uc_list = list()
        self.mp3_list = list()
