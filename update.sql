alter table proxy_project add column version varchar;
alter table proxy_job  add column project_version text;
alter table proxy_job_test  add column count varchar;
alter table proxy_job_test add column start_time datetime;
alter table proxy_job_test add column end_time datetime;
alter table proxy_job_test add column source_url varchar;
alter table proxy_job_test add column source_type varchar;
alter table proxy_job_test add column source_branch varchar;
