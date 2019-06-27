import axios from 'axios'

var http = axios.create()
if (localStorage.getItem('jwt_token') != null)
    http.defaults.headers.common['Authorization'] = 'JWT ' + localStorage.getItem('jwt_token')
else
    http.defaults.headers.common['Authorization'] = ''
http.defaults.headers.common['Content-Type'] = 'application/json'

const baseUrl = 'http://127.0.0.1:8000/'

const getToken =      baseUrl + 'api/v1/auth/obtain_token/'
const updateToken =   baseUrl + 'api/v1/auth/refresh_token/'
const userInfo =      baseUrl + 'api/v1/user/'
const userRegister =  baseUrl + 'api/v1/user/register/'
const userPassword =  baseUrl + 'api/v1/user/password/'
const userAvatar =    baseUrl + 'api/v1/user/avatar/'
const userRestore =   baseUrl + 'api/v1/user/restore/'

const blogCategory =  baseUrl + 'api/v1/blog/category/'
const blogTag =       baseUrl + 'api/v1/blog/tag/'

const mediaFolder =   baseUrl + 'api/v1/media/folder/'

export default {
    http,

    getToken,
    updateToken,
    userInfo,
    userRegister,
    userPassword,
    userAvatar,
    userRestore,

    blogCategory,
    blogTag,

    mediaFolder,

    baseUrl
}
