from odoo import api,fields,models



class Res_Partner (models.Model):
    _inherit = 'res.partner'

    is_tech_offer=fields.Boolean(string='Is Tech Offer?')
