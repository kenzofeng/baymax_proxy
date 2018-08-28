# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

Run_Status = (
    ('Running', 'Running'),
    ('Done', 'Done'),
    ('Error', 'Error'),
    ('Waiting', 'Waiting'),
    ('FAIL', 'FAIL'),
    ('PASS', 'PASS'),
)


class Svn(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=50)


class Project(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    email = models.CharField(max_length=250)

    def __unicode__(self):
        return self.name


class Node(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    projects = models.ManyToManyField(Project, blank=True)
    aws_instance_id = models.CharField(max_length=100, blank=True, null=True)
    host = models.CharField(max_length=50, blank=True, null=True)
    port = models.CharField(max_length=50, default="51234")
    status = models.CharField(max_length=20, choices=Run_Status)


class Test_Map(models.Model):
    project = models.CharField(max_length=50)
    test = models.CharField(max_length=50)
    testurl = models.CharField(max_length=250)
    robot_parameter = models.CharField(max_length=250, blank=True, null=True, default='')
    app= models.CharField(max_length=250)
    use = models.BooleanField(default=True)

    def touse(self):
        if self.use:
            return 'yes'
        else:
            return 'no'


class Job(models.Model):
    project = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=Run_Status)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    job_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.project


class Job_Log(models.Model):
    job = models.OneToOneField(Job)
    path = models.CharField(max_length=250)
    text = models.TextField(blank=True, null=True)


class Job_Test(models.Model):
    job = models.ForeignKey(Job)
    project_sha = models.CharField(max_length=60)
    project_branch = models.CharField(max_length=60)
    testurl = models.CharField(max_length=250)
    robot_parameter = models.CharField(max_length=250, blank=True, null=True, default='')
    name = models.CharField(max_length=50, blank=True, null=True, default='')
    pid = models.CharField(max_length=50, blank=True, null=True, default='')
    status = models.CharField(max_length=20, choices=Run_Status)
    revision_number = models.CharField(max_length=50, blank=True, null=True, )


class Job_Test_Result(models.Model):
    job_test = models.OneToOneField(Job_Test)
    log = models.TextField(blank=True, null=True)
    log_path = models.CharField(max_length=250)
    report = models.CharField(max_length=250, blank=True, null=True)


class Job_Test_Distributed_Result(models.Model):
    job_test = models.ForeignKey(Job_Test)
    host = models.CharField(max_length=250)
    script = models.CharField(max_length=250)
    log = models.TextField(blank=True, null=True)
    log_path = models.CharField(max_length=250)
    report = models.CharField(max_length=250, blank=True, null=True)
