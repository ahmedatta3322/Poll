from rest_framework import generics, filters, views
from .serializers import PollSerializer
from .models import Poll, UserCast, Choice
from rest_framework.response import Response

# Create your views here.


class PollsListView(generics.ListAPIView):
    queryset = Poll.objects.all().order_by("-expiry_date")
    serializer_class = PollSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "description", "choices__choice"]


class VoteAPI(views.APIView):
    def post(self, request, pk):
        user = request.user
        if UserCast.objects.filter(user=user, poll_id=pk).exists():
            return Response({"error": "You have already voted"}, status=400)
        if Poll.objects.filter(id=pk)["is_expired"]:
            return Response({"error": "Poll has expired"}, status=400)
        else:
            choice = request.data.get("choice")
            if choice:
                try:
                    choice = Choice.objects.get(choice=choice)
                except Choice.DoesNotExist:
                    return Response({"error": "Invalid choice"}, status=400)
                else:
                    choice.votes += 1
                    choice.save()
                    UserCast.objects.create(user=user, poll_id=pk, choice=choice)
                    return Response(
                        {"success": "You have successfully voted"}, status=200
                    )
            else:
                return Response({"error": "Choice not found"}, status=400)
