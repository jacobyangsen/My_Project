from rest_framework import serializers
from .models import CourseCategory

class CourseCategoryModelSerializer(serializers.ModelSerializer):
    """课程分类"""
    class Meta:
        model = CourseCategory
        fields = ["id","name"]

from .models import Teacher
class TeacherModelSerializer(serializers.ModelSerializer):
    """讲师导师序列化器"""
    class Meta:
        model = Teacher
        fields = ["id", "image", "brief", "name","role_name","title","signature"]

from .models import Course
class CourseModelSerializer(serializers.ModelSerializer):
    """课程列表"""
    teacher = TeacherModelSerializer()
    class Meta:
        model = Course
        fields = ["id","name","course_img","students","lessons","pub_lessons","price","teacher","recomment_lessons","discount_name","discount_price"]

class CourseRetrieveModelSerializer(serializers.ModelSerializer):
    """课程详情"""
    teacher = TeacherModelSerializer()
    class Meta:
        model = Course
        fields = ["id", "name", "course_img", "course_video", "students", "lessons", "pub_lessons", "price", "teacher", "brief",
                  "level_name","discount_name","discount_price","has_time"]

from .models import CourseChapter,CourseLesson
class CourseLessonModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLesson
        fields = ["id", "name", "free_trail","duration"]

class CourseChapterModelSerializer(serializers.ModelSerializer):
    lessons = CourseLessonModelSerializer(many=True)
    class Meta:
        model = CourseChapter
        fields = ["chapter","name","summary","lessons"]