from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Subject, Category, Material
# from .resources import SubjectResource, CategoryResource, MaterialResource
from import_export import resources

# class SubjectResource(resources.ModelResource):
#     class Meta:
#         model = Subject
#         fields = ('id', 'name', 'description', 'code')  # Specify the fields you want to export/import
#         export_order = ('id', 'name', 'description', 'code')

# class CategoryResource(resources.ModelResource):
#     class Meta:
#         model = Category
#         fields = ('id', 'category_name', 'subject__name')  # Export subject name instead of FK
#         export_order = ('id', 'category_name', 'subject__name')

# class MaterialResource(resources.ModelResource):
#     class Meta:
#         model = Material
#         fields = ('id', 'subject__name', 'material_type', 'file', 'uploaded_at')  # Export subject name instead of FK
#         export_order = ('id', 'subject__name', 'material_type', 'file', 'uploaded_at')

# # Registering Subject with Import/Export
# @admin.register(Subject)
# class SubjectAdmin(ImportExportModelAdmin):
#     resource_class = SubjectResource
#     list_display = ('name', 'code', 'description')
#     search_fields = ('name', 'code')

# # Registering Category with Import/Export
# @admin.register(Category)
# class CategoryAdmin(ImportExportModelAdmin):
#     resource_class = CategoryResource
#     list_display = ('category_name', 'subject')
#     search_fields = ('category_name', 'subject__name')

# # Registering Material with Import/Export
# @admin.register(Material)
# class MaterialAdmin(ImportExportModelAdmin):
#     resource_class = MaterialResource
#     list_display = ('subject', 'material_type', 'file', 'uploaded_at')
#     search_fields = ('subject__name', 'material_type')
