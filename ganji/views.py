from django.shortcuts import render
from ganji.models import ItemInfo
from django.core.paginator import Paginator

def area_data(time):
    pipeline = [
        {'$match': {'time':time}},
        {'$group': {'_id': {'$slice': ['$area', 0, 1]}, 'counts': {'$sum': 1}}},
        {'$sort': {'counts': -1}}
    ]
    total_sum = 0
    for i in ItemInfo._get_collection().aggregate(pipeline):
        total_sum += i['counts']
    for i in ItemInfo._get_collection().aggregate(pipeline):
        data = [i['_id'][0],i['counts']/total_sum]
        yield data

series_area = [i for i in area_data(1)]

def cate_data(time):
    pipeline = [
        {'$match': {'time':time}},
        {'$group': {'_id': {'$slice':['$cates',2,1]}, 'counts': {'$sum': 1}}},
        {'$sort': {'counts': -1}}
    ]
    total_sum = 0
    for i in ItemInfo._get_collection().aggregate(pipeline):
        total_sum += i['counts']
    for i in ItemInfo._get_collection().aggregate(pipeline):
        data = [i['_id'][0],i['counts']/total_sum]
        yield data
series_cate = [i for i in cate_data(1)]


# all cate
def all():
    pipeline = [
        {'$group': {'_id': {'$slice':['$cates',2,1]}, 'counts': {'$sum': 1}}},
        {'$sort': {'counts': -1}}
    ]
    for i in ItemInfo._get_collection().aggregate(pipeline):
        data = {
            'name': i['_id'][0],
            'data': [i['counts']],
            'type': 'column'
        }
        yield data
series_all = [i for i in all()]

# Top 3
def top3(date1, date2, area, limit):
    pipeline = [
        {'$match': {'$and': [{'pub_date': {'$gte': date1, '$lte': date2}}, {'area': {'$all': area}}]}},
        {'$group': {'_id': {'$slice':['$cates',2,1]}, 'counts': {'$sum': 1}}},
        {'$limit': limit},
        {'$sort': {'counts': -1}}
    ]
    for i in ItemInfo._get_collection().aggregate(pipeline):
        data = {
            'name': i['_id'][0],
            'data': [i['counts']],
            'type': 'column'
        }
        yield data


series_CY = [i for i in top3('2015.12.25', '2015.12.27', ['朝阳'], 3)]
series_HD = [i for i in top3('2015.12.25', '2015.12.27', ['海淀'], 3)]
series_TZ = [i for i in top3('2015.12.25', '2015.12.27', ['通州'], 3)]


# Create your views here.
def index(request):
    limit = 15
    arti_info = ItemInfo.objects[:2]
    paginator = Paginator(arti_info, limit)
    page = request.GET.get('page', 1)
    loaded = paginator.page(page)

    context = {
        'ItemInfo': loaded,
        'counts': arti_info.count(),
        'last_time': arti_info.order_by('-pub_date').limit(1)
    }
    return render(request, 'index_data.html', context)


def chart(request):
    context = {
        'chart_CY': series_CY,
        'chart_TZ': series_TZ,
        'chart_HD': series_HD,
        'chart_ALL': series_all,
        'chart_CATE': series_cate,
        'chart_AREA': series_area
    }
    return render(request, 'chart.html', context)
