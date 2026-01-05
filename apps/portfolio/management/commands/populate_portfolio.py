"""
Management command to populate database with sample portfolio data.
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.portfolio.models import ProjectCategory, Project, ProjectCharacteristic


class Command(BaseCommand):
    help = 'Populate database with sample portfolio data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample portfolio data...\n')

        # Create categories
        categories_data = [
            {
                'name': 'Квартиры',
                'description': 'Дизайн интерьера квартир различной площади'
            },
            {
                'name': 'Дома',
                'description': 'Проекты частных домов и коттеджей'
            },
            {
                'name': 'Офисы',
                'description': 'Дизайн офисных помещений'
            },
            {
                'name': 'Коммерческие помещения',
                'description': 'Рестораны, магазины, салоны красоты'
            }
        ]

        categories = {}
        for idx, cat_data in enumerate(categories_data):
            category, created = ProjectCategory.objects.get_or_create(
                slug=slugify(cat_data['name']),
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description'],
                    'order': idx
                }
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created category: {category.name}'))
            else:
                self.stdout.write(f'  Category already exists: {category.name}')

        # Create projects
        projects_data = [
            {
                'title': '3-х комнатная квартира',
                'category': 'Квартиры',
                'year': 2025,
                'area': 55.00,
                'client_type': 'для семейной пары',
                'short_description': 'Современная квартира с элегантным дизайном и функциональной планировкой',
                'description': '''Дизайн интерьера для молодой семейной пары. Основной акцент сделан на создание уютного и функционального пространства с элементами натурального дерева. Мы стремились создать пространство, которое будет гармонично сочетать в себе эстетику и практичность.

Использовались светлые тона и натуральные материалы, что создает ощущение простора и уюта. Многоуровневое освещение позволяет создавать различные сценарии освещения для разного времени суток и настроения.''',
                'is_published': True,
                'is_featured': True,
                'order': 0,
                'characteristics': [
                    ('Стиль', 'Современный минимализм'),
                    ('Материалы', 'Дерево, стекло, текстиль'),
                    ('Цветовая гамма', 'Светлые тона с акцентами'),
                    ('Освещение', 'Многоуровневое'),
                ]
            },
            {
                'title': 'Двухуровневая квартира-студия',
                'category': 'Квартиры',
                'year': 2024,
                'area': 42.00,
                'client_type': 'для молодого специалиста',
                'short_description': 'Компактная студия с эффективным использованием пространства',
                'description': '''Проект квартиры-студии для молодого специалиста. Главная задача - максимально эффективно использовать каждый квадратный метр, создав при этом стильное и комфортное пространство.

Двухуровневая планировка позволила разделить зоны сна и работы, сохранив при этом ощущение простора. Использование светлых оттенков и зеркальных поверхностей визуально расширяет пространство.''',
                'is_published': True,
                'is_featured': False,
                'order': 1,
                'characteristics': [
                    ('Стиль', 'Скандинавский'),
                    ('Материалы', 'Дерево, металл, стекло'),
                    ('Цветовая гамма', 'Белый, серый, натуральное дерево'),
                    ('Особенности', 'Двухуровневая планировка'),
                ]
            },
            {
                'title': 'Загородный дом 200 м²',
                'category': 'Дома',
                'year': 2024,
                'area': 200.00,
                'client_type': 'для семьи с детьми',
                'short_description': 'Просторный загородный дом в современном стиле',
                'description': '''Проект загородного дома для семьи с двумя детьми. Основная концепция - создание комфортного пространства для всей семьи с учетом потребностей каждого члена семьи.

Большие панорамные окна обеспечивают естественное освещение и связь с природой. Открытая планировка первого этажа создает ощущение простора, а приватные зоны на втором этаже обеспечивают уединение.''',
                'is_published': True,
                'is_featured': True,
                'order': 2,
                'characteristics': [
                    ('Стиль', 'Современный'),
                    ('Материалы', 'Камень, дерево, стекло'),
                    ('Цветовая гамма', 'Натуральные оттенки'),
                    ('Особенности', 'Панорамные окна, камин'),
                    ('Этажность', '2 этажа'),
                ]
            },
            {
                'title': 'Офис IT-компании',
                'category': 'Офисы',
                'year': 2025,
                'area': 120.00,
                'client_type': 'для IT-компании',
                'short_description': 'Современный офис с зонами для работы и отдыха',
                'description': '''Дизайн офиса для молодой IT-компании. Задача - создать пространство, которое будет стимулировать креативность и продуктивность сотрудников.

Офис включает в себя открытое пространство для работы, переговорные комнаты, зону отдыха и кухню. Использование ярких акцентов и современной мебели создает энергичную атмосферу.''',
                'is_published': True,
                'is_featured': False,
                'order': 3,
                'characteristics': [
                    ('Стиль', 'Индустриальный'),
                    ('Материалы', 'Металл, бетон, дерево'),
                    ('Цветовая гамма', 'Серый, белый, яркие акценты'),
                    ('Зонирование', 'Open space, переговорные, зона отдыха'),
                ]
            },
            {
                'title': 'Ресторан средиземноморской кухни',
                'category': 'Коммерческие помещения',
                'year': 2024,
                'area': 85.00,
                'client_type': 'для ресторанного бизнеса',
                'short_description': 'Уютный ресторан с атмосферой средиземноморья',
                'description': '''Проект ресторана средиземноморской кухни. Концепция - создать атмосферу, которая переносит гостей на побережье Средиземного моря.

Использование натуральных материалов, теплых оттенков и характерных элементов декора создает аутентичную атмосферу. Продуманное освещение позволяет создать уютную обстановку в вечернее время.''',
                'is_published': True,
                'is_featured': False,
                'order': 4,
                'characteristics': [
                    ('Стиль', 'Средиземноморский'),
                    ('Материалы', 'Камень, дерево, керамика'),
                    ('Цветовая гамма', 'Теплые оттенки, терракота, синий'),
                    ('Вместимость', '40 посадочных мест'),
                ]
            },
            {
                'title': '4-х комнатная квартира премиум-класса',
                'category': 'Квартиры',
                'year': 2025,
                'area': 120.00,
                'client_type': 'для семьи',
                'short_description': 'Роскошная квартира с изысканным дизайном',
                'description': '''Проект квартиры премиум-класса для семьи. Задача - создать роскошное, но при этом комфортное пространство для жизни.

Использование дорогих материалов, авторской мебели и произведений искусства создает уникальную атмосферу. Каждая комната имеет свой характер, но при этом все пространство объединено общей концепцией.''',
                'is_published': True,
                'is_featured': True,
                'order': 5,
                'characteristics': [
                    ('Стиль', 'Неоклассика'),
                    ('Материалы', 'Мрамор, дерево ценных пород, шелк'),
                    ('Цветовая гамма', 'Бежевый, золотой, темное дерево'),
                    ('Особенности', 'Авторская мебель, произведения искусства'),
                ]
            },
        ]

        for project_data in projects_data:
            characteristics = project_data.pop('characteristics')
            category_name = project_data.pop('category')
            
            project, created = Project.objects.get_or_create(
                slug=slugify(project_data['title']),
                defaults={
                    **project_data,
                    'category': categories[category_name],
                    'meta_description': project_data['short_description']
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created project: {project.title}'))
                
                # Add characteristics
                for idx, (name, value) in enumerate(characteristics):
                    ProjectCharacteristic.objects.create(
                        project=project,
                        name=name,
                        value=value,
                        order=idx
                    )
                self.stdout.write(f'  Added {len(characteristics)} characteristics')
            else:
                self.stdout.write(f'  Project already exists: {project.title}')

        self.stdout.write(self.style.SUCCESS('\n✓ Sample data created successfully!'))
        self.stdout.write('\nYou can now:')
        self.stdout.write('1. Visit http://127.0.0.1:8000/admin/ to manage projects')
        self.stdout.write('2. Add images to projects through admin interface')
        self.stdout.write('3. Visit http://127.0.0.1:8000/portfolio/ to see the portfolio')
