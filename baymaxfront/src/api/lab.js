import request from '@/utils/request'

export function getList (params) {
  return request({
    url: '/api/lab/getall',
    method: 'get',
    params
  })
}
