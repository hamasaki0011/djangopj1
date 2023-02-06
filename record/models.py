from django.db import models
from django.conf import settings
from django.utils import timezone
#import datetime

class Record(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title=models.CharField(verbose_name='タイトル', max_length=200)
    text=models.TextField(verbose_name='本文')
    created_at=models.DateTimeField(verbose_name='作成日時', default=timezone.now)
    puvlisheded_at=models.DateTimeField(verbose_name='公開日時', blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
    #def __str__(self):
        # 管理画面で表示する時間に9時間加算する
    #    datetime_now = self.update_at + datetime.timedelta(hours=9)
    #    datetime_now = datetime_now.strftime("%Y/%m/%d %H:%M:%S")
    #    return f'{self.name} {datetime_now}'

