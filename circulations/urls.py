from django.urls import path 
from .views import borrow_book, return_book, loan_list, return_list, edit_loan, delete_loan, export_loans_csv, export_returns_csv, add_loan, add_return, reward_system, activity_chart

urlpatterns = [
    path('borrow/', borrow_book, name='borrow_book'),
    path('return/', return_book, name='return_book'),
    path('loans/', loan_list, name='loan_list'),
    path('returns/', return_list, name='return_list'),
    path('loans/edit/<int:pk>/', edit_loan, name='edit_loan'),
    path('delete/<int:loan_id>/', delete_loan, name='delete_loan'),
    path('export_loans_csv/', export_loans_csv, name='export_loans_csv'),
    path('export_returns_csv/', export_returns_csv, name='export_returns_csv'),
    path('add_loan/', add_loan, name='add_loan'),
    path('add_return/', add_return, name='add_return'),
    path('reward_system/', reward_system, name='reward_system'),
    path('activity_chart/', activity_chart, name='activity_chart'),
]