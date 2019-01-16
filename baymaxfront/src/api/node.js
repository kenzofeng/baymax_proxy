import request from '@/utils/request'

export function nodeList(params) {
    return request({
        url: '/api/node/list',
        method: 'get',
        params
    })
}