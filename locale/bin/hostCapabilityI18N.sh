#!/usr/bin/env bash
#
#    Copyright (C) 2013 Intel Corporation.  All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

# Program:
#			This program is used for the i18n of hostcapability.
LINK_DIR='/usr/lib/python2.7/dist-packages/horizon/locale/zh_CN/LC_MESSAGES'
HORIZON_I18N_DIR='/usr/share/pyshared/horizon/locale/zh_CN/LC_MESSAGES'
CURRENTBINPATH=$PWD
LOCALE_DIR=${CURRENTBINPATH%/*}

# Merge the i18n file of hostcapability with the prime one
cat $LOCALE_DIR/zh_CN/LC_MESSAGES/django.po>>$HORIZON_I18N_DIR/django.po

# Translate message
msgfmt --statistics --verbose -o $HORIZON_I18N_DIR/django.mo $HORIZON_I18N_DIR/django.po

rm -rf $LINK_DIR/django.mo

ln -s  $HORIZON_I18N_DIR/django.mo $LINK_DIR/django.mo

# Restart the apache2 service
service apache2 restart