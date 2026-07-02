

from odoo import models, fields, api


class CancelAppointmentWizard(models.TransientModel):
    _name = 'cancel.order'
    _description = 'Cancel Appointment Wizard'



    reason = fields.Text(string="Cancel Reason", required=True)
    technical_order_id = fields.Many2one('technical.order')



    def confirm_button(self):
        print(self.technical_order_id)
        print(self.reason)
        self.technical_order_id.rejection_reason=self.reason
        self.technical_order_id.state='reject'
        print("hello")


