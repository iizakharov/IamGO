from django.views.generic import ListView

from mainapp.models import Event


class SearchView(ListView):
    template_name = 'searchapp/view.html'
    paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)

        if query is not None:
            events_results = Event.objects.search(query)
            qs = sorted(events_results,
                        key=lambda instance: instance.pk,
                        reverse=True)
            self.count = len(qs)  # since qs is actually a list
            return qs
        return Event.objects.none()  # just an empty queryset as default
