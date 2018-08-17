import request from '@/utils/request'

export function getList (params) {
  return request({
    url: '/project/getall/',
    method: 'get',
    params
  })
}

export function getdetail (params) {
  return request({
    url: '/project/getdetail',
    method: 'get',
    params
  })
}
