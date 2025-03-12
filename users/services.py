from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

from users.models import User


@permission_required("users.view_customuser")
def block_user(self, pk):
    user = User.objects.get(pk=pk)
    user.is_active = not user.is_active
    user.save()
    return redirect(reverse("users:users_list"))


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return HttpResponseRedirect(reverse("clients:home"))