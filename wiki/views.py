from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from django.utils import timezone
from django.shortcuts import redirect , get_object_or_404, render
from wiki.models import WikiPage
from wiki.forms import EditArticleForm, AddArticleForm, DeleteForm
from wiki.wikiparser import WikiParser

class IndexPage(ListView):
    template_name = 'wiki/index.html'
    context_object_name = 'pages_list'
    
    def get_queryset(self):
        return WikiPage.objects.order_by('-public_date')
    
class AddPage(CreateView):
    template_name = 'wiki/add.html'
    model = WikiPage
    form_class = AddArticleForm
    fields = ['url_title', 'title', 'text']
    slug_field = 'url'
    slug_url_kwarg = 'page'
    
    def get_initial(self):
        initial = super(AddPage, self).get_initial()
        initial_edited = initial.copy()
        if 'page' in self.kwargs:
            initial_edited['url_title'] = self.kwargs['page']
        return initial_edited
    
    def form_valid(self, form):
        self.obj = form.save(commit=False)
        self.obj.public_date = timezone.now()
        self.obj.url = self.obj.url_title + '/' + self.obj.title
        try:
            WikiPage.objects.get(url = self.obj.url)
            return render(self.request, 'add.html', dictionary = {'form': form, 'exist': True})
        except WikiPage.DoesNotExist:
            self.obj.save()
            
            return redirect('page', self.obj.url)
    
class Page(DetailView):
    model = WikiPage
    template_name = 'wiki/page.html'
    slug_field = 'url'
    slug_url_kwarg = 'page'
    
    def get_context_data(self, *args, **kwargs):
        context = super(Page, self).get_context_data(**kwargs)
        
        context['children'] = WikiPage.objects.filter(url__startswith = self.kwargs['page'] + '/')
        
        page = get_object_or_404(WikiPage, url=self.kwargs['page'])
        wp = WikiParser(page.text)
        page.text = wp.get_text()
        context['page'] = page
        
        
        temp_url = page.url[:page.url.rfind(page.title) - 1]
        try:
            parent = WikiPage.objects.get(url=temp_url)
        except WikiPage.DoesNotExist:
            parent = False
        context['parent'] = parent
        
        return context
    
class EditPage(UpdateView):
    template_name = 'wiki/edit.html'
    model = WikiPage
    form_class = EditArticleForm
    fields = ['title', 'text']
    slug_field = 'url'
    slug_url_kwarg = 'page'
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.public_date = timezone.now()
        obj.save()
        return redirect('page', obj.url)
    
class DeletePage(DeleteView):
    template_name = 'wiki/delete.html'
    model = WikiPage
    form_class = DeleteForm
    fields = []
    slug_field = 'url'
    slug_url_kwarg = 'page'
    
    def post(self, request, *args, **kwargs):
        if 'yes_delete' in request.POST:        
            try:
                WikiPage.objects.get(url=kwargs['page']).delete()
                return redirect('index')
            except WikiPage.DoesNotExist:
                return render(request, 'delete.html', dictionary={'error': True})
        elif 'no_delete' in request.POST:
            return redirect('page', kwargs['page'])        

def error404(request):
    temp = request.path.split('/')
    url = '/'.join(temp[2:-1])
    return render(request, 'wiki/404.html', dictionary={'path_url':url})
    