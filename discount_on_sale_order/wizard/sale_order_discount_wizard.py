# -*- coding: utf-8 -*-
from odoo import fields,models,api,_
from odoo.exceptions import UserError, ValidationError
import re


class sale_order_wizard(models.Model):
	_inherit = 'sale.order'
	
	discount_value = fields.Float(string='Discount Value')
	discounted_amount = fields.Float(compute='disc_amount', string='Discounted Amount',readonly=True)
	pricelist_id = fields.Many2one('product.pricelist',string='Pricelist')
	product_ids = fields.Many2one('product.product', string="Type of Discount",domain=['|',('default_code','=','D-FIXED'),('default_code','=','D-PER')])

	@api.depends('order_line.price_subtotal', 'product_ids', 'discount_value')
	def _amount_all(self):
		"""
		Compute the total amounts of the SO..
		"""
		for order in self:
			amount_untaxed = amount_tax  = amount_total = 0.0
			for line in order.order_line:
				amount_untaxed += line.price_subtotal
				amount_tax += line.price_tax

			if order.product_ids.default_code == 'D-FIXED':
				# amount_total = amount_untaxed + amount_tax - order.discount_value
				amount_total = amount_untaxed + amount_tax
			elif order.product_ids.default_code == 'D-PER':
				if order.discount_value < 100:
					amount_to_dis = (amount_untaxed + amount_tax) * (order.discount_value / 100)
					# amount_total = (amount_untaxed + amount_tax) - amount_to_dis
					amount_total = (amount_untaxed + amount_tax) 
				else:
					raise UserError(_('Discount percentage should not be greater than 100.'))
			else:
				amount_total = amount_untaxed + amount_tax
		   
			order.update({
				'amount_untaxed': amount_untaxed,
				'amount_tax': amount_tax,
				'amount_total': amount_total,
				})

	@api.one
	@api.depends('order_line.price_subtotal', 'product_ids', 'discount_value')
	def disc_amount(self):
		val = 0
		for line in self.order_line:
			val += line.price_tax
		if self.product_ids.default_code == 'D-FIXED':
			self.discounted_amount = self.discount_value
		elif self.product_ids.default_code == 'D-PER':
			amount_to_dis = (self.amount_untaxed + val) * (self.discount_value / 100)
			self.discounted_amount = amount_to_dis
		else:
			self.discounted_amount = 0
