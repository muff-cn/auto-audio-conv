import os

from mutagen.mp3 import MP3
import mutagen

# 定义一个函数来检测MP3文件是否损坏
def is_mp3_corrupted(mp3_file):
    try:
        audio = MP3(mp3_file)
        return False
    except mutagen.mp3.HeaderNotFoundError:
        return True


_count = 0
# 定义要检测的文件夹路径
folder_path = r"tools"

# 获取文件夹内所有文件的列表
file_list = os.listdir(folder_path)

# 遍历文件列表，检查每个文件是否为MP3文件并检查是否损坏
for file_name in file_list:
    if file_name.endswith(".mp3"):
        file_path = os.path.join(folder_path, file_name)
        if is_mp3_corrupted(file_path):
            print(f"损坏的MP3文件：{file_name}")
            _count += 1

if not _count:
    print('无损坏MP3文件')
