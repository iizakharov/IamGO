from django.views.generic import ListView

from mainapp.models import Event, EventCategory


def get_main_menu():

    return EventCategory.objects.filter(is_active=True).order_by('-name')


class SearchView(ListView):
    template_name = 'searchapp/search.html'
    paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        my_context = super().get_context_data(*args, **kwargs)
        my_context['page_title'] = 'Поиск'
        my_context['main_menu'] = get_main_menu()[:8]
        my_context['count'] = self.count or 0
        my_context['query'] = self.request.GET.get('q')

        return my_context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)

        if query is not None:
            events_results = Event.objects.search(query)
            qs = sorted(
                events_results,
                key=lambda instance: instance.pk,
                reverse=True
            )
            self.count = len(qs)  # since qs is actually a list

            return qs

        return Event.objects.none()  # just an empty queryset as default
