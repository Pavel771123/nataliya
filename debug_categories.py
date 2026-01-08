
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'des_nat.settings')
django.setup()

from apps.portfolio.models import ProjectCategory

print("-" * 50)
print("PROJECT CATEGORIES DEBUG INFO")
print("-" * 50)

categories = ProjectCategory.objects.all()
for cat in categories:
    status = []
    if cat.is_deleted: status.append("DELETED")
    if not cat.slug: status.append("NO_SLUG")
    
    status_str = f"[{', '.join(status)}]" if status else "[OK]"
    
    print(f"ID: {cat.id} | Name: '{cat.name}' | Slug: '{cat.slug}' | {status_str}")

print("-" * 50)
