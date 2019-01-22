import request from '@/utils/request'

export function getall(params) {
    return request({
        url: '/api/job/getall',
        method: 'get',
        params
    })
}

export function startjob(project) {
    return request({
        url: '/api/job/' + project + '/start',
        method: 'get'
    })
}

export function stopjob(project) {
    return request({
        url: '/api/job/' + project + '/stop',
        method: 'get'
    })
}
export function rmjob(jobpk) {
    return request({
        url: '/api/job/' + jobpk + '/remove',
        method: 'post'
    })
}

export function rerunjob(jobpk, data) {
    return request({
        url: '/api/job/' + jobpk + '/rerun',
        method: 'post',
        data
    })
}

export function savecomment(params) {
    return request({
        url: '/api/job/comments/',
        method: 'post',
        data: params
    })
}