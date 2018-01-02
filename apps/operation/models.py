from django.db import models
from  datetime import datetime

from apps.users.models import UserProfile
from apps.courses.models import Course

# Create your models here.

# 用户咨询
class UserAsk(models.Model):
    name = models.CharField('姓名' ,max_length=20)
    mobile = models.CharField('手机号码', max_length=11)
    course_name = models.CharField('咨询课程名', max_length=50)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name
        ordering = ['-add_time']

    def __str__(self):
        return self.name + '------' + self.course_name

# 用户对课程评论
class CourseComment(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户名', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='课程名', on_delete=models.CASCADE)
    comments = models.CharField('评论内容', max_length=200)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户对课程评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user + '------' + self.course

# 用户收藏
class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户名', on_delete=models.CASCADE)
    fav_type = models.IntegerField('收藏类型', choices=((1, '课程'), (2, '教师'), (3, '授课机构')), default=1)
    fav_id = models.IntegerField('数据ID', default=0)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user +  '------' + self.fav_type

# 给用户发送消息
class UserMessage(models.Model):
    user = models.IntegerField('接收ID', default=0)
    message = models.CharField('消息内容', max_length=500)
    has_read = models.BooleanField('是否已读', default=False)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user + '------' + self.has_read


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户名', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户学习课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user + '------' + self.course