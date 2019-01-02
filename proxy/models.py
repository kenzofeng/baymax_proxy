from django.db import models

Run_Status = (
    ('Running', 'Running'),
    ('Done', 'Done'),
    ('Error', 'Error'),
    ('Waiting', 'Waiting'),
    ('FAIL', 'FAIL'),
    ('PASS', 'PASS'),
)

Source_type = (
    ('SVN', 'SVN'),
    ('Git', 'Git'),
)


class Project(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    email = models.CharField(max_length=250)
    version = models.CharField(max_length=500, blank=True, default="")

    def __unicode__(self):
        return self.name


class Node(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    projects = models.ManyToManyField(Project, blank=True)
    aws_instance_id = models.CharField(max_length=100, blank=True, default="")
    host = models.CharField(max_length=50, blank=True, default="")
    public_ip = models.CharField(max_length=50, blank=True, default="")
    private_ip = models.CharField(max_length=50, blank=True, default="")
    port = models.CharField(max_length=50, default="51234")
    status = models.CharField(max_length=20, choices=Run_Status)


class Test_Map(models.Model):
    project = models.CharField(max_length=50)
    test = models.CharField(max_length=50)
    source_type = models.CharField(max_length=20, choices=Source_type)
    source_url = models.CharField(max_length=250)
    source_branch = models.CharField(max_length=250, default='master')
    robot_parameter = models.CharField(max_length=250, blank=True, null=True, default='')
    app = models.CharField(max_length=250)
    use = models.BooleanField(default=True)

    def touse(self):
        if self.use:
            return 'yes'
        else:
            return 'no'

    def __unicode__(self):
        return self.test


class Job(models.Model):
    project = models.CharField(max_length=50)
    project_version = models.TextField(default="")
    servers = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=Run_Status)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    job_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.project


class Job_Log(models.Model):
    job = models.OneToOneField(Job, on_delete=models.CASCADE)
    path = models.CharField(max_length=250)
    text = models.TextField(blank=True, null=True)


class Job_Test(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    testurl = models.CharField(max_length=250)
    robot_parameter = models.CharField(max_length=250, blank=True, null=True, default='')
    app = models.CharField(max_length=250, blank=True, null=True, default='')
    name = models.CharField(max_length=50, blank=True, null=True, default='')
    pid = models.CharField(max_length=50, blank=True, null=True, default='')
    status = models.CharField(max_length=20, choices=Run_Status)
    revision_number = models.CharField(max_length=50, blank=True, null=True, )
    count = models.CharField(max_length=50, blank=True, default="")


class Job_Test_Result(models.Model):
    job_test = models.OneToOneField(Job_Test, on_delete=models.CASCADE)
    log = models.TextField(blank=True, null=True)
    log_path = models.CharField(max_length=250)
    report = models.CharField(max_length=250, blank=True, null=True)


class Job_Test_Distributed_Result(models.Model):
    job_test = models.ForeignKey(Job_Test, on_delete=models.CASCADE)
    host = models.CharField(max_length=250)
    script = models.CharField(max_length=250)
    log = models.TextField(blank=True, null=True)
    log_path = models.CharField(max_length=250)
    report = models.CharField(max_length=250, blank=True, null=True)
