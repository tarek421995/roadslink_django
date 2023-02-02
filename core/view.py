# in views.py
from django.db.models import Sum
from slick_reporting.views import SlickReportView
from slick_reporting.fields import SlickReportField
from assessments.models import Psycometric
from django.contrib.auth import get_user_model

User = get_user_model()
class TotalProductSales(SlickReportView):

    report_model = User
    date_field = 'date_joined'
    group_by = 'username'
    columns = ['username',
                SlickReportField.create(Sum, 'current_attempts') ,
                SlickReportField.create(Sum, 'final_score', name='final_score') ]
    chart_settings = [{
        'type': 'column',
        'data_source': ['current_attempts'],
        'plot_total': False,
        'title_source': 'current_attempts',
        'title': ('Detailed Columns'),

    }, ]