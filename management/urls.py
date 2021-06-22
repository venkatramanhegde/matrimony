from django.conf.urls import url
from .views import LoginAPIView, SignUp, AdminPage, FilterUserPage, LogoutAPIView, UserApproveView

urlpatterns = [
    url(r'^login/', view=LoginAPIView.as_view(), name="login"),
    url(r'^sign_up/', view=SignUp.as_view(), name="sign-up"),
    url(r'^admin_page/', view=AdminPage.as_view(), name="admin-page"),
    url(r'^user_detail_page/', view=FilterUserPage.as_view(), name="user-detail-page"),
    url(r'^user_approve/', view=UserApproveView.as_view(), name="user-detail-page"),
    url(r'^logout/', view=LogoutAPIView.as_view(), name="log_out"),

]