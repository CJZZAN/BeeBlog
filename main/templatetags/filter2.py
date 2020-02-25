from django import template
from django.utils.safestring import mark_safe
register = template.Library()


@register.simple_tag
def filter_article_type(article_type_list,arg_dict):
    ret = []

    for i in article_type_list:
        try:
            n1 = arg_dict['article_type_id']
            if i.type_id == n1:
                temp = '<li><a class="active" href="/main/home-%s.html">%s</a></li>' % (i.type_id, i.type_name,)
            else:
                temp = '<li><a href="/main/home-%s.html">%s</a></li>' % (i.type_id, i.type_name,)
            ret.append(temp)
        except:
            temp = '<li><a href="/main/home-%s.html">%s</a></li>' % (i.type_id, i.type_name,)
            ret.append(temp)
    return mark_safe(''.join(ret))