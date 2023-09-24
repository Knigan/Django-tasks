from django.http import HttpResponse
from .models import Product, Lesson, User, View
from django.shortcuts import get_object_or_404
from django.db.models import Count, Sum


def full_lessons_list(request, user_id):
    this_user = get_object_or_404(User, pk=user_id)

    s = set()
    for p in list(this_user.products.all()):
        s = s.union(set(p.lessons.all()))
        
    result = []
    for l in s:
        data = View.objects.filter(user=this_user, lesson=l)[0]
        result.append("Lesson's name: " + str(l) + ", Viewed time: " + str(data.time) + ", Viewing status: " + str(data.viewed))
    
    if len(result) == 0:
        return HttpResponse("This user hasn't watched a single lesson")
    else:
        return HttpResponse(result)

def lessons_list(request, user_id, product_id):
    this_user = get_object_or_404(User, pk=user_id)
    this_product = get_object_or_404(Product, pk=product_id)
        
    result = []
    for l in list(this_product.lessons.all()):
        data = View.objects.filter(user=this_user, lesson=l)[0]
        result.append("Lesson's name: " + str(l) + ", Viewed time: " + str(data.time) + ", Viewing status: " + str(data.viewed))
    
    if len(result) == 0:
        return HttpResponse("This user hasn't watched a single lesson contained in this product")
    else:
        return HttpResponse(result)

def statistics(request):
    result = []
    for p in list(Product.objects.all()):
        result.append(str(p) + ": ")
        number = View.objects.filter(lesson__in=list(p.lessons.all())).aggregate(Count("id"))
        S = View.objects.filter(lesson__in=list(p.lessons.all())).aggregate(Sum("duration"))
        pupils = 0
        result.append("Number of viewed lessons equals %d, " %(number["id__count"]))
        result.append("Summary spent time equals %d, " %(S["duration__sum"]))
        
        for u in list(User.objects.all()):
            if p in list(u.products.all()):
                pupils += 1
        
        result.append("Number of pupils equals %d, " %(pupils))

        percentage = float(100 * pupils / User.objects.all().aggregate(Count("id"))["id__count"])
        result.append("Percentage of product purchase equals %.2f%%" %(percentage))

        
    return HttpResponse(result)
