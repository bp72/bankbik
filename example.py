#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' usage example '''

import bankbik

bik = bankbik.BikGarant()
bik.parse_state('tumen')
bik.parse_state('moscow')

for state, bank_set in bik.bank_set.items():
	for bank in bank_set:
		print state, bank.bik, bank.name.encode('utf-8'), bank.is_active
