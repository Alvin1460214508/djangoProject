from django.db import models
# from neomodel import (StructuredNode, StringProperty, IntegerProperty, UniqueIdProperty, RelationshipTo,
#                       DateTimeFormatProperty, ArrayProperty, StructuredRel)

from neomodel import *

'''操作数据库'''

# Create your models here.
# app要先注册


"""MySQL"""


class Book(models.Model):
    book_name = models.CharField(max_length=64)
    create_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.book_name


class UserInfo(models.Model):
    name = models.CharField(max_length=32)  # 字符串类型
    password = models.CharField(max_length=64)  # 字符串类型
    age = models.IntegerField(default=2)  # int类型
    # data = models.IntegerField(null=True,blank=True)  # 默认为空也可以
    event_date = models.DateTimeField(null=True, blank=True)
    """相当于:
    create table app001_userinfo(
        id bigint auto_increment primary key,
        name varchar(32),
        password varchar(64),
        age int
    )"""


class Department(models.Model):
    title = models.CharField(max_length=16)


"""Neo4j"""


class Country(StructuredNode):
    @classmethod
    def category(cls):
        pass

    code = StringProperty(unique_index=True, required=True)
    countryName = StringProperty(required=True)


class Person(StructuredNode):
    @classmethod
    def category(cls):
        pass

    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True)
    age = IntegerProperty(index=True, default=0)
    people = StringProperty()
    # 性别
    SEXES = {'M': 'Man', 'W': 'Woman', 'O': 'Other'}
    sex = StringProperty(required=True, choices=SEXES)
    # 喜好
    likes = ArrayProperty(StringProperty())
    dislikes = ArrayProperty(StringProperty())
    # 关系
    # traverse outgoing IS_FROM relations, inflate to Country objects
    country = RelationshipTo(Country, 'IS_FROM')


class ActedInRel(StructuredRel):
    actorType = {'0': '主角', '1': "配角"}
    isLeader = StringProperty(required=True, choices=actorType)


class Movie(StructuredNode):
    @classmethod
    def category(cls):
        pass

    mid = UniqueIdProperty()
    title = StringProperty(required=True)
    releasedTime = DateTimeFormatProperty(format="%Y-%m")
    tags = ArrayProperty(StringProperty(), required=True)
    score = IntegerProperty()

    # 关系
    actors = RelationshipFrom(Person, 'Acted_In', model=ActedInRel)
    director = RelationshipFrom(Person, 'Directed_In')
    writer = RelationshipFrom(Person, 'WROTE')
    producer = RelationshipFrom(Person, 'Produce')

    country = RelationshipTo(Country, 'IS_FROM')
