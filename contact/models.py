''' Models configuration for contact app '''

from django.db import models

from profiles.models import UserProfile


class ContactUs(models.Model):
    '''Model that represent the data structure for contact us '''

    class Meta:
        '''Set verbose name'''
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    subject_options = [
            ('Information', 'Information'),
            ('Issue', 'Issue'),
            ('Other', 'Other'),
        ]

    subject = models.CharField(choices=subject_options, default='Information',
                               max_length=254, null=False, blank=False)
    body = models.TextField(max_length=2000, null=False, blank=False)
    sender = models.EmailField(max_length=254, null=False, blank=False)
    receiver = models.EmailField(max_length=254, null=False, blank=False)
    date_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                             null=True, blank=True)

    def __str__(self):
        ''' String method to return the sender's email '''
        return str(self.sender)
