from django.contrib import admin
from .models import Course, Chapter, TextPart, CodingProblemPart, UserSolution
# Register your models here.

class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "public")
    prepopulated_fields = {"slug": ("title",)}
    
class CodingProblemAdmin(admin.ModelAdmin):
    list_display = ("title", "chapter")
    prepopulated_fields = {"slug": ("title",)}

class ChapterAdmin(admin.ModelAdmin):
    list_display = ("title", )
    prepopulated_fields = {"slug": ("title",)}

class TextPartAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}



admin.site.register(Course, CourseAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(TextPart, TextPartAdmin)
admin.site.register(CodingProblemPart)
admin.site.register(UserSolution)
