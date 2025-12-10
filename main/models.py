from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Events(models.Model):
    title = models.CharField(max_length=100, null=True, help_text="Перед добавлением новой недели удалите предыдущую")
    img = models.ImageField(upload_to='events/images/')
    order = models.IntegerField(help_text="Укажите номер изображения(0 - Главное изображение)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Event {self.order}"

class Clubs(models.Model):
    title = models.CharField(max_length=100, null=True)
    img = models.ImageField(upload_to='clubs/images/')
    description = models.TextField()
    other = models.TextField(help_text="Напишите адресс, время, ссылку. Ссылка должна быть полной.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Club {self.id}"

class Services(models.Model):
    title = models.CharField(max_length=100, null=True)
    img = models.ImageField(upload_to='services/images/', null=True, blank=True)
    description = models.TextField(help_text="Ссылка должна быть полной.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Service {self.id}"

class Support(models.Model):
    title = models.CharField(max_length=100, null=True)
    img = models.ImageField(upload_to='support/images/')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Support {self.id}"

class News(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)
    description = models.TextField(help_text="Ссылка должна быть полной.")
    main_image = models.ImageField(upload_to='news/main/', help_text="Пропорция картинки 1.6:1")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:7]
        super().save(*args, **kwargs)

    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('main:new_detail',
                       args=[self.slug])
    

class NewsImage(models.Model):
    product = models.ForeignKey(News, on_delete=models.CASCADE, 
                                related_name='images')
    image = models.ImageField(upload_to='news/extra/')


class Zayvka(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="ФИО")
    birth_date = models.DateField(verbose_name="Дата рождения")
    phone = models.CharField(max_length=20, verbose_name="Номер телефона")
    email = models.EmailField(verbose_name="Адрес электронной почты")
    vk_link = models.CharField(verbose_name="Ссылка на социальную сеть ВКонтакте")
    workplace = models.CharField(max_length=300, verbose_name="Место работы/учёбы")
    initiative_name = models.CharField(max_length=200, verbose_name="Название инициативы")
    initiative_goal = models.TextField(verbose_name="Цель инициативного предложения")
    initiative_description = models.TextField(verbose_name="Описание инициативного предложения")

    FORMAT_CHOICES = [
        ('stock', 'Акция'),
        ('discussion', 'Дискуссия'),
        ('class', 'Занятие'),
        ('games', 'Игры'),
        ('competition', 'Конкурс'),
        ('conference', 'Конференция'),
        ('holiday', 'Праздник'),
        ('performance', 'Представление'),
        ('thematic_meeting', 'Тематическая встреча'),
        ('broadcast', 'Трансляция'),
        ('ceremony', 'Церемония'),
        ('information_support', 'Информационное сопровождение'),
        ('support', 'Кадровая поддержка'),
        ('other', 'Другое')
    ]

    initiative_format = models.CharField(max_length=50, choices=FORMAT_CHOICES, verbose_name="Формат инициативы")
    other_format_details = models.TextField(verbose_name="Если выбрали 'Другое', распишите формат", blank=True)
    initiative_date = models.DateField(verbose_name="Дата проведения инициативы")
    initiative_time = models.CharField(verbose_name="Время проведения инициативы")

    PARTICIPANTS_CHOICES = [
        ('10-30', '10-30 человек'),
        ('30-50', '30-50 человек'),
        ('50-100', '50-100 человек'),
        ('100+', 'Более 100 человек'),
    ]

    expected_participants = models.CharField(max_length=10, choices=PARTICIPANTS_CHOICES, verbose_name="Предполагаемое количество участников")
    
    ROOM_TYPE_CHOICES = [
        ('conference_room', 'Конференц-зал'),
        ('digital_workshop', 'Цифровая мастерская'),
        ('photo_studio', 'Фотостудия'),
        ('food_court', 'Фудкорт'),
        ('soldering_workshop', 'Паяльная мастерская'),
        ('cyberclass', 'Киберкласс'),
        ('lobby_cyber_class', 'Холл у киберкласса'),
        ('coworking', 'Коворкинг'),
    ]

    room_type = models.CharField(max_length=50, choices=ROOM_TYPE_CHOICES, verbose_name="Тип помещения")
    technical_equipment = models.TextField(verbose_name="Техническое оснащение инициативы")
    comments = models.TextField(verbose_name="Комментарии")
    personal_data_agreement = models.BooleanField(verbose_name="Согласие на обработку персональных данных", default=False)
    status = models.CharField(max_length=20,
        choices=[
            ('review', 'На рассмотрении'),
            ('accepted', 'Принято'),
            ('rejected', 'Отклонена'),
        ],
        default='review', verbose_name="Статус заявки")
    
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Заявка от {self.full_name} ({self.created_at.date()})"