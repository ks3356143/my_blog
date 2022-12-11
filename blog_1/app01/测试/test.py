current_count = 2

fenye_count = 9
half_fenye = int(9 / 2)
if current_count < fenye_count:
    # 如果可分页的页码小于最大显示页码，就让最大显示页码变成可分页页码
    fenye_count = current_count
