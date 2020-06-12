from django.urls import path, include
from .views import InputNumView, SumViewCalculate, SumViewList, AllView, History, HistoryDetail

app_name = 'core'

urlpatterns = [
    path('add', InputNumView.as_view(), name='add_num'),
    path('calculate', SumViewCalculate.as_view(), name = 'calculate'),
    path('calculate/all', SumViewList.as_view()),
    path('reset', AllView.as_view()),
    path('history', History.as_view()),
    path('history/<int:pk>', HistoryDetail.as_view()),
]