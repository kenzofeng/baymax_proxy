import request from '@/utils/request'

export function getall (params) {
  return request({
    url: '/api/job/getall',
    method: 'get',
    params
  })
}

export function startjob (project) {
  return request({
    url: '/api/job/' + project + '/start',
    method: 'get'
  })
}

export function stopjob (project) {
  return request({
    url: '/api/job/' + project + '/stop',
    method: 'get'
  })
}

export function rerunjob (jobpk) {
  return request({
    url: '/api/job/' + jobpk + '/rerun',
    method: 'get'
  })
}

export function savecomment (params) {
  return request({
    url: '/api/job/comments/',
    method: 'post',
    data: params
  })
}
