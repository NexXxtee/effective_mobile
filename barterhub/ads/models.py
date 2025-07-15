from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")
    
    def __str__(self):
        return self.name


class Ad(models.Model):
    CONDITION_CHOICES = [
        ("new", "Новый"),
        ("used", "Б/у"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ads")
    title = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="ads")
    condition = models.CharField(
        max_length=20, choices=CONDITION_CHOICES, default="used"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("ads:ad_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title


class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ("pending", "Ожидает"),
        ("accepted", "Принята"),
        ("declined", "Отклонена"),
    ]

    ad_sender = models.ForeignKey(
        Ad, on_delete=models.CASCADE, related_name="sent_proposals"
    )
    ad_receiver = models.ForeignKey(
        Ad, on_delete=models.CASCADE, related_name="received_proposals"
    )
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ad_sender} → {self.ad_receiver} ({self.status})"

