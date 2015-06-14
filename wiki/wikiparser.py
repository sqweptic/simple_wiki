import re
from django.core.urlresolvers import reverse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from wiki.models import WikiPage

class WikiParser():    
    def __init__(self, text = ''):
        self.text = text
         
    def set_text(self, text):
        self.text = text
         
    def get_text(self):
        self._process()
        return self.text
     
    def _process(self):
        if self.text:
            self._find_quote_symbols()
            self._find_bold_tag()
            self._find_italic_tag()
            self._find_underline()
            self._find_external_links()
            self._find_own_links()
            self._find_new_line_tag()
              
    def _find_new_line_tag(self):
        self.text = self.text.replace('\r\n', '<br>\r\n')
         
    def _find_bold_tag(self):
        self.text = re.sub(r'[*]{2}(?P<line>[\w]+)[*]{2}', r'<b>\1</b>', self.text)
         
    def _find_italic_tag(self):
        self.text = re.sub(r'[/]{2}(?P<line>[\w]+)[/]{2}', r'<i>\1</i>', self.text)
         
    def _find_underline(self):
        self.text = re.sub(r'[_]{2}(?P<line>[\w]+)[_]{2}', r'<u>\1</u>', self.text)
         
    def _find_quote_symbols(self):
        i = j = 0
        complite_text = ''
        while True:
            i = self.text.find(r'"', j)
            j = self.text.find(r'"', i+1)
            if i < 0 or j < 0:
                break
            text_begin = self.text[:i]
            text_end = self.text[j+1:]
            working_text = self.text[i:j+1]
            quote_simbols = '«' + working_text[1:-1] + '»'
            complite_text = text_begin + quote_simbols + text_end
            j += 2
            i = j
        if complite_text:
            self.text = complite_text
         
    def _find_own_links(self):
        text_begin = text_end = working_text = ''
        brace = ''
        complite_text = self.text
        while True:
            text_begin, brace, text_end = complite_text.partition('[')
            if not brace:
                complite_text = ''.join([text_begin, brace, text_end])
                break
            working_text, brace, text_end_new = text_end.partition(']]')
            if not brace:
                complite_text = ''.join([text_begin, brace, text_end])
                break
            
            if working_text.find('\n') > -1:
                working_text = 'ERROR SYNTAX'
                complite_text = ''.join([text_begin, working_text, text_end])
                continue
            
            url, space, name = working_text.partition(' ')
            
            v = URLValidator()
            try:
                v(url)
                external = True
                url = False
            except ValidationError:
                external = False
                
            try:
                WikiPage.objects.get(url=url)
                found_url = True
            except WikiPage.DoesNotExist:
                found_url = False                
                
            if not space or not name:
                tag = '<a style="color:red;" href="{!s}">error: syntax</a>'.format(url)
            elif external:
                tag = '<a style="color:red;" href="">error: external link</a>'
            elif not found_url:
                tag = '<a style="color:red;" href="{!s}">{!s}</a>'.format(reverse('page', args=[url,]), name)
            else:
                tag = '<a href="{!s}">{!s}</a>'.format(reverse('page', args=[url,]), name)
                
            complite_text = ''.join([text_begin, tag, text_end_new])
        self.text = complite_text
            
    def _find_external_links(self):
        text_begin = ''
        text_end = ''
        working_text = ''
        brace = ''
        complite_text = self.text
        while True:
            text_begin, brace, text_end = complite_text.partition('[[')
            if not brace:
                complite_text = ''.join([text_begin, brace, text_end])
                break
            working_text, brace, text_end_new = text_end.partition(']]')
            if not brace:
                complite_text = ''.join([text_begin, brace, text_end])
                break
            
            if working_text.find('\n') > -1:
                working_text = 'ERROR SYNTAX'
                complite_text = ''.join([text_begin, working_text, text_end])
                continue
            url, space, name = working_text.partition(' ')
            
            v = URLValidator()
            try:
                v(url)
            except ValidationError:
                url = False
                
            if not space or not name or url == name:
                tag = '<a style="color:red;" href="{!s}">error</a>'.format(url)
            elif not url:
                tag = '<a style="color:red;" href="">error: internal link</a>'
            else:
                tag = '<a href="{!s}">{!s}</a>'.format(url, name)
                
            complite_text = ''.join([text_begin, tag, text_end_new])
        self.text = complite_text
            
                
                

if __name__ == "__main__":
    test = """text **text** *est*asdg**\n\n\t aasdf __dfgdfg__ -_sdg_- __sdgsdg_a \n [[http://yandex.ru яндекс]]
             [[яндекс]] [[zaq zaq]] \n **sdfhsrth**
            *jhgbkjb**[[Ошибка! Недопустимый объект гиперссылки.]
            
            //ugiugikjb//
            j//oih00i//
            //ohojhnkj/
            
            __knonokn__
            _89gh9u_
            
            [igbuhgvkuguy777 hjbhvl]]
            
            [qwerty qwerty]]
            [qwerty]]
            q[werty ]]
            """
    p = WikiParser(test)
    print(p.get_text())
    