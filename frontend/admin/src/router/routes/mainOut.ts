/**
The routing of this file will not show the layout.
It is an independent new page.
the contents of the file still need to log in to access
 */
import type { AppRouteModule } from '/@/router/types';

// test
// http:ip:port/main-out
export const mainOutRoutes: AppRouteModule[] = [
  {
    path: '/search',
    name: 'Search',
    component: () => import('/@/views/guest/search.vue'),
    meta: {
      ignoreAuth: true,
      title: '搜索',
    },
  },
];

export const mainOutRouteNames = mainOutRoutes.map((item) => item.name);
