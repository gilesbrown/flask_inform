import types
from operator import methodcaller
from jinja2 import evalcontextfilter, Markup, escape


from collections import namedtuple
Item = namedtuple('Item', 'value id')

#from informref.elements import Value, Link, Form, Input, Select

class Value(object):
    pass

class Link(unicode):
    pass

class Form(object):
    pass
class Select(object):
    pass
class Input(object):
    pass

@evalcontextfilter
def inform_value(eval_ctx, value):

    if isinstance(value, Value):
        id = value.id
        value = value.value
    else:
        id = None

    module = eval_ctx.environment.get_template('macros.html').module
    if hasattr(value, '__iter__'):
        if hasattr(value, 'items'):
            return module.inform_dl(value, id)
        else:
            return module.inform_ol(value, id)
    elif isinstance(value, Link):
        return module.inform_link(value, id)
    else:
        result = escape(value)
    if eval_ctx.autoescape:
        result = Markup(result)
    return result

_dispatch_by_type = {
    types.ListType: 'inform_ol',
    str: 'inform_str',
    unicode: 'inform_str',
    type(None): 'inform_none',
}

def default_x(module, item, id):
    return repr(item)


@evalcontextfilter
def inform_item(eval_ctx, item):
    print "INFORM ITEM?", repr(item), isinstance(item, Item)
    module = eval_ctx.environment.get_template('macros.html').module
    if isinstance(item, Item):
        args = (item.value, item.id)
    else:
        args = item

    macro = _dispatch_by_type.get(type(args[0]), 'inform_value')
    print "IS IT?", args, macro, type(args[0])
    return getattr(module, macro)(*args)


@evalcontextfilter
def inform_form_field(eval_ctx, item):
    module = eval_ctx.environment.get_template('macros.html').module
    if isinstance(item, Select):
        return module.inform_form_select(item)
    elif isinstance(item, Input):
        return module.inform_form_input(item.name, item.type)
    result = escape(item)
    if eval_ctx.autoescape:
        result = Markup(result)
    return result

inform_filters = {
    'inform_value': inform_value,
    'inform_item': inform_item,
    'inform_form_field': inform_form_field,
}
