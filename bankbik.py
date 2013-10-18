#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Парсер справочника БАНКОВ с сайта ГАРАНТа
Автор: Битюков Павел (pavleg.bityukov@gmail.com)
'''

import logging
import urllib2
import lxml.html

logging.basicConfig()
logger = logging.getLogger(__name__)


################################################################################
class BankGarantParser(object):
	''' Парсер банка (элемента справочника) с сайта http://www.garant.ru '''

	version = '0.1a'

	def __init__(self, item):
		self._item = item


	@property
	def is_active(self):
		if self._item.attrib.get('class') == 'TxtOutOfDate':
			return False
		return True

	@property
	def orgtype(self):
		''' тип участника расчетов '''
		try:
			return self._item.xpath('td[9]/text()')[0]
		except IndexError:
			raise Exception(u'Некорретный элемент справочника: отсутвует тип участника расчетов')


	@property
	def bik(self):
		''' БИК '''
		try:
			return self._item.xpath('td[1]/text()')[0]
		except IndexError:
			raise Exception(u'Некорретный элемент справочника: отсутвует БИК')


	@property
	def corr(self):
		''' Корсчет '''
		try:
			return self._item.xpath('td[2]/text()')[0]
		except IndexError:
			raise Exception(u'Некорретный элемент справочника: отсутвует Корсчет')


	@property
	def name(self):
		''' платежное наименование участника расчетов '''
		try:
			return self._item.xpath('td[3]/text()')[0]
		except IndexError:
			raise Exception(u'Некорретный элемент справочника: отсутвует платежное наименование участника расчетов')


	@property
	def zip(self):
		''' индекс участника расчетов '''
		try:
			return self._item.xpath('td[14]/text()')[0]
		except IndexError:
			raise Exception(u'Некорретный элемент справочника: отсутвует индекс участника расчетов')


	@property
	def city(self):
		''' наименование населенного пункта участника расчетов '''
		try:
			return self._item.xpath('td[15]/text()')[0]
		except IndexError:
			raise Exception(u'Некорретный элемент справочника: отсутвует наименование населенного пункта участника расчетов')


	@property
	def addr(self):
		''' адрес в насленном пункте участника расчетов '''
		try:
			return self._item.xpath('td[16]/text()')[0]
		except IndexError:
			raise Exception(u'Некорретный элемент справочника: отсутвует адрес в насленном пункте участника расчетов')



################################################################################


################################################################################
class BikGarant(object):
	''' Парсер справочника БИК с сайта http://www.garant.ru '''
	version = '0.1a'

	def __init__(self, include=[], exclude=[u'КУПР', u'РКЦ', u'ГРКЦ']):
		self.name = 'BikBot'
		self.baseurl = 'http://www.garant.ru/doc/busref/spr_bik'
		self.content_set = {}
		self.bank_set = {}
		self.include = include
		self.exclude = exclude



	def grab_state(self, name):
		''' Скачивание станицы справочника области '''
		url = '%s/%s' % (self.baseurl, name)
		request = urllib2.Request(url)
		response = urllib2.urlopen(request)
		self.content_set[name] = response.read()


	def parse_state(self, name):
		''' Парсинг справочника области '''
		if name not in self.content_set:
			self.grab_state(name)

		if name not in self.bank_set:
			self.bank_set[name] = []

		document = lxml.html.document_fromstring(self.content_set[name])
		item_set = document.xpath('/html/body/table/tr[2]/td[2]/table/tr[2]/td/div/table/tr')
		for item in item_set:
			try:
				bank = BankGarantParser(item)
				if self.exclude and bank.orgtype in self.exclude:
					continue
				self.bank_set[name].append(bank)
			except Exception, E:
				logger.error(E.message)


################################################################################
