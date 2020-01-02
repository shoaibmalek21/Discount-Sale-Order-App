# -*- coding: utf-8 -*-
from odoo import fields,models,api,_
from odoo.exceptions import UserError, ValidationError
import numpy as np

class discount_on_sale_order(models.Model):
	_name = 'discount.on.sale.order'
	_discription = 'Discount on Sale Order'
  	
	product_id = fields.Many2one('product.product', string="Type of Discount",domain=['|',('default_code','=','D-FIXED'),('default_code','=','D-PER')])
	discount_value = fields.Float(string='Discount Value')

	@api.multi
	def add_discount_on_sale_order(self):
		order_id = self._context.get('active_id',False)
		product_id = self.env['product.product'].search(['|',('default_code','=','D-FIXED'),('default_code','=','D-PER')])
		product_id_name = self.env['product.product'].search([('name','=','Fixed Discount')])
		print(product_id_name.name,'#$%#$%#$%#$%')
			
		# disc_total = self.env['sale.order'].browse(self._context.get('active_id'))
		disc_total = self.env['sale.order'].browse(self._context.get('active_id'))
		print(disc_total.discounted_amount,'$$$$')
		discount_value = 0.0
		active_ids = self.env['sale.order'].browse(self._context.get('active_id'))

		for i in active_ids:
			i.update({
				'discount_value': self.discount_value,
				'product_ids': self.product_id,
				})
				
		if order_id:
			for rec in disc_total.order_line:	
				if (rec.product_id in product_id):
					print(rec.product_id in product_id ,'****')
					raise UserError(_('Delete Previous %s record from Order. ') % self.product_id.name)
			else:
				print(rec.product_id in product_id ,'****')

				values = {'product_id': self.product_id.id,
				'discount_value': self.discount_value,
			 	# 'price_unit': (self.discount_value) * (-1),
			 	'price_unit': (disc_total.discounted_amount)*(-1),
				'order_id': order_id,	                      
				}

				sale_order_line = self.env['sale.order.line'].create(values)
