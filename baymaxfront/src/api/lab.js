import request from '@/utils/request'

export function labList (params) {
  return request({
    url: '/api/lab/getall',
    method: 'get',
    params
  })
}
