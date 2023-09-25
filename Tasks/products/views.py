from django.http import HttpResponse
from .models import Product, Lesson, User, View
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Sum
from django.template import loader

def index(request):
    template = loader.get_template("Tasks/index.html")
    context = {}
    return HttpResponse(template.render(context, request))

def full_lessons_list(request, user_id):
    this_user = get_object_or_404(User, pk=user_id)

    s = set()
    for p in list(this_user.products.all()):
        s = s.union(set(p.lessons.all()))
        
    result = []
    for l in s:
        data = View.objects.filter(user=this_user, lesson=l)
        if len(data) > 0:
            data = data[0]
            result.append("Lesson's name: " + str(l) + ", Viewed time: " + str(data.time) + ", Viewing status: " + str(data.viewed))
    
    template = loader.get_template("Tasks/full_lessons_list.html")
    context = {
        "lessons_list": result,
    }
    return HttpResponse(template.render(context, request))

def lessons_list(request, user_id, product_id):
    this_user = get_object_or_404(User, pk=user_id)
    this_product = get_object_or_404(Product, pk=product_id)
        
    result = []
    for l in list(this_product.lessons.all()):
        data = View.objects.filter(user=this_user, lesson=l)
        if len(data) > 0:
            data = data[0]
            result.append("Lesson's name: " + str(l) + ", Viewed time: " + str(data.time) + ", Viewing status: " + str(data.viewed))
    
    template = loader.get_template("Tasks/lessons_list.html")
    context = {
        "lessons_list": result,
    }
    return HttpResponse(template.render(context, request))

def statistics(request):
    stat_list = []
    for p in list(Product.objects.all()):
        stat_list.append("Product: %s" % str(p))
        number = View.objects.filter(lesson__in=list(p.lessons.all())).aggregate(Count("id"))
        S = View.objects.filter(lesson__in=list(p.lessons.all())).aggregate(Sum("duration"))
        pupils = 0
        stat_list.append("Number of viewed lessons: %d" %(number["id__count"]))
        stat_list.append("Summary spent time: %d" %(S["duration__sum"]))
        
        for u in list(User.objects.all()):
            if p in list(u.products.all()):
                pupils += 1
        
        stat_list.append("Number of pupils: %d" %(pupils))

        percentage = float(100 * pupils / User.objects.all().aggregate(Count("id"))["id__count"])
        stat_list.append("Percentage of product purchase: %.2f%%" %(percentage))
        stat_list.append("")
    
    template = loader.get_template("Tasks/statistics.html")
    context = {
        "stat_list": stat_list,
    }
    return HttpResponse(template.render(context, request))
