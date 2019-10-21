from django.template.loader import render_to_string


def MediaLib():
    return render_to_string('media/widget.html')
