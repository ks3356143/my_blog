from urllib.parse import urlencode


class Search:
    def __init__(self, order, order_list, query_params):  # query_params为原搜索条件
        self.order_list = order_list
        self.query_params = query_params
        self.order = order

    def order_html(self):
        order_h = []
        self.query_params['order'] = '-change_date'
        order_h.append(f'<li><a href="?{self.query_encode}">综合排序</a></li>')
        for li in self.order_list:
            self.query_params['order'] = li[0]
            if self.order == li[0]:
                li_html = f'<li class="active"><a href="?{self.query_encode}">{li[1]}</a></li>'
            else:
                li_html = f'<li><a href="?{self.query_encode}">{li[1]}</a></li>'
            order_h.append(li_html)

        return ''.join(order_h)

    @property
    def query_encode(self):
        # return self.query_params.urlencode()
        return urlencode(self.query_params)


if __name__ == '__main__':
    order = Search(
        order='-create_date',  # 参数：当前搜索状态
        order_list=[
            ('-create_date', '最新发布'),
            ('look_count', '最多浏览'),
            ('digg_count', '最多点赞'),
            ('collects_count', '最多收藏'),
            ('comment_count', '最多评论'),
        ],
        query_params={'key': 'python'},  # 搜索条件，我要搜索python，如果有分页器东西移除
    )
    print(order.order_html())
