from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from wordplay.responses.models import Survey


class UserCheckMixin(object):
    user_check_failure_path = ''  # can be path, url name or reverse_lazy

    def check_user(self, user, team_temp):
        return True

    def user_check_failed(self, request, *args, **kwargs):
        raise PermissionDenied

    def dispatch(self, request, *args, **kwargs):
        if not self.check_user(request.user, get_object_or_404(Survey, pk=kwargs['pk'])):
            return self.user_check_failed(request, *args, **kwargs)

        return super(UserCheckMixin, self).dispatch(request, *args, **kwargs)


class CreatorRequiredMixin(UserCheckMixin):

    def check_user(self, user, team_temp):
        return user == team_temp.created_by
