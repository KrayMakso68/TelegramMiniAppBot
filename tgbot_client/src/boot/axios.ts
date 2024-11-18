import { boot } from 'quasar/wrappers';
import axios, { AxiosInstance } from 'axios';

import { LocalStorage } from 'quasar';
import { useWebApp } from 'vue-tg'

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $axios: AxiosInstance;
    $api: AxiosInstance;
  }
}

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1'
});

api.interceptors.request.use((config) => {
  const token = LocalStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if ((error.response?.status === 401) && !originalRequest._retry) {
      originalRequest._retry = true;
      const {initData} = useWebApp()

      try {
        const response = await api.post('/auth/login', {queryString: initData});
        const { accessToken } = response.data;

        LocalStorage.set('token', accessToken);
        api.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;

        return api(originalRequest);
      } catch (err) {
        console.error('Ошибка обновления токена:', err);
      }
    }

    return Promise.reject(error);
  }
);

export default boot(({ app }) => {
  app.config.globalProperties.$axios = axios;
  app.config.globalProperties.$api = api;
});

export { axios, api };
