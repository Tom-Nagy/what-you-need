''' Views to manage and render the profiles pages '''


from django.shortcuts import render


def profile(request):
    ''' Display the user's profile information '''
    template = 'profiles/profile.html'
    context = {}

    return render(request, template, context)
