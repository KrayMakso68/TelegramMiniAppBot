import { boot } from 'quasar/wrappers';
import axios, { AxiosInstance } from 'axios';
import { LocalStorage } from 'quasar';
import {useWebApp} from 'vue-tg'

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $axios: AxiosInstance;
    $api: AxiosInstance;
  }
}


// const api = axios.create({ baseURL: 'https://api.example.com' });
//
// export default boot(({ app }) => {
//   // for use inside Vue files (Options API) through this.$axios and this.$api
//
//   app.config.globalProperties.$axios = axios;
//   // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
//   //       so you won't necessarily have to import axios in each vue file
//
//   app.config.globalProperties.$api = api;
//   // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
//   //       so you can easily perform requests against your app's API
// });
//
// export { api };



const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1'
});

// Интерсептор запроса для добавления токена
api.interceptors.request.use((config) => {
  const token = LocalStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

// Интерсептор ответа для обработки ошибок и обновления токенов
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
        // Здесь можно вызвать логаут или перенаправление на страницу входа
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
