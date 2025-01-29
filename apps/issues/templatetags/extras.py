from django import template
from apps.issues.services import language_services

register = template.Library()

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter
def lang_name(code):
    """concatenate arg1 & arg2"""
    return language_services.get_language_name_from_code(code)


@register.tag(name="ifequal")
def do_ifequal(parser, token):
    try:
        tag_name, value, arg = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("'ifequal' tag requires two arguments")

    nodelist = parser.parse(("endifequal",))
    parser.delete_first_token()
    return IfequalNode(nodelist, value, arg)

class IfequalNode(template.Node):
    def __init__(self, nodelist, value, arg):
        self.nodelist = nodelist
        self.value = value
        self.arg = arg

    def render(self, context):
        value = template.Variable(self.value).resolve(context)
        arg = template.Variable(self.arg).resolve(context)
        print(self.nodelist)
        if value == arg:
            return self.nodelist.render(context)
        return 'not'