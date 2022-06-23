# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Products(models.Model):
    productname = models.CharField(max_length=500, blank=True, null=True)
    productdesc = models.CharField(max_length=500, blank=True, null=True)
    category= models.CharField(max_length=500, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    productage = models.CharField(max_length=45, blank=True, null=True)
    studentid = models.ForeignKey('Students', models.DO_NOTHING, db_column='studentid', blank=True, null=True)
    img = models.FileField(upload_to="student/images", default='' ,blank=False, null=True)

    def _str_(self):
        return self.productname


class Students(models.Model):
    emailid = models.CharField(unique=True, max_length=45, blank=True, null=True)
    password = models.CharField(max_length=225, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    branch = models.CharField(max_length=45, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    year = models.CharField(max_length=45, blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)
    mob = models.CharField(max_length=45, blank=True, null=True)

    def _str_(self):
        return self.productname
