# Copyright (C) 2019 by eHealth Africa : http://www.eHealthAfrica.org
#
# See the NOTICE file distributed with this work for additional information
# regarding copyright ownership.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import json

from django.utils.translation import ugettext as _
from drf_dynamic_fields import DynamicFieldsMixin
from rest_framework import serializers

from django_eha_sdk.multitenancy.serializers import MtModelSerializer, MtPrimaryKeyRelatedField
from django_eha_sdk.multitenancy.utils import add_user_to_realm

from .models import Project, Schema, MobileUser


class SchemaSerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    avro_file = serializers.FileField(
        write_only=True,
        allow_null=True,
        default=None,
        label=_('AVRO Schema file'),
        help_text=_('Upload an AVRO Schema file'),
    )

    project = MtPrimaryKeyRelatedField(
        queryset=Project.objects.all(),
    )

    def validate(self, value):
        if value['avro_file']:
            try:
                # extract data from file and put it on `avro_schema`
                value['avro_schema'] = json.loads(value['avro_file'].read())
            except Exception as e:
                raise serializers.ValidationError({'avro_file': str(e)})
        value.pop('avro_file')

        return super(SchemaSerializer, self).validate(value)

    class Meta:
        model = Schema
        fields = '__all__'


class ProjectSerializer(DynamicFieldsMixin, MtModelSerializer):

    # this will return all linked schemas in one request call
    schemas = SchemaSerializer(read_only=True, many=True)

    class Meta:
        model = Project
        fields = '__all__'


class MobileUserSerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    def create(self, validated_data):
        instance = super(MobileUserSerializer, self).create(validated_data)
        self.post_save(instance)
        return instance

    def update(self, instance, validated_data):
        email = validated_data.get('email', instance.email)
        # changing the email could head to weird permission issues with linked devices
        # in order to skip those errors we do not allow to change it
        # delete and create a new one will be the solution
        if email != instance.email:
            raise serializers.ValidationError({'email': _('email field cannot be changed.')})

        instance = super(MobileUserSerializer, self).update(instance, validated_data)
        self.post_save(instance)
        return instance

    def post_save(self, instance):
        add_user_to_realm(self.context['request'], instance)

    class Meta:
        model = MobileUser
        fields = ('id', 'email',)
