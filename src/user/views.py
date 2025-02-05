from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
#Create your views here

class UserLoginView(LoginView):
    template_name = "user/login.html"
    ##TODO(Cambiar la ruta)
    success_url= reverse_lazy('category_index')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)
    
    


def logout_view(request):
    logout(request)
    return redirect('login')