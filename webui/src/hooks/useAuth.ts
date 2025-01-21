import type { User } from '#/auth';
import type { ApiError } from '#/api';
import { router } from '@/router';

export const useAuth = createSharedComposable(() => {
  const message = useMessage();
  const { t } = useMyI18n();

  const isLoggedIn = useLocalStorage('isLoggedIn', false);

  watch(isLoggedIn, (v) => {
    if (v) {
      router.replace({ name: 'Index' });
    } else {
      router.replace({ name: 'Login' });
    }
  });

  const user = reactive<User>({
    username: '',
    password: '',
  });

  function clearUser() {
    user.username = '';
    user.password = '';
  }

  function formVerify() {
    if (user.username === '') {
      message.warning(t('notify.please_enter', [t('topbar.profile.username')]));
      return false;
    } else if (user.password === '') {
      message.warning(t('notify.please_enter', [t('topbar.profile.password')]));
      return false;
    } else if (user.password.length < 8) {
      message.error(t('notify.password_length_error'));
      return false;
    }

    return true;
  }

  function login() {
    if (!formVerify()) return;

    apiAuth
      .login(user.username, user.password)
      .then(() => {
        isLoggedIn.value = true;
        clearUser();
        message.success(t('notify.login_success'));
      })
      .catch((err: ApiError) => {
        if (err.status === 404) {
          message.error(t('notify.please_update'));
        }
      });
  }

  const { execute: logout } = useApi(apiAuth.logout, {
    showMessage: true,
    onSuccess() {
      clearUser();
      isLoggedIn.value = false;
    },
  });

  const { execute: refresh } = useApi(apiAuth.refresh, {
    showMessage: false,
    onSuccess() {
      isLoggedIn.value = true;
    },
  });

  function update() {
    if (!formVerify()) return;

    apiAuth.update(user.username, user.password).then((res) => {
      if (res.message.toLocaleLowerCase() === 'update success') {
        clearUser();
        message.success(t('notify.update_success'));
      } else {
        user.password = '';
        message.error(t('notify.update_failed'));
      }
    });
  }

  return {
    isLoggedIn,
    user,

    login,
    logout,
    refresh,
    update,
  };
});
