from urllib.parse import urlencode
class Search:
    def __init__(self, order, order_list, query_params):
        self.order_list = order_list
        self.order = order
        self.query_params = query_params

    def order_html(self):
        order_list = []
        self.query_params['order'] = '-change_date'
        order_list.append(f'<li><a href="?{self.query_encode}">综合排序</a></li>')
        for li in self.order_list:
            self.query_params['order'] = li[0]
            if self.order == li[0]:
                li = f'<li class="active"><a href="?{self.query_encode}">{li[1]}</a></li>'
            else:
                li = f'<li><a href="?{self.query_encode}">{li[1]}</a></li>'
            order_list.append(li)

        return ''.join(order_list)

    @property
    def query_encode(self):
        return urlencode(self.query_params)
        # return self.query_params.urlencode()


if __name__ == '__main__':
    order = Search(
        order='',
        order_list=[
            ('-create_date', "最新发布"),
            ('look_count', "最多浏览"),
            ('digg_count', "最多点赞"),
            ('coLects_count', "最多收藏"),
            ('comment_count', "最多评论"),
        ],
        query_params={'key': 'python'}
    )

    print(order.order_html())
