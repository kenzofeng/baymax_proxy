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
