# 对article.html使用simple tag进行简化，各司其职
from django import template
from django.utils.safestring import mark_safe
register = template.Library()


@register.simple_tag
def filter_all(arg_dict,k):
    """
    {% if arg_dict.article_type_id == 0 %}
        <a class="choosed decoration" href="/article-0-{{ arg_dict.category_id }}.html">全部</a>
    {% else %}
        <a class="decoration" href="/article-0-{{ arg_dict.category_id }}.html">全部</a>

    {% if arg_dict.category_id == 0 %}
        <a class="choosed decoration" href="/article-{{ arg_dict.article_type_id }}-0.html">全部</a>
    {% else %}
        <a class="decoration" href="/article-{{ arg_dict.article_type_id }}-0.html">全部</a>
    :param arg:
    :return:
    """
    if k == 'article_type_id':
        n1 = arg_dict[k]
        n2 = arg_dict['category_id']
        if n1 == 0:
            ret = '<a class="choosed decoration" href="/article-0-%s.html">全部</a>' % n2
        else:
            ret = '<a class="decoration" href="/article-0-%s.html">全部</a>' % n2
    else:
        n1 = arg_dict[k]
        n2 = arg_dict['article_type_id']
        if n1 == 0:
            ret = '<a class="choosed decoration" href="/article-%s-0.html">全部</a>'% n2
        else:
            ret = '<a class="decoration" href="/article-%s-0.html">全部</a>'% n2
    return mark_safe(ret)


@register.simple_tag
def filter_article_type(article_type_list, arg_dict):
    """
    {% for i in article_type_list %}
        {% if i.id == arg_dict.article_type_id %}
            <a class="choosed decoration" href="/article-{{ i.id }}-{{ arg_dict.category_id }}.html">{{ i.caption }}</a>
        {% else %}
            <a class="decoration" href="/article-{{ i.id }}-{{ arg_dict.category_id }}.html">{{ i.caption }}</a>
        {% endif %}
    {% endfor %}
    {% for i in category_list %}
        {% if i.id == arg_dict.category_id %}
            <a class="choosed decoration" href="/article-{{ arg_dict.article_type_id }}-{{ i.id }}.html">{{ i.caption }}</a>
        {% else %}
            <a class="decoration" href="/article-{{ arg_dict.article_type_id }}-{{ i.id }}.html">{{ i.caption }}</a>
        {% endif %}
    {% endfor %}
    :return:
    """
    ret = []
    n1 = arg_dict['article_type_id']
    n2 = arg_dict['category_id']

    for i in article_type_list:
        if i.id == n1:
            temp = '<a class="choosed decoration" href="/article-%s-%s.html">%s</a>' % (i.id, n2, i.type_name,)
        else:
            temp = '<a class="decoration" href="/article-%s-%s.html">%s</a>' % (i.id, n2, i.type_name)
        ret.append(temp)
    return mark_safe(''.join(ret))


@register.simple_tag
def filter_sarticle_type(category_list, arg_dict):
    ret = []
    n1 = arg_dict['category_id']
    n2 = arg_dict['article_type_id']

    for i in category_list:
        if i.id == n1:
            temp = '<a class="choosed decoration" href="/article-%s-%s.html">%s</a>' % (n2, i.id, i.caption,)
        else:
            temp = '<a class="decoration" href="/article-%s-%s.html">%s</a>' % (n2, i.id, i.caption)
        ret.append(temp)
    return mark_safe(''.join(ret))