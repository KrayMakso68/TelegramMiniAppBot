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
        component: () => import('pages/PaymentHistoryPage.vue')
      },
      {
        path: 'payment-new',
        component: () => import('pages/PaymentNewPage.vue')
      },
      {
        path: 'connect-info',
        component: () => import('pages/ConnectInfoPage.vue'),
        props: (route) => ({
          id: Number(route.query.id) ?? 0,
          name: route.query.name as string ?? "",
          email: route.query.email as string ?? "",
          serverId: Number(route.query.serverId) ?? 0,
          url: route.query.url as string ?? "",
          unlimited: route.query.unlimited === 'true' ?? false,
          isActive: route.query.isActive === 'true' ?? false
        }),
      },
      {
        path: 'subscription-new',
        component: () => import('pages/SubscriptionNewPage.vue')
      },
      {
        path: 'subscription-extension',
        component: () => import('pages/ExtensionSubscriptionPage.vue'),
        props: (route) => ({
          id: Number(route.query.id) ?? 0,
          name: route.query.name as string ?? "",
          serverId: Number(route.query.serverId) ?? 0
        }),
      }
    ],
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/errors/ErrorNotFound.vue'),
  },
];

export default routes;
