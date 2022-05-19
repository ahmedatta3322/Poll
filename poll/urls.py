from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from common.permissions import auth_required

urlpatterns = [
    path("polls/", auth_required(views.PollsListView.as_view()), name="polls"),
    path("<int:pk>/vote/", auth_required(views.VoteAPI.as_view()), name="poll-vote"),
]
