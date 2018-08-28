import request from '@/utils/request'

export function getList (params) {
  return request({
    url: '/api/project/getall',
    method: 'get',
    params
  })
}

export function getdetail (params) {
  return request({
    url: '/api/project/getdetail',
    method: 'get',
    params
  })
}

export function saveproject (data) {
  return request({
    url: '/api/project/save',
    method: 'post',
    data: data
  })
}

export function newproject (data) {
  return request({
    url: '/api/project/new',
    method: 'post',
    data: data
  })
}

export function deleteproject (data) {
  return request({
    url: '/api/project/delete',
    method: 'post',
    data: data
  })
}
