from bs4 import BeautifulSoup
import re

def parse_html_files(html_contents):
    """
    解析HTML内容列表，提取电影信息，返回电影信息列表。
    每个电影信息为字典：
    {
        'id': 电影编号,
        'name': 电影名称,
        'score': 评分字符串（如'4.69分'，如无则空字符串）, 
        'current_rank': 当前排名（int）
    }
    """
    movie_list = []
    for html in html_contents:
        soup = BeautifulSoup(html, 'html.parser')
        movie_items = soup.select('div.item')
        for item in movie_items:
            # 排名
            rank_tag = item.select_one('span.ranking')
            current_rank = int(rank_tag.text.strip()) if rank_tag else None
            # 电影编号和名称
            title_div = item.select_one('div.video-title')
            if title_div:
                strong = title_div.find('strong')
                movie_id = strong.text.strip() if strong else ''
                # 名称为 strong 后面的内容
                name = title_div.get_text().replace(movie_id, '', 1).strip()
            else:
                movie_id = ''
                name = ''
            # 评分
            score_div = item.select_one('div.score span.value')
            score = ''
            if score_div:
                # 例：4.69分, 由2185人評價
                m = re.search(r'(\d+\.\d+)分', score_div.text)
                if m:
                    score = m.group(1) + '分'
            # 组装
            movie_list.append({
                'id': movie_id,
                'name': name,
                'score': score,
                'current_rank': current_rank
            })
    return movie_list
