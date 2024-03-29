from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError
import re


def validate_ip(ip):
    pattern = re.compile('^((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))$')

    if not re.match(pattern, ip):
        raise ValidationError("Incorrect IP format input")


# Create your models here.
class AllowHostModel(models.Model):
    class Meta():
        verbose_name = verbose_name_plural = '1. 白名单'

    ip = models.CharField(max_length=255, null=False, blank=False, verbose_name='IP',
                          validators=[validate_ip], unique=True)
    datetime = models.DateTimeField(auto_now=now, verbose_name='修改时间')

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.ip = self.ip.strip()
        super(AllowHostModel, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                         update_fields=update_fields)

    def __str__(self):
        return self.ip


class SenderLogManagerModel(models.Model):
    class Meta():
        verbose_name = verbose_name_plural = '2. 日志管理'

    USE_LOG_CHOICES = (
        (0, '否'),
        (1, '是'),
    )
    use_log = models.PositiveIntegerField(
        choices=USE_LOG_CHOICES, default=USE_LOG_CHOICES[0][0], verbose_name='是否记录日期'
    )

    def __str__(self):
        return 'SenderLogManager'


class SenderLogModel(models.Model):
    class Meta():
        verbose_name = verbose_name_plural = '3. 日志信息'

    STATUS_CHOICES = (
        (1, '成功'),
        (0, '失败'),
    )
    ip = models.CharField(max_length=255, blank=False, null=False, verbose_name='IP')
    datetime = models.DateTimeField(auto_now=now, verbose_name='日期时间')
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0], verbose_name='状态')
    error_msg = models.TextField(default='',blank=True,null=True,verbose_name='异常信息')

    def __str__(self):
        return self.ip
