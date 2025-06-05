import os
import re

def scan_local_movies(local_movie_folder):
    """
    扫描本地电影文件夹，返回本地存在的电影编号集合（全部大写）。
    只要文件名中包含类似SSNI-XXX、ABP-YYY等编号即可。
    """
    movie_id_set = set()
    # 番号正则：字母+连字符+数字（如SSNI-123、ABP-456）
    pattern = re.compile(r'([A-Z]{2,5}-\d{2,5})', re.IGNORECASE)
    for root, _, files in os.walk(local_movie_folder):
        for fname in files:
            matches = pattern.findall(fname)
            for m in matches:
                movie_id_set.add(m.upper())
    return movie_id_set
