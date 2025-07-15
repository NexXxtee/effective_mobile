from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Ad, Category, ExchangeProposal

class AdModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name='Техника', slug='tehnika')

    def test_create_ad(self):
        ad = Ad.objects.create(
            user=self.user,
            title='Iphone',
            description='Состояние отличное',
            category=self.category,
            condition='new'
        )
        self.assertEqual(ad.title, 'Iphone')
        self.assertEqual(ad.condition, 'new')
        self.assertEqual(ad.user.username, 'testuser')

class CategoryModelTest(TestCase):
    def test_create_category(self):
        category = Category.objects.create(name='Одежда', slug='odezhda')
        self.assertEqual(category.name, 'Одежда')
        self.assertEqual(category.slug, 'odezhda')

class ExchangeProposalModelTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(username='user1', password='12345')
        self.user2 = get_user_model().objects.create_user(username='user2', password='12345')
        self.category = Category.objects.create(name='Техника', slug='tehnika')
        self.ad1 = Ad.objects.create(user=self.user1, title='Телефон', description='...', category=self.category, condition='new')
        self.ad2 = Ad.objects.create(user=self.user2, title='Ноутбук', description='...', category=self.category, condition='used')

    def test_create_proposal(self):
        proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            status='pending'
        )
        self.assertEqual(proposal.status, 'pending')
        self.assertEqual(proposal.ad_sender, self.ad1)
        self.assertEqual(proposal.ad_receiver, self.ad2)

class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name='Техника', slug='tehnika')
        Ad.objects.create(user=self.user, title='Телефон', description='...', category=self.category, condition='new')
        Ad.objects.create(user=self.user, title='Ноутбук', description='...', category=self.category, condition='used')

    def test_profile_access(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('ads:profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Мои объявления')

    def test_profile_ads_filter(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('ads:profile')
        response = self.client.get(url, {'condition': 'new'})
        self.assertContains(response, 'Телефон')
        self.assertNotContains(response, 'Ноутбук')

class AdListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name='Техника', slug='tehnika')
        for i in range(5):
            Ad.objects.create(user=self.user, title=f'Товар {i}', description='...', category=self.category, condition='new')

    def test_ad_list_pagination(self):
        url = reverse('ads:ad_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Проверяем, что на первой странице есть первые 3 товара
        self.assertContains(response, 'Товар 0')
        self.assertContains(response, 'Товар 1')
        self.assertContains(response, 'Товар 2')
        # Проверяем, что на второй странице есть следующий товар
        response2 = self.client.get(url + '?page=2')
        self.assertContains(response2, 'Товар 3')
        self.assertContains(response2, 'Товар 4')
        
        
class AdListSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='searchuser', password='12345')
        self.category = Category.objects.create(name='Техника', slug='tehnika')
        Ad.objects.create(user=self.user, title='Samsung Galaxy', description='Смартфон', category=self.category, condition='new')
        Ad.objects.create(user=self.user, title='Iphone', description='Apple', category=self.category, condition='new')
        Ad.objects.create(user=self.user, title='Ноутбук', description='Dell', category=self.category, condition='used')

    def test_search_by_title(self):
        url = reverse('ads:ad_list')
        response = self.client.get(url, {'search': 'Samsung'})
        self.assertContains(response, 'Samsung Galaxy')
        self.assertNotContains(response, 'Iphone')
        self.assertNotContains(response, 'Ноутбук')

    def test_search_by_description(self):
        url = reverse('ads:ad_list')
        response = self.client.get(url, {'search': 'Apple'})
        self.assertContains(response, 'Iphone')
        self.assertNotContains(response, 'Samsung Galaxy')
        self.assertNotContains(response, 'Ноутбук')