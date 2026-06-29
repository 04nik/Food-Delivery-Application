from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.timezone import datetime
from customer.models import OrderModel


class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        # get the current date
        today = datetime.today()
        orders = OrderModel.objects.filter(
            created_on__year=today.year, created_on__month=today.month, created_on__day=today.day
        ).order_by('-created_on')

        # loop through the orders and add the price value
        total_revenue = 0
        for order in orders:
            total_revenue += order.price

        # pass total number of orders and total revenue into template
        context = {
            'orders': orders,
            'total_revenue': total_revenue,
            'total_orders': len(orders)
        }

        return render(request, 'restaurant/dashboard.html', context)

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser or self.request.user.groups.filter(name='Staff').exists()


class OrderDetail(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        context = {
            'order': order
        }
        return render(request, 'restaurant/order_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)
        
        # Check which action was submitted
        if 'shipped' in request.POST:
            order.is_shipped = True
        elif 'paid' in request.POST:
            order.is_paid = True
            
        order.save()
        
        context = {
            'order': order
        }
        return render(request, 'restaurant/order_detail.html', context)

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser or self.request.user.groups.filter(name='Staff').exists()