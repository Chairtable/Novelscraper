# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Novelchapters(models.Model):
    chapter_id = models.AutoField(db_column='Chapter_ID', primary_key=True)  # Field name made lowercase.
    novel_id = models.ForeignKey('Novelslist', models.DO_NOTHING, db_column='Novel_ID')  # Field name made lowercase.
    chapter_num = models.IntegerField(db_column='Chapter_Num')  # Field name made lowercase.
    chapter_text = models.TextField(db_column='Chapter_Text', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'novelchapters'


class Novelslist(models.Model):
    novel_name = models.CharField(db_column='Novel_Name', max_length=200)  # Field name made lowercase.
    novel_id = models.AutoField(db_column='Novel_ID', primary_key=True)  # Field name made lowercase.
    novel_url = models.CharField(db_column='Novel_URL', max_length=200)  # Field name made lowercase.
    novel_numchapters = models.IntegerField(db_column='Novel_Numchapters', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'novelslist'
