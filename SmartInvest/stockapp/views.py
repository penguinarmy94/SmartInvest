

from django.shortcuts import render
from django.http import HttpResponse

linksCards = [
{'header':'Invest',
'body':'','src':'/invest'},
{'header':'Portfolio','body':'','src':'/portfolio'},
{'header':'Trends','body':'','src':'/trends'},
{'header':'About','body':'','src':'/about'}
]

teamsCards = [
{
'title':'Marianne Paulson',
'backText':' I am a Software Engineer at Lawrence Livermore National Laboratory and love the field of Software Engineering. On my free time I like to hang out with my family and occationally explore my endurance limits on all the beautiful trails California has to offer.',
'img':'/img/marianne_paulson.jpg'
},
{
'title':'Luis Otero',
'backText':'I am a Software Engineering student at San Jose State University working on his MS degree. Most of my experience has been in Android development and PHP server-side web development. Worked on the invest and portfolio portion of this project.',
'img':'/img/luis_otero.jpg'
},
{
'title':'Lalini Wudali',
'backText':'I work as a Technical Program Manager for an EMR (Electronic Medical Records) project at a Home Health care company. In my free time, I love to spend time with my family and sing Indian classical music',
'img':'/img/lalini_wudali.jpeg'
},
{
'title':'Arturo Montoya',
'backText':'I have a bachelor’s degree from SJSU in Computer Engineering. On my down time, I like going on walks with my dog and watching him run around playing with other dogs. I also enjoy challenging myself by learning new things such as juggling (next on my list slack-lining).',
'img':'/img/arturo_montoya.jpeg'
}
]
def home(request):
    return render(request, 'home.html',{'cards':linksCards})
def trends(request):
    return render(request, 'trends.html')
def about(request):
    return render(request, 'about.html')
def team(request):
    return render(request, 'team.html',{'cards':teamsCards})
def services(request):
    return render(request, 'services.html')
