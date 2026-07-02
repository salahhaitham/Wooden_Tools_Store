from odoo import fields, models



class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    technical_order_id = fields.Many2one(
        'technical.order',
    )
    sale_order_count = fields.Integer(
        compute='_compute_purchase_request_count'
    )

    def _compute_purchase_request_count(self):
        for rec in self:
            rec.sale_order_count = len(rec.technical_order_id)

    def action_view_technical_order(self):
        print("sadasda")
        # return {
        #     'type': 'ir.actions.act_window',
        #     'name': 'technical order',
        #     'res_model': 'technical.order',
        #     'view_mode': 'list,form',
        #     'domain': [('id', 'in', self.sale_order_id.id)],
        # }