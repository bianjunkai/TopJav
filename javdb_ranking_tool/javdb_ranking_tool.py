import argparse
import os
from modules import config_manager, html_reader, html_parser, local_scanner, data_processor, excel_writer

def choose_year(html_root):
    print("请选择排行榜类型：")
    print("1. 历年总排名")
    print("2. 指定年份")
    choice = input("输入1或2: ").strip()
    if choice == '1':
        subfolder = os.path.join(html_root, 'all_time')
        history_json = os.path.join(os.path.dirname(__file__), 'ranking_history_all_time.json')
        excel_xlsx = os.path.join(os.path.dirname(__file__), 'javdb_rankings_all_time.xlsx')
    else:
        year = input("请输入年份（如2025）: ").strip()
        subfolder = os.path.join(html_root, year)
        history_json = os.path.join(os.path.dirname(__file__), f'ranking_history_{year}.json')
        excel_xlsx = os.path.join(os.path.dirname(__file__), f'javdb_rankings_{year}.xlsx')
    return subfolder, history_json, excel_xlsx

def main():
    parser = argparse.ArgumentParser(description='JavDB 日本电影排行榜工具')
    parser.add_argument('--html_root_folder', type=str, help='HTML文件根目录')
    parser.add_argument('--local_movie_folder', type=str, help='本地电影文件夹路径')
    args = parser.parse_args()

    # 1. 读取配置
    config = config_manager.load_config(args.html_root_folder, args.local_movie_folder)
    html_root = config['html_root_folder']
    local_movie_folder = config['local_movie_folder']

    # 2. 选择年份/类型
    subfolder, history_json, excel_xlsx = choose_year(html_root)

    # 3. 读取HTML
    html_contents = html_reader.read_html_files(subfolder)

    # 4. 解析HTML
    movie_list = html_parser.parse_html_files(html_contents)

    # 5. 处理排名变化
    final_data = data_processor.process_data(movie_list, history_json)

    # 6. 扫描本地电影
    local_movies = local_scanner.scan_local_movies(local_movie_folder)

    # 7. 标记本地存在
    for item in final_data:
        item['exists_locally'] = '是' if item['id'].upper() in local_movies else '否'

    # 8. 写Excel
    excel_writer.write_excel(final_data, excel_xlsx)

    # 9. 保存历史
    data_processor.save_current_ranking(final_data, history_json)

if __name__ == '__main__':
    main()
