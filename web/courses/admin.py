from django.contrib import admin
from .models import Course, Chapter, TextBlock, CodingProblem
# Register your models here.

class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "public")
    prepopulated_fields = {"slug": ("title",)}

class ChapterAdmin(admin.ModelAdmin):
    list_display = ("title", "course")
    prepopulated_fields = {"slug": ("title",)}
    
class CodingProblemAdmin(admin.ModelAdmin):
    list_display = ("title", "chapter")
    prepopulated_fields = {"slug": ("title",)}



admin.site.register(Course, CourseAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(TextBlock)
admin.site.register(CodingProblem)
