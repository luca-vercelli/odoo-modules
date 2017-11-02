# -*- coding: utf-8 -*-

from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

try:
    from mako.template import Template
    import re
    import Queue
    import set
except:
    pass

class ViewDict(dict):
    """
    This dict search keys in the ir.ui.view table, too.
    Keys that are not found are stored in self._unknownKeys for better performance.
    """
    _unknownKeys = set()
    
    def __init__(self, values):
        super(ViewDict, self).__init__()
        self.values = values    #oppure update?

    def __getitem__(self, key):
        if key in self._unknownKeys:
            raise KeyError(key)
        try:
            return super(ViewDict, self).__getitem__(self, key)
        except KeyError:
            view_id = Engine._find_mustache_template(key)
            if view_id is not None:
                tpl = Template(view_id.arch)
                rnd = tpl.render(**values)    #ignore **options
                self[key] = rnd
                return rnd
            else:
                self._unknownKeys.add(key)
                raise KeyError(key)

    def __putitem__(self, key, value):    
        if key in self._unknownKeys:
            self._unknownKeys.remove(key)
        return super(ViewDict, self).__putitem__(self, key, value)

#see base/ir/ir_qweb/ir_qweb.py
class Engine(models.AbstractModel):
    """
    Mustache rendering engine
    """
    _inherit = 'ir.qweb'

    @api.model
    def render(self, id_or_xml_id, values=None, **options):
        """ render(id_or_xml_id, values, **options)

        Render the template specified by the given name.

        :param id_or_xml_id: name or etree (see get_template)
        :param dict values: template values to be used for rendering
        :param options: used to compile the template (the dict available for the rendering is frozen)
            * ``load`` (function) overrides the load method
            * ``profile`` (float) profile the rendering (use astor lib) (filter
              profile line with time ms >= profile)
        """
        
        view_id = self._find_mako_template(id_or_xml_id)
        if view_id is not None:
        
                # only in this case, render using Mako
                
                if values is None:
                    values = {}
                
                values['views'] = ViewDict(values)

                def currency(amount):
                    #which locale ???
                    return locale.format("%.2f", amount, grouping=True)
                values['currency'] = currency

                def date(d):
                    return Date(d).strfmt('dd/MM/YYYY') #this is Italian only :(
                values['date'] = date

                tpl = Template(view_id.arch)
                return tpl.render(**values)    #ignore **options
        
        # In all other cases, render with super()
        return super(Engine, self).render(id_or_xml_id, values, **options)

    def _find_mako_template(self, id_or_xml_id):
    
        view_id = None
        
        if isinstance(id_or_xml_id, ( int, long ) ):
            view_id = self.env['ir.ui.view'].search([('id', '=', id_or_xml_id)])
            #should check auth...
        elif isinstance(id_or_xml_id, basestring):
            view_id = self.env.ref(id_or_xml_id)
        
        if (view_id is not None) and (len(view_id) == 1) :
            if view_id[0].type and view_id[0].type == "mako":
                return view_id[0]
        
        return None
        

