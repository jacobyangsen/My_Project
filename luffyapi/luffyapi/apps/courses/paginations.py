from rest_framework.pagination import PageNumberPagination
class CoursePageNumberPagination(PageNumberPagination):
    """课程列表数据的分页器"""
    page_query_param = "page"           # 页码参数
    page_size_query_param = 'size'      # 单页数据量
    page_size = 5                       # 默认的单页数据量，就是每一页显示5个课程信息
    max_page_size = 20                  # 允许客户端设置的单页数据量