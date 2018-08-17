import request from '@/utils/request'

export function getList (params) {
  return request({
    url: '/node/list/',
    method: 'get',
    params
  })
}
