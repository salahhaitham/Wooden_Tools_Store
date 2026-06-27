import typing
from typing import Sequence, Self

from odoo import models,fields



class Owner(models.Model):
    _name='owner'


    name=fields.Char(size=20)
    phone=fields.Char(size=20)
    address=fields.Char(size=20)






