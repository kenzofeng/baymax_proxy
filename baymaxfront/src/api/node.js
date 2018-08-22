import request from '@/utils/request'

export function getList (params) {
  return request({
    url: '/api/node/list/',
    method: 'get',
    params
  })
}
