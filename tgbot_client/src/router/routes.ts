import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') },
      { path: 'not-from-telegram', component: () => import('pages/errors/NotFromTelegram.vue') },
      { path: 'test-colors', component: () => import('pages/TelegramColors.vue') },
    ],
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/errors/ErrorNotFound.vue'),
  },
];

export default routes;
