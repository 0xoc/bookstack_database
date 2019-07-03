import jdatetime


def filter_date__exact(queryset, field, value):
    jalali_date = jdatetime.date(value.year, value.month, value.day)
    return queryset.filter(issue_date=jalali_date)


def filter_date__lt(queryset, field, value):
    jalali_date = jdatetime.date(value.year, value.month, value.day)
    return queryset.filter(issue_date__lt=jalali_date)


def filter_date__gt(queryset, field, value):
    jalali_date = jdatetime.date(value.year, value.month, value.day)
    return queryset.filter(issue_date__gt=jalali_date)
