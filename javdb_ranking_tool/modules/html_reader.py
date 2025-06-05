import os

def read_html_files(html_folder):
    """
    读取指定目录下的7个HTML文件，返回文件内容列表（按页码顺序）。
    文件名格式如：ranking_page1.html, ranking_page2.html ...
    """
    html_files = []
    for i in range(1, 8):
        fname = f'ranking_page{i}.html'
        fpath = os.path.join(html_folder, fname)
        if os.path.exists(fpath):
            html_files.append(fpath)
        else:
            print(f"警告: 缺少文件 {fpath}")
    html_contents = []
    for fpath in html_files:
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                html_contents.append(f.read())
        except Exception as e:
            print(f"读取文件失败: {fpath}, 错误: {e}")
    return html_contents
