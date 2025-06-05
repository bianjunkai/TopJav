import json
import os

def process_data(movie_list, history_path):
    """
    处理电影数据，计算排名变化，返回最终用于Excel的数据（不含本地存在状态）。
    每个元素为dict：
    {
        'current_rank': int 或 '已跌出',
        'id': str,
        'name': str,
        'score': str,
        'rank_change': str
    }
    """
    # 1. 加载历史数据
    if os.path.exists(history_path):
        try:
            with open(history_path, 'r', encoding='utf-8') as f:
                last_data = json.load(f)
        except Exception:
            last_data = []
    else:
        last_data = []
    last_rank_map = {item['id']: item['current_rank'] for item in last_data}
    # 2. 构建当前编号到电影信息的映射
    current_rank_map = {item['id']: item for item in movie_list}
    # 3. 处理当前排行榜电影
    result = []
    for movie in movie_list:
        movie_id = movie['id']
        current_rank = movie['current_rank']
        # 排名变化
        if movie_id in last_rank_map:
            last_rank = last_rank_map[movie_id]
            diff = last_rank - current_rank
            if diff > 0:
                rank_change = f'↑{abs(diff)}'
            elif diff < 0:
                rank_change = f'↓{abs(diff)}'
            else:
                rank_change = '无变化'
        else:
            rank_change = '新晋'
        result.append({
            'current_rank': current_rank,
            'id': movie['id'],
            'name': movie['name'],
            'score': movie['score'],
            'rank_change': rank_change
        })
    # 4. 处理跌出排行榜的电影（插入到榜单后，按上次名次排序）
    dropped = []
    for movie_id, last_rank in last_rank_map.items():
        if movie_id not in current_rank_map:
            last_movie = next((item for item in last_data if item['id'] == movie_id), None)
            if last_movie:
                dropped.append({
                    'current_rank': '已跌出',
                    'id': last_movie['id'],
                    'name': last_movie['name'],
                    'score': last_movie.get('score', ''),
                    'rank_change': '跌出'
                })
    # 跌出电影按上次名次升序排列
    dropped.sort(key=lambda x: next((item['current_rank'] for item in last_data if item['id'] == x['id']), 9999))
    result.extend(dropped)
    print('解析后电影数：', len(movie_list))
    print('排名处理后数据数：', len(result))
    return result

def save_current_ranking(final_data, history_path):
    """
    保存本次排行榜数据到历史文件。
    只保存当前在榜的电影（不含已跌出）。
    """
    to_save = [
        {
            'current_rank': item['current_rank'],
            'id': item['id'],
            'name': item['name'],
            'score': item['score']
        }
        for item in final_data if item['rank_change'] != '跌出'
    ]
    with open(history_path, 'w', encoding='utf-8') as f:
        json.dump(to_save, f, ensure_ascii=False, indent=2)
