import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'des_nat.settings')
django.setup()

from apps.samples.models import Sample

for s in Sample.objects.all():
    print(f"Title: {s.title}, Slug: {s.slug}")
