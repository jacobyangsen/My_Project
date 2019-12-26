# Create your models here.
from django.db import models
from luffyapi.utils.models import BaseModel
# Create your models here.
class CourseCategory(BaseModel):
    """
    课程分类
    """
    name = models.CharField(max_length=64, unique=True, verbose_name="分类名称")
    class Meta:
        db_table = "ly_course_category"
        verbose_name = "课程分类"
        verbose_name_plural = "课程分类"

    def __str__(self):
        return "%s" % self.name

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from datetime import datetime
class Course(BaseModel):
    """
    实战课程
    """
    course_type = (
        (0, '付费'),
        (1, 'VIP专享'),
        (2, '学位课程'),
    )
    level_choices = (
        (0, '初级'),
        (1, '中级'),
        (2, '高级'),
    )
    status_choices = (
        (0, '上线'),
        (1, '下线'),
        (2, '预上线'),
    )
    name = models.CharField(max_length=128, verbose_name="课程名称")
    course_img = models.ImageField(upload_to="course", max_length=255, verbose_name="封面图片", blank=True, null=True)
    course_video = models.FileField(upload_to="course_video", max_length=255, verbose_name="封面视频", blank=True, null=True)
    course_type = models.SmallIntegerField(choices=course_type,default=0, verbose_name="付费类型")
    # 使用这个字段的原因
    brief = RichTextUploadingField(verbose_name="详情介绍", null=True, blank=True)
    level = models.SmallIntegerField(choices=level_choices, default=1, verbose_name="难度等级")
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)
    period = models.IntegerField(verbose_name="建议学习周期(day)", default=7)
    attachment_path = models.FileField(max_length=128, verbose_name="课件路径", blank=True, null=True)
    status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="课程状态")
    course_category = models.ForeignKey("CourseCategory", on_delete=models.CASCADE, null=True, blank=True,verbose_name="课程分类")
    students = models.IntegerField(verbose_name="学习人数",default = 0)
    lessons = models.IntegerField(verbose_name="总课时数量",default = 0)
    pub_lessons = models.IntegerField(verbose_name="课时更新数量",default = 0)
    price = models.DecimalField(max_digits=6,decimal_places=2, verbose_name="课程原价",default=0)
    teacher = models.ForeignKey("Teacher",on_delete=models.DO_NOTHING, null=True, blank=True,verbose_name="授课老师")
    class Meta:
        db_table = "ly_course"
        verbose_name = "实战课程"
        verbose_name_plural = "实战课程"

    @property
    def teacher_demo(self):
        return "测试数据"

    @property
    def recomment_lessons(self):
        """课程列表的推荐课时"""
        lesson_list = self.lesson_list.filter(recomment=True, is_show=True, is_delete=False).order_by("orders","id")
        # data = []
        # for lesson in lesson_list:
        #     data.append({
        #         "id": lesson.id,
        #         "name": lesson.name,
        #         "free_trail": lesson.free_trail,
        #     })
        # return data

        # 列表生成式
        return  [{"id":lesson.id, "name": lesson.name, "free_trail": lesson.free_trail} for lesson in lesson_list]

    @property
    def level_name(self):
        """难度等级的文本格式"""
        return self.level_choices[self.level][1]

    @property
    def expire_list(self):
        """课程有效期选项列表"""
        data_list = self.courseexpire.all()
        data = []

        # 如果课程模型中，有存在永久价格，则在有效期选项列表中，新增永久有效的选项
        if self.price > 0:
            data.append({
                "time": "0",
                "text": "永久有效",
                "price": self.discount_price(self.price)
            })

        for item in data_list:
            data.append({
                "time": item.timer,
                "text": item.text,
                "price": self.discount_price(item.price)
            })

        return data

    def real_price(self, time=None):
        """获取真实原价"""
        if time == "0":
            price = self.price
        else:
            courseexpire = self.courseexpire.get(timer=time)
            price = courseexpire.price

        # 根据优惠计算真实价格

        return price

    @property
    def discount_name(self):
        """折扣类型"""
        # 判断 当前时间>活动开始时间 and 当前时间<活动结束时间
        try:
            activity = self.course_prices.get(activity__start_time__lt=datetime.now(), activity__end_time__gt=datetime.now(),is_show=True,is_delete=False)
        except:
            return ""
        return activity.discount.discount_type.name

    def discount_price(self,price=None):
        """折扣后的价格"""
        if price is None: # 如果没有传递参数，则默认采用当前原价
            price = self.price

        price = float(price) # 默认获取到的数据时Decimal类型的
        try:
            activity = self.course_prices.get(activity__start_time__lt=datetime.now(), activity__end_time__gt=datetime.now(),is_show=True,is_delete=False)
        except:
            return price

        # 计算参与活动后的真实价格
        condition = activity.discount.condition
        # 判断当前课程原价是否满足活动的参与条件
        if condition > price:
            return price

        sale = activity.discount.sale
        if sale == "0":
            """限时免费"""
            price = 0
        elif sale[0] == "*":
            """限时折扣"""
            num = float( sale[1:] ) # 折扣数值
            price = price * num

        elif sale[0] == "-":
            """限时减免"""
            num = float( sale[1:] ) # 减免数值
            price = price - num

        elif sale[0] == "满":
            """限时满减"""
            num_list = sale.split("\r\n")
            sale_list = [0]
            for item in num_list:
                sale_condition,sale_num = item[1:].split("-")
                if price > float(sale_condition):
                    sale_list.append( float(sale_num) )
            if len(sale_list) > 0:
                current_sale = max(sale_list)
                price = price - current_sale

        return "%.2f" % price

    @property
    def has_time(self):
        try:
            activity = self.course_prices.get(activity__start_time__lt=datetime.now(), activity__end_time__gt=datetime.now(),is_show=True,is_delete=False)
        except:
            return 0

        cur_timestamp = datetime.now().timestamp()
        end_timestamp = activity.activity.end_time.timestamp()
        time = end_timestamp - cur_timestamp
        return int(time)

    def __str__(self):
        return "%s" % self.name



class Teacher(BaseModel):
    """讲师、导师表"""
    role_choices = (
        (0, '讲师'),
        (1, '导师'),
        (2, '班主任'),
    )
    name = models.CharField(max_length=32, verbose_name="讲师昵称")
    role = models.SmallIntegerField(choices=role_choices, default=0, verbose_name="讲师身份")
    title = models.CharField(max_length=64, verbose_name="职位、职称")
    signature = models.CharField(max_length=255, verbose_name="导师签名", help_text="导师签名", blank=True, null=True)
    image = models.ImageField(upload_to="teacher", null=True, blank=True, verbose_name = "讲师封面")
    brief = models.TextField(max_length=1024, verbose_name="讲师描述")

    class Meta:
        db_table = "ly_teacher"
        verbose_name = "讲师导师"
        verbose_name_plural = "讲师导师"

    @property
    def role_name(self):
        return self.role_choices[self.role][1]

    def __str__(self):
        return "%s" % self.name


class CourseChapter(BaseModel):
    """课程章节"""
    course = models.ForeignKey("Course", related_name='chapters', on_delete=models.CASCADE, verbose_name="课程名称")
    chapter = models.SmallIntegerField(verbose_name="第几章", default=1)
    name = models.CharField(max_length=128, verbose_name="章节标题")
    summary = models.TextField(verbose_name="章节介绍", blank=True, null=True)
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)

    class Meta:
        db_table = "ly_course_chapter"
        verbose_name = "课程章节"
        verbose_name_plural = "课程章节"

    def __str__(self):
        return "%s:(第%s章)%s" % (self.course, self.chapter, self.name)


class CourseLesson(BaseModel):
    """课程课时"""
    lesson_type_choices = (
        (0, '文档'),
        (1, '练习'),
        (2, '视频')
    )
    chapter = models.ForeignKey("CourseChapter", related_name='lessons', on_delete=models.CASCADE,verbose_name="章节")
    course = models.ForeignKey("Course", related_name="lesson_list", on_delete=models.CASCADE, verbose_name="课程")
    name = models.CharField(max_length=128,verbose_name = "课时标题")
    lesson_type = models.SmallIntegerField(default=2, choices=lesson_type_choices, verbose_name="课时种类")
    lesson_link = models.CharField(max_length=255, blank=True, null=True, verbose_name="课时链接", help_text = "若是video，填vid,若是文档，填link")
    duration = models.CharField(verbose_name="视频时长", blank=True, null=True, max_length=32)  # 仅在前端展示使用
    pub_date = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)
    free_trail = models.BooleanField(verbose_name="是否可试看", default=False)
    recomment = models.BooleanField(verbose_name="是否推荐到课程列表")

    class Meta:
        db_table = "ly_course_lesson"
        verbose_name = "课程课时"
        verbose_name_plural = "课程课时"

    def __str__(self):
        return "%s-%s" % (self.chapter, self.name)


class CourseExpire(BaseModel):
    course = models.ForeignKey("Course", related_name='courseexpire', on_delete=models.CASCADE, verbose_name="课程ID")
    timer = models.CharField(max_length=100,verbose_name="课程有效期(天)",help_text="课程有效期")
    price = models.DecimalField(max_digits=6,decimal_places=2, verbose_name="课程价格",default=0)
    text  = models.CharField(max_length=64, verbose_name="课程有效期文本格式", help_text="课程有效期文本格式")

    class Meta:
        db_table = "ly_course_expire"
        verbose_name = "课程与有效期"
        verbose_name_plural = verbose_name
    def __str__(self):
        return "%s[%s]" % (self.course, self.text)


"""价格相关的模型"""
class PriceDiscountType(BaseModel):
    """课程优惠类型"""
    name = models.CharField(max_length=32, verbose_name="类型名称")
    remark = models.CharField(max_length=250, blank=True, null=True, verbose_name="备注信息")

    class Meta:
        db_table = "ly_price_discount_type"
        verbose_name = "课程优惠类型"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % (self.name)


class PriceDiscount(BaseModel):
    """课程优惠策略模型"""
    discount_type = models.ForeignKey("PriceDiscountType", on_delete=models.CASCADE, related_name='pricediscounts',
                                      verbose_name="优惠类型")
    condition = models.IntegerField(blank=True, default=0, verbose_name="满足优惠的价格条件")
    sale = models.TextField(verbose_name="优惠公式", help_text="""
    0表示免费；<br>
    *号开头加上浮点数表示折扣价，例如*0.82表示八二折；<br>
    -号开头加上数值表示减免价，例如-50表示减免50；<br>
    如果要表示限时满减,则需要使用 原价-优惠价格,例如表示,课程价格大于100,优惠10;大于200,优惠20,格式如下:<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;满100-10<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;满200-20<br>
    """)

    class Meta:
        db_table = "ly_price_discount"
        verbose_name = "价格优惠策略"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s: 优惠条件:%s,优惠值:%s" % (self.discount_type.name, self.condition, self.sale)

class Activity(BaseModel):
    """优惠活动模型"""
    name = models.CharField(max_length=64, verbose_name="活动名称")
    start_time = models.DateTimeField(verbose_name="活动的开始时间", help_text="活动的开始时间")
    end_time = models.DateTimeField(verbose_name="活动的结束时间", help_text="活动的结束时间")

    class Meta:
        db_table = "ly_activity"
        verbose_name = "优惠活动表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s[%s-%s]" % (self.name, self.start_time, self.end_time)

class CourseActivity(BaseModel):
    """课程与活动的关系模型"""
    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="course_prices", verbose_name="课程")
    activity = models.ForeignKey("Activity", on_delete=models.CASCADE, related_name="activity_courses")
    discount = models.ForeignKey("PriceDiscount", on_delete=models.CASCADE, related_name="discount_courses", verbose_name="优惠活动")

    class Meta:
        db_table = "ly_course_activity"
        verbose_name = "课程与优惠活动的关系"
        verbose_name_plural = "课程与优惠策略的关系"

    def __str__(self):
        return "%s-%s-%s" % (self.course.name, self.activity.name, self.discount.discount_type.name)