from django.http import HttpResponse

def home(request):
    register_login = '''
                        <a href="/main/register/"><button>register</button></a>
                        <a href="/main/login/"><button>login</button></a>
                    '''
    return HttpResponse(register_login)