import xadmin

from .models import CourseCategory
class CourseCategoryModelAdmin(object):
    """课程分类模型管理类"""
    pass
xadmin.site.register(CourseCategory, CourseCategoryModelAdmin)


from .models import Course
class CourseModelAdmin(object):
    """课程模型管理类"""
    pass
xadmin.site.register(Course, CourseModelAdmin)


from .models import Teacher
class TeacherModelAdmin(object):
    """老师模型管理类"""
    pass
xadmin.site.register(Teacher, TeacherModelAdmin)


from .models import CourseChapter
class CourseChapterModelAdmin(object):
    """课程章节模型管理类"""
    pass
xadmin.site.register(CourseChapter, CourseChapterModelAdmin)



from .models import CourseLesson
class CourseLessonModelAdmin(object):
    """课程课时模型管理类"""
    pass
xadmin.site.register(CourseLesson, CourseLessonModelAdmin)


from .models import CourseExpire
class CourseExpireModelAdmin(object):
    """课程与有效期模型管理类"""
    list_display = ["course","text","price"]
xadmin.site.register(CourseExpire, CourseExpireModelAdmin)

"""优惠活动的相关模型注册"""
from .models import Activity
class ActivityModelAdmin(object):
    """优惠活动模型管理类"""
    list_display = ["name","start_time","end_time"]
xadmin.site.register(Activity, ActivityModelAdmin)

from .models import PriceDiscountType
class PriceDiscountTypeModelAdmin(object):
    """优惠类型模型管理类"""
    list_display = ["name","remark"]
xadmin.site.register(PriceDiscountType, PriceDiscountTypeModelAdmin)

from .models import PriceDiscount
class PriceDiscountModelAdmin(object):
    """优惠策略公式模型管理类"""
    pass

xadmin.site.register(PriceDiscount, PriceDiscountModelAdmin)

from .models import CourseActivity
class CourseActivityModelAdmin(object):
    """课程与活动的关系模型管理类"""
    pass
xadmin.site.register(CourseActivity, CourseActivityModelAdmin)