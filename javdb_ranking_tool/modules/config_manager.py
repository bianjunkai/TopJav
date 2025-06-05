import configparser
import os

def load_config(html_root_folder_arg=None, local_movie_folder_arg=None):
    """
    读取或初始化配置文件，返回配置字典。
    优先使用命令行参数，否则读取config.ini，没有则引导用户输入并写入。
    """
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.ini')
    config = configparser.ConfigParser()
    # 优先用命令行参数
    html_root_folder = html_root_folder_arg
    local_movie_folder = local_movie_folder_arg
    # 如果参数没有，尝试读取config.ini
    if not html_root_folder or not local_movie_folder:
        if os.path.exists(config_path):
            config.read(config_path, encoding='utf-8')
            if not html_root_folder:
                html_root_folder = config.get('General', 'html_root_folder', fallback=None)
            if not local_movie_folder:
                local_movie_folder = config.get('General', 'local_movie_folder', fallback=None)
    # 如果还没有，提示用户输入
    if not html_root_folder:
        html_root_folder = input('请输入HTML文件根目录路径: ').strip()
    if not local_movie_folder:
        local_movie_folder = input('请输入本地电影文件夹路径: ').strip()
    # 写入config.ini
    config['General'] = {
        'html_root_folder': html_root_folder,
        'local_movie_folder': local_movie_folder
    }
    with open(config_path, 'w', encoding='utf-8') as f:
        config.write(f)
    return {
        'html_root_folder': html_root_folder,
        'local_movie_folder': local_movie_folder
    }
