from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Ad, ExchangeProposal, Category
from .forms import AdForm, ExchangeProposalForm
from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.core.paginator import Paginator



class AdListView(ListView):
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        condition = self.request.GET.get('condition')
        search = self.request.GET.get('search')
        if category:
            queryset = queryset.filter(category__id=category)
        if condition:
            queryset = queryset.filter(condition=condition)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        # ручная пагинация из-за танцева с бубном
        ads_list = self.get_queryset()
        paginator = Paginator(ads_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['ads'] = page_obj
        return context
    
    
class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'
    context_object_name = 'ad'


class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    template_name = 'ads/ad_form.html'
    form_class = AdForm
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AdUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ad 
    template_name = 'ads/ad_form.html'
    form_class = AdForm
    
    def test_func(self):
        ad = self.get_object()
        if ad.user != self.request.user:
            messages.error(self.request, "Вы не являетесь автором этого объявления.")
            raise Http404("Нет доступа")
        return True

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Http404:
            messages.error(self.request, "Объявление не найдено.")
            raise

class AdDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ad
    template_name = 'ads/ad_confirm_delete.html'
    success_url = reverse_lazy('ads:profile')

    def test_func(self):
        ad = self.get_object()
        if ad.user != self.request.user:
            messages.error(self.request, "Вы не являетесь автором этого объявления.")
            raise Http404("Нет доступа")
        return True
    
    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Http404:
            messages.error(self.request, "Объявление не найдено.")
            raise
        
        
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'ads/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Фильтрация объявлений пользователя
        ads = Ad.objects.filter(user=user)
        category = self.request.GET.get('category')
        condition = self.request.GET.get('condition')
        search = self.request.GET.get('search')
        if category:
            ads = ads.filter(category__id=category)
        if condition:
            ads = ads.filter(condition=condition)
        if search:
            ads = ads.filter(Q(title__icontains=search) | Q(description__icontains=search))

        # Предложения обмена
        context['ads'] = ads
        context['categories'] = Category.objects.all()
        context['proposals'] = ExchangeProposal.objects.filter(ad_sender__user=user) | ExchangeProposal.objects.filter(ad_receiver__user=user)
        return context
    

class ExchangeProposalCreateView(LoginRequiredMixin, CreateView):
    model = ExchangeProposal
    form_class = ExchangeProposalForm
    template_name = 'ads/exchange_proposal_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad_receiver'] = self.ad_receiver
        return context

    def dispatch(self, request, *args, **kwargs):
        self.ad_receiver = Ad.objects.get(pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Показывать только объявления пользователя
        return kwargs

    def form_valid(self, form):
        form.instance.ad_receiver = self.ad_receiver
        form.instance.status = 'pending'  # Всегда "Ожидает"
        form.instance.ad_sender = form.cleaned_data['ad_sender']  # Выбранное объявление пользователя
        response = super().form_valid(form)
        messages.success(self.request, "Ваше предложение обмена отправлено и ожидает ответа.")
        return response

    def get_success_url(self):
        return reverse_lazy('ads:profile')
    
    
class ExchangeProposalStatusView(LoginRequiredMixin, View):
    def post(self, request, pk):
        proposal = get_object_or_404(ExchangeProposal, pk=pk)
        user = request.user
        action = request.POST.get('action')

        # Отправитель может отменить
        if proposal.ad_sender.user == user and proposal.status == 'pending' and action == 'cancel':
            proposal.status = 'cancelled'
            proposal.save()
            messages.success(request, "Вы отменили предложение.")
        # Получатель может принять
        elif proposal.ad_receiver.user == user and proposal.status == 'pending' and action == 'accept':
            proposal.status = 'accepted'
            proposal.save()
            messages.success(request, f"Вы приняли предложение. Контакты отправителя: {proposal.ad_sender.user.email}")
        else:
            messages.error(request, "Недопустимое действие или статус.")

        return redirect('ads:profile')