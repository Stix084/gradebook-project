from django.shortcuts import redirect

def role_redirect(request):
    user = request.user
    
    if user.is_authenticated:
        # Redirect all users to home temporarily
        return redirect('home')
    
    return redirect('login')