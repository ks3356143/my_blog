import math

class Pagination:
    def __init__(self,current_page,all_count,base_url,
                 query_params,per_page,pager_page_count,position='pos'):#position为锚点
        # 当前页码、数据库中的总条数、原始URL、保留原搜索条件、一页展示多少、最多显示多少个页码
        self.all_count = all_count
        self.base_url = base_url
        self.query_params = query_params
        self.per_page = per_page
        self.position = position
        # 计算一共有多少个页
        self.current_count = math.ceil(all_count/per_page) #ceil函数是除有余就进位

        # 1.只能是满足条件的数字
        try:
            self.current_page = int(current_page)
            if not 0 < self.current_page <= self.current_count:
                self.current_page = 1
        except Exception as e:
            self.current_page = 1

        self.pager_page_count = pager_page_count
        # 2.分页的中值
        self.half_page_count = int(self.pager_page_count / 2)
        if self.current_count < self.pager_page_count:
            # 如果可分页的页码小于最大显示页码，就让最大显示页码变成可分页页码
            self.pager_page_count = self.current_count

    # 当前页码问题
    def page_html(self):
        # 计算页码起始和结束
        # 分类讨论
        # 1.正常情况
        # 现在有20个页码，我在第7页，左边5个右边5个，4 5 6 7 8 九 10 11 12 13 14
        start = self.current_page - self.half_page_count
        end = self.current_page + self.half_page_count
        # 非正常情况，判断当前页码所在位置
        if self.current_page <= self.half_page_count:
            # 在左侧
            start = 1
            end = self.pager_page_count
        if self.current_page + self.half_page_count >= self.current_count:
            # 在右侧
            start = self.current_count - self.pager_page_count + 1
            end = self.current_count

        # 生成分页
        page_list = []

        # 上一页
        if self.current_page != 1:
            self.query_params['page'] = self.current_page - 1
            page_list.append(f'<li><a href="{self.base_url}?{self.query_encode}#{self.position}">上一页</a></li>')

        # 数字部分
        for i in range(start, end + 1):
            self.query_params['page'] = i
            if self.current_page == i:
                li = f'<li class="active"><a href="{self.base_url}?{self.query_encode}#{self.position}">{i}</a></li>'
            else:
                li = f'<li><a href="{self.base_url}?{self.query_encode}#{self.position}">{i}</a></li>'
            page_list.append(li)

        # 下一页
        if self.current_page != self.current_count:
            self.query_params['page'] = self.current_page + 1
            page_list.append(f'<li><a href="{self.base_url}?{self.query_encode}#{self.position}">下一页</a></li>')

        return ''.join(page_list)

    # 起始和结束值
    @property
    def query_encode(self):
        return self.query_params.urlencode()

    @property #有点像计算属性
    def start(self):
        return (self.current_page - 1) * self.per_page

    @property
    def end(self):
        return self.current_page * self.per_page
