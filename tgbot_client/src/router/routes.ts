import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        component: () => import('pages/IndexPage.vue')
      },
      {
        path: 'not-from-telegram',
        component: () => import('pages/errors/NotFromTelegram.vue')
      },
      {
        path: 'test-colors',
        component: () => import('pages/TelegramColors.vue')
      },
      {
        path: 'payment-history',
        component: () => import('pages/PaymentHistory.vue')
      },
      {
        path: 'connect-info',
        component: () => import('pages/ConnectInfoPage.vue'),
        props: (route) => ({
          connectUrl: route.query.connectUrl as string,
          uuid: route.query.uuid as string,
          email: route.query.email as string,
          inboundName: route.query.inboundName as string
        }),
        meta: { transition: 'slide-right' },
      },
    ],
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/errors/ErrorNotFound.vue'),
  },
];

export default routes;
