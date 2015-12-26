from django import template

register = template.Library()


@register.filter
def page_range(page):
    if page.paginator.num_pages != 1:
        for i in page.paginator.page_range:
            if page.number - 3 < i < page.number + 3:
                yield i
