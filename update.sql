alter table proxy_project add column version varchar;
alter table proxy_job  add column project_version text;
alter table proxy_job_test  add column count varchar;