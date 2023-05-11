from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

from .models import Novelchapters, Novelslist



def index(request):  
    novelslist = Novelslist.objects.all()

    return render(request,"index.html",{'novelslist':novelslist})

def novel(request, id):
    novelslist = Novelslist.objects.all()
    novID = id
    novelID = Novelslist.objects.filter(novel_id = id)
    #novelName =Novelslist.novel_name.filter(novel_id = id)  

    test = Novelchapters.objects.all()
    return render(request, "novel.html", {'test':test, 'novelID':novelID, 'novelslist':novelslist, 'novID':novID})

def chapter(request, id, num):
    chapter = Novelchapters.objects.get(chapter_num = num, novel_id = id)
    chapternumber = num
    return render(request, "chapter.html", {'chapter':chapter, 'chapternumber': chapternumber, 'novelID':id})


    #Do if no next chapter send to chapter not found page, or remove  < button on first and > button on last chapter
          