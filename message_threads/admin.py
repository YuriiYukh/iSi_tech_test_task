from django.contrib import admin
from message_threads.models import Thread, Message


class ThreadAdmin(admin.ModelAdmin):
    '''
    Custom admin for Thread model
    '''
    list_display = ('id', 'participants_list', 'created', 'updated')
    search_fields = ('participants__username')
    list_filter = ('created', 'updated')

    def participants_list(self, obj: Thread):
        '''
        Display participants in comma-separated format
        '''
        return ', '.join(user.username for user in obj.participants.all())


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


admin.site.register(Thread)
admin.site.register(Message)
