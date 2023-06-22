from django.urls import path
from . import views

urlpatterns = [
    # login handel
    path('login', views.login_view, name='login'),
    
    # logout handel
    path('logout',views.logout_view, name='logout'),

    # createuser handel
    path('signup',views.add_user_view, name='add_user'),

    # dashboard
    path('', views.show_all_cat, name='dashboard'),

    # add catogery form
    path('add_category', views.add_category_view, name='add_cat_form'),

    # remove catogery
    path('remove_cat/<int:id>',  views.remove_category_view, name='remove_catogery'),

    # get all the links inside the catogery
    path('link/<int:id>', views.show_all_link, name='link_view'),

    # del a link
    path('link_del/<int:cat_id>/<int:id>', views.del_link, name='remove_link'),
    
    # add new Link
    path('add_link/<int:id>', views.add_link_view, name='add_link'),

    path('alter/<int:link_id>', views.alter_collection, name='alter_link'),

    # collected data
    path('data/<int:link_id>', views.collected_data_view, name='data_link'),

    path('download/<int:id>', views.download_view, name='download')
]