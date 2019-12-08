# coding=utf-8

from django.db import models

from utils.constant import TRUE_INT, FALSE_INT


class ManagerFilterDelete(models.Manager):
    def get_queryset(self):
        return super(ManagerFilterDelete, self).get_queryset().filter(is_del=FALSE_INT)