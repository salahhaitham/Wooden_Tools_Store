from openpyxl.styles.builtins import total

from odoo import fields, models
from odoo.exceptions import ValidationError


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

    def action_confirm(self):
        for rec in self:
            technical_order = rec.technical_order_id

            for to_line in technical_order.technical_order_ids:
                confirmed_qty = sum(
                    technical_order.sale_order_ids.filtered(
                        lambda so: so.state == 'sale'
                    ).mapped(
                        lambda so: sum(
                            so.order_line.filtered(
                                lambda l: l.product_id == to_line.product_id
                            ).mapped('product_uom_qty')
                        )
                    )
                )
                print("confirmed_qty", confirmed_qty)

                total_qty=sum(rec.order_line.filtered(lambda l:l.product_id==to_line.product_id).mapped('product_uom_qty'))
                remaining_qty = to_line.quantity - confirmed_qty
                print("remaining_qty",remaining_qty)
                if total_qty > remaining_qty:
                    raise ValidationError(f'{to_line.product_id.display_name} more than Total Quantity{to_line.quantity}')

                else:

                    print("to_line_qty",to_line.quantity)
        print("confirmed_qty 2:> ", confirmed_qty)
        return super().action_confirm()


    def write(self, vals):
        res = super().write(vals)
        self.validation_lines()
        return res
    def validation_lines(self):
        for rec in self:
           technical_order = rec.technical_order_id

           for to_line in technical_order.technical_order_ids:

            total_qty = sum(
                rec.order_line.filtered(lambda l: l.product_id == to_line.product_id).mapped('product_uom_qty'))

            if total_qty > to_line.quantity:
                raise ValidationError(f'{to_line.product_id.display_name} more than Total Quantity{to_line.quantity}')

    def action_view_technical_order(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Technical Order',
            'res_model': 'technical.order',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.technical_order_id.id)],
        }
