# -*- coding: utf-8 -*-
import time
import tempfile
import binascii
import xlrd
from odoo import models, fields, exceptions, api, _

import logging

_logger = logging.getLogger(__name__)
import pdb
import requests
from io import BytesIO
import codecs
import pdb

try:
    import xlwt
except ImportError:
    _logger.debug('Cannot `import xlwt`.')
try:
    import cStringIO
except ImportError:
    _logger.debug('Cannot `import cStringIO`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')


class Template(models.Model):
    _inherit = "product.template"

    to_be = fields.Boolean('To Be')


class ImportWizard(models.TransientModel):
    _name = "import.wizard"
    _description = 'Import Wizard'
    
    file = fields.Binary('File')

    def import_product_pictures_pre(self):
        fp = tempfile.NamedTemporaryFile(suffix=".xlsx")
        fp.write(binascii.a2b_base64(self.file))
        fp.seek(0)
        
        workbook = xlrd.open_workbook(fp.name)
        sheet = workbook.sheet_by_index(0)

        not_imported_list = []
        for row_num in range(0, sheet.nrows):
            row = sheet.row_values(row_num)

            product = self.env['product.template'].search([('default_code','=',str(int(row[1])))])
            if product:
                image_name = ''
                for i in range(3,18):
                    if '.jpg' in str(row[i]):
                        image_name = str(row[i])
                        break
                print(str(row[2]) + "="+image_name[1:])
                if image_name and image_name != '':
                    url = 'http://www.beardedirisflowers.com/pictures/product'
                    if 'big' in image_name:
                        url += '/big/'+image_name[1:]
                    elif 'middle' in image_name:
                        url += '/middle/' + image_name[1:]
                    elif 'small' in image_name:
                        url += '/small/' + image_name[1:]

                    # response = requests.get("https://i.imgur.com/ExdKOOz.png")
                    response = requests.get(url)
                    if response.status_code == 200:
                        image_bytes = BytesIO(response.content)
                        product[0].image_1920 = codecs.encode(response.content, 'base64')

            else:
                not_imported_list.append(row[2])

        print('Data not imported')
        print(not_imported_list)

    def import_product_pictures(self):
        fp = tempfile.NamedTemporaryFile(suffix=".xlsx")
        fp.write(binascii.a2b_base64(self.file))
        fp.seek(0)

        workbook = xlrd.open_workbook(fp.name)
        sheet = workbook.sheet_by_index(0)

        not_imported_list = []
        for row_num in range(1, sheet.nrows):
            row = sheet.row_values(row_num)

            product = self.env['product.template'].search([('default_code','=',str(int(row[2])))])
            if product:
                print ('Product:'+ (product.name or ""))
                url1 = str(row[4])
                url2 = str(row[5])
                url3 = str(row[6])
                url4 = str(row[7])

                if len(url1) > 0:
                    print('Url1:' + url1)
                    response1 = requests.get(url1)
                    if response1.status_code == 200:
                        product[0].image_1920 = codecs.encode(response1.content, 'base64')

                if len(url2) > 0:
                    print('Url2:' + url2)
                    response2 = requests.get(url2)
                    if response2.status_code == 200:
                        name = (product.name or '') + ':Image2'
                        image = codecs.encode(response2.content, 'base64')

                        product_image_id = self.env['product.image'].search([('name','=', name),('product_tmpl_id', '=', product.id)], limit=1)
                        if not product_image_id:
                            product_image_id =  product_image_id.create({'name': name, 'product_tmpl_id':product.id })
                        product_image_id.image_1920 = image

                if len(url3) > 0:
                    print('Url3:' + url3)
                    response3 = requests.get(url3)
                    if response3.status_code == 200:
                        name = (product.name or '') + ':Image3'
                        image = codecs.encode(response3.content, 'base64')

                        product_image_id = self.env['product.image'].search(
                            [('name', '=', name), ('product_tmpl_id', '=', product.id)], limit=1)
                        if not product_image_id:
                            product_image_id = product_image_id.create({'name': name, 'product_tmpl_id': product.id})
                        product_image_id.image_1920 = image

                if len(url4) > 0:
                    print('Url4:' + url4)
                    response4 = requests.get(url4)
                    if response4.status_code == 200:
                        name = (product.name or '') + ':Image4'
                        image = codecs.encode(response4.content, 'base64')

                        product_image_id = self.env['product.image'].search(
                            [('name', '=', name), ('product_tmpl_id', '=', product.id)], limit=1)
                        if not product_image_id:
                            product_image_id = product_image_id.create({'name': name, 'product_tmpl_id': product.id})
                        product_image_id.image_1920 = image

            else:
                not_imported_list.append(row[2])

        print('Data not imported')
        print(not_imported_list)

    def update_contacts_pre(self):
        fp = tempfile.NamedTemporaryFile(suffix=".xlsx")
        fp.write(binascii.a2b_base64(self.file))
        fp.seek(0)

        workbook = xlrd.open_workbook(fp.name)
        sheet = workbook.sheet_by_index(0)

        not_imported_list = []
        imported_list = []
        for row_num in range(0, sheet.nrows):
            row = sheet.row_values(row_num)

            partner = self.env['res.partner'].search([('email', '=', str(row[9]))], limit =1)
            if not partner:
                partner = self.env['res.partner'].search([('name', '=', str(row[2]))], limit =1)
                if not partner and '@' in str(row[8]):
                    partner = self.env['res.partner'].search([('email', '=', str(row[8]))], limit =1)

            if partner:
                country = self.env['res.country'].search([('name', '=', str(row[3]))])
                country_state = self.env['res.country.state'].search([('name', '=', str(row[5]))])
                data_vals = {
                    'country_id': country and country.id,
                    'city': str(row[4]),
                    'state_id': country_state and country_state.id,
                    'zip': str(row[5]),
                    'street': str(row[7]),
                    'phone': str(row[8]),
                    'ref': 'Import Data Updated',
                }
                partner.write(data_vals)
                imported_list.append(partner.id)
            else:
                not_imported_list.append(str(row[2]))


        print(len(imported_list))
        print(imported_list)
        print(len(not_imported_list))
        print(not_imported_list)

    def update_contacts(self):
        fp = tempfile.NamedTemporaryFile(suffix=".xlsx")
        fp.write(binascii.a2b_base64(self.file))
        fp.seek(0)

        workbook = xlrd.open_workbook(fp.name)
        sheet = workbook.sheet_by_index(0)

        not_imported_list = []
        imported_list = []
        for row_num in range(0, sheet.nrows):
            row = sheet.row_values(row_num)

            partner = self.env['res.partner'].search([('email', '=', str(row[9]))], limit =1)
            if not partner:
                partner = self.env['res.partner'].search([('name', '=', str(row[2]))], limit =1)
                if not partner and '@' in str(row[8]):
                    partner = self.env['res.partner'].search([('email', '=', str(row[8]))], limit =1)

            if partner:
                country = self.env['res.country'].search([('name', '=', str(row[3]))])
                country_state = self.env['res.country.state'].search([('name', '=', str(row[5]))])
                if not country_state:
                    country_state = self.env['res.country.state'].search([('code', '=', str(row[5]))])

                country_state = country_state.filtered(lambda s: s.country_id == country)
                data_vals = {
                    'state_id': country_state and country_state[0].id,
                    'zip': str(row[6]),
                }
                partner.write(data_vals)
                imported_list.append(partner.id)

                if not country_state:
                    not_imported_list.append(str(row[9]))
            else:
                not_imported_list.append(str(row[9]))

        _logger.info('Data not imported List')
        _logger.info(not_imported_list)
        _logger.info("Not imported list lenght:" + str(len(not_imported_list)))
        _logger.info("Imported list length:" + str(len(imported_list)))

    def update_other_address(self):
        fp = tempfile.NamedTemporaryFile(suffix=".xlsx")
        fp.write(binascii.a2b_base64(self.file))
        fp.seek(0)

        workbook = xlrd.open_workbook(fp.name)
        sheet = workbook.sheet_by_index(0)

        not_imported_list = []
        imported_list = []
        for row_num in range(0, sheet.nrows):
            row = sheet.row_values(row_num)

            partner = self.env['res.partner'].search([('email', '=', str(row[9]))], limit =1)
            if not partner:
                partner = self.env['res.partner'].search([('name', '=', str(row[2]))], limit =1)
                if not partner and '@' in str(row[10]):
                    partner = self.env['res.partner'].search([('email', '=', str(row[10]))], limit =1)
                if not partner and '@' in str(row[11]):
                    partner = self.env['res.partner'].search([('email', '=', str(row[11]))], limit =1)

            if partner and not partner.parent_id and len(partner.child_ids) == 0:
                country = self.env['res.country'].search([('name', '=', str(row[11]))])
                country_state = self.env['res.country.state'].search([('name', '=', str(row[12]))])
                data_vals = {
                    'parent_id': partner.id,
                    'type': 'other',
                    'country_id': country and country.id,
                    'city': str(row[14]),
                    'state_id': country_state and country_state.id,
                    'zip': str(row[13]),
                    'street': str(row[10]),
                    'ref': 'Other Address import',
                }
                if country or country_state or len(str(row[14])) > 0 or len(str(row[13])) > 0 or len(str(row[10])) > 0:
                    sub_partner = self.env['res.partner'].create(data_vals)
                    imported_list.append(sub_partner.id)
                    print("New Address: "+str(sub_partner.id))
            else:
                not_imported_list.append(str(row[2]))


        print(len(imported_list))
        print(imported_list)
        print(len(not_imported_list))
        print(not_imported_list)

    def import_product_volume(self):
        fp = tempfile.NamedTemporaryFile(suffix=".xlsx")
        fp.write(binascii.a2b_base64(self.file))
        fp.seek(0)

        workbook = xlrd.open_workbook(fp.name)
        sheet = workbook.sheet_by_index(0)

        not_imported_list = []
        imported_list = []
        for row_num in range(1, sheet.nrows):
            row = sheet.row_values(row_num)

            product = self.env['product.template'].search([('default_code', '=', str(row[0]))])
            if product:
                imported_list.append(row[12])
                volume = 0
                if len (row[12]) == 12:
                    volume = ( int(row[12][:2]) * int(row[12][5:7]) * int(row[12][10:12]) ) * 0.00328084
                    product.to_be = True
                elif len (row[12]) == 9:
                    volume = ( int(row[12][0]) * int(row[12][4]) * int(row[12][8]) ) * 0.00328084
                    product.to_be = True

                if volume > 0 :
                    product.volume = volume
            else:
                not_imported_list.append(row[12])


        print('Data not imported')
        print(len(not_imported_list))
        print(len(imported_list))
