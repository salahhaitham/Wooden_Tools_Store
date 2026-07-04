from odoo import  fields, models,api
from odoo.exceptions import ValidationError


class TechnicalOrder(models.Model):
    _name = 'technical.order'

    name = fields.Char(
        string='Sequence',
        readonly=True,
        default='New'
    )
    request_name = fields.Char(
        string='Request Name',
        required=True
    )
    requested_by = fields.Many2one(
       'res.users',
        required=True,
        default=lambda self: self.env.user,
        string='Requested By'
    )
    custormer_id=fields.Many2one('res.partner',required=True,domain=[('is_tech_offer','=',True)])
    start_date = fields.Datetime(string='Start Date',default=fields.Date.today())
    end_date = fields.Date(string='End Date')
    rejection_reason = fields.Char(string='Rejection Reason',readonly=True)
    total_price=fields.Float(string='Total Price',readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_be_approved', 'To Be Approved'),
        ('approve', 'Approved'),
        ('reject', 'Rejected'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft')
    technical_order_ids = fields.One2many('technical.order.line','technical_order_id')
    total = fields.Float(string="Total",compute='_compute_technical_order_ids')
    sale_order_ids = fields.One2many(
        'sale.order','technical_order_id'
    )
    sale_order_count = fields.Integer(
        compute='_compute_purchase_order_count'
    )
    def action_view_orders(self):

        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Orders',
            'res_model': 'sale.order',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.sale_order_ids.ids)],
        }

    

    def _compute_purchase_order_count(self):
        for rec in self:
            rec.sale_order_count = len(rec.sale_order_ids)

    @api.depends('technical_order_ids.total_price')
    def _compute_technical_order_ids(self):

        for rec in self:
            rec.total = sum(rec.technical_order_ids.mapped('total_price'))

    @api.model
    def create(self, vals_list):
        res = super().create(vals_list)
        if res.name == "New":
            res.name = self.env['ir.sequence'].next_by_code('tools_order_seq')
        return res

    def action_submit_for_approve(self):
        self.state = 'to_be_approved'

    def action_cancel(self):
        self.state = 'cancel'

    def action_draft(self):
        self.state = 'draft'

    def action_approve(self):
        self.state = 'approve'

        sale_manager_group = self.env.ref(
            'sales_team.group_sale_manager'
        )

        users = self.env['res.users'].search([]).filtered(
            lambda u: sale_manager_group in u.group_ids
        )
        print(users.ids)

        for user in users:
            print("User:", user.name)
            print("User:", user.name)
            print("Email:", user.partner_id.email)

            if user.partner_id.email:
                print("Entered IF")
            if user.partner_id.email:
                mail = self.env['mail.mail'].create({
                    'subject': 'Technical Order Approved',
                    'body_html': f"""
                        <p>Hello {user.name},</p>
                        <p>
                            Technical Order
                            <strong>{self.name}</strong>
                            has been approved.
                        </p>
                    """,
                    'email_to': user.partner_id.email,
                })

                print("Mail Record:", mail)
                print("Before Send:", mail.state)

                mail.send()
                print(mail.failure_reason)

                print("After Send:", mail.state)


    def create_sale_order(self):

        order_lines = []

        for line in self.technical_order_ids:
            confirmed_qty = sum(
                self.sale_order_ids.filtered(
                    lambda so: so.state == 'sale'
                ).mapped(
                    lambda so: sum(
                        so.order_line.filtered(
                            lambda l: l.product_id == line.product_id
                        ).mapped('product_uom_qty')
                    )
                )
            )
            remaining_qty = line.quantity - confirmed_qty

            order_lines.append((0, 0, {
                'product_id': line.product_id.id,
                'product_uom_qty': remaining_qty,
                'price_unit': line.price,

            }))
        if remaining_qty > 0 :
         sale_order = self.env['sale.order'].create({
            'partner_id': self.custormer_id.id,
            'technical_order_id': self.id,
            'order_line': order_lines,
        })
        else :
            raise ValidationError("remaining_qty less than 1")





    def action_reject(self):
         pass

class TechnicalOrderLine(models.Model):
    _name = 'technical.order.line'
    _order = 'id'
    technical_order_id = fields.Many2one('technical.order')
    product_id = fields.Many2one('product.product')
    description = fields.Char(string='Description')
    sequence = fields.Integer(
        string='Line No',
        compute='_compute_sequence',
    readonly=True,
    store=False
    )
    quantity = fields.Integer(string='Quantity',default=1)
    price=fields.Float(string='Price')
    total_price = fields.Float(string='Total',compute='_compute_total_price')

    @api.depends('quantity', 'price')
    def _compute_total_price(self):
        for line in self:
            line.total_price = line.quantity * line.price

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.description = self.product_id.name
            self.price = self.product_id.lst_price

    @api.depends('technical_order_id.technical_order_ids')
    def _compute_sequence(self):
        for order in self.mapped('technical_order_id'):
            for index, line in enumerate(order.technical_order_ids, start=1):
                line.sequence = index















