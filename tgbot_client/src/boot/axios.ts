import { boot } from 'quasar/wrappers';
import axios, { AxiosInstance } from 'axios';

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $axios: AxiosInstance;
    $api: AxiosInstance;
  }
}

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)
const api = axios.create({ baseURL: 'https://api.example.com' });

export default boot(({ app }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api

  app.config.globalProperties.$axios = axios;
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$api = api;
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
});

export { api };

// import { boot } from 'quasar/wrappers';
// import axios from 'axios';
// import { LocalStorage } from 'quasar';
//
// const api = axios.create({
//   baseURL: 'http://localhost:5000/api/v1/', // Замените на ваш базовый URL
// });
//
// // Интерсептор запроса для добавления токена
// api.interceptors.request.use((config) => {
//   const token = LocalStorage.getItem('token'); // Получаем токен из LocalStorage
//   if (token) {
//     config.headers.Authorization = `Bearer ${token}`; // Добавляем заголовок Authorization
//   }
//   return config;
// }, (error) => {
//   return Promise.reject(error);
// });
//
// // Интерсептор ответа для обработки ошибок и обновления токенов
// api.interceptors.response.use(
//   (response) => response,
//   async (error) => {
//     const originalRequest = error.config;
//
//     if (error.response?.status === 401 && !originalRequest._retry) {
//       originalRequest._retry = true;
//       const refreshToken = LocalStorage.getItem('refreshToken'); // Получаем refresh токен
//
//       try {
//         const response = await api.post('/auth/refreshToken', { refreshToken });
//         const { accessToken } = response.data;
//
//         LocalStorage.set('token', accessToken); // Сохраняем новый access токен
//         api.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`; // Обновляем заголовок
//
//         return api(originalRequest); // Повторяем оригинальный запрос
//       } catch (err) {
//         console.error('Ошибка обновления токена:', err);
//         // Здесь можно вызвать логаут или перенаправление на страницу входа
//       }
//     }
//
//     return Promise.reject(error);
//   }
// );
//
// export default boot(({ app }) => {
//   app.config.globalProperties.$axios = axios;
//   app.config.globalProperties.$api = api; // Используйте $api для запросов к вашему API
// });
//
// export { axios, api };
