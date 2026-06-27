from odoo import  fields, models,api



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

    def action_reject(self):
        pass

class TechnicalOrderLine(models.Model):
    _name = 'technical.order.line'

    technical_order_id = fields.Many2one('technical.order')
    product_id = fields.Many2one('product.product')
    description = fields.Char(string='Description')
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















