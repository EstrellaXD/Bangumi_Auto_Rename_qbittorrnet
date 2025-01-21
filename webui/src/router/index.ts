import { createRouter, createWebHashHistory } from 'vue-router/auto';

const router = createRouter({
  history: createWebHashHistory(),
});

router.beforeEach((to) => {
  const { isLoggedIn } = useAuth();
  const { type, url } = storeToRefs(usePlayerStore());

  if (!isLoggedIn.value && to.path !== '/login') {
    return { name: 'Login' };
  } else if (isLoggedIn.value && to.path === '/login') {
    return { name: 'Index' };
  }

  if (type.value === 'jump' && url.value !== '' && to.path === '/player') {
    open(url.value);
    return false;
  }
});

export { router };
