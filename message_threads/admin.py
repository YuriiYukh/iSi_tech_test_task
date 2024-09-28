from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from message_threads.models import Thread, Message


class ThreadAdmin(admin.ModelAdmin):
    '''
    Custom admin for Thread model
    '''
    list_display = ('id', 'participants_list', 'created', 'updated')
    search_fields = ('participants__username', )
    list_filter = ('created', 'updated')

    def participants_list(self, obj: Thread):
        '''
        Display participants in comma-separated format
        '''
        return ', '.join(user.username for user in obj.participants.all())
    
    def save_model(self, request, obj, form, change):
        """
        Save the Thread object first to ensure it has an ID.
        """
        obj.save()

    def save_related(self, request, form, formsets, change):
        """
        Validate the participants field after saving the Thread.
        """
        form.save_m2m()

        if form.instance.participants.count() > 2:
            raise ValidationError(_("A thread cannot have more than 2 participants."))

        super().save_related(request, form, formsets, change)


class MessageAdmin(admin.ModelAdmin):
    '''
    Custom admin for Message model
    '''
    list_display = ('id', 'sender', 'text_preview',
                    'thread', 'created', 'is_read')
    search_fields = ('sender__username', 'text')
    list_filter = ('created', 'is_read')

    def text_preview(self, obj: Message):
        '''
        Method to show the preview text of the message
        '''
        text = obj.text
        return text[:50] + '...' if len(obj.text) > 50 else text


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Message, MessageAdmin)
