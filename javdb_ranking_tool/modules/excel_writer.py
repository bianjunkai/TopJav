from openpyxl import Workbook
import os

def write_excel(final_data, out_path):
    """
    将最终数据写入Excel文件（out_path），按排名排序，已跌出的排在最后。
    """
    # 排序：榜单电影按 current_rank 升序，已跌出的排在最后且按上次名次升序
    def sort_key(item):
        if item['current_rank'] == '已跌出':
            # 跌出电影排最后，且按上次名次排序
            try:
                return (9999, int(item.get('last_rank', 9999)))
            except Exception:
                return (9999, 9999)
        else:
            return (int(item['current_rank']), 0)
    sorted_data = sorted(final_data, key=sort_key)

    wb = Workbook()
    ws = wb.active
    ws.title = 'JavDB排行榜'
    # 表头
    headers = ['名次', '电影编号', '电影名称', '评分', '本地是否存在', '排名变化']
    ws.append(headers)
    # 数据
    for item in sorted_data:
        ws.append([
            item['current_rank'],
            item['id'],
            item['name'],
            item['score'],
            item['exists_locally'],
            item['rank_change']
        ])
    # 保存
    wb.save(out_path)
    print(f'Excel报告已生成: {out_path}')
