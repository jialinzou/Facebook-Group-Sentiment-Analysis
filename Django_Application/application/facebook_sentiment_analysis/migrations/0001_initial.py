# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='YelpReview',
            fields=[
                ('id', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('review_text', models.TextField()),
                ('star', models.FloatField()),
            ],
        ),
    ]
