import type { LoginSuccess, Update } from '#/auth';
import type { ApiSuccess } from '#/api';

export const apiAuth = {
  async login(username: string, password: string) {
    const formData = new URLSearchParams({
      username,
      password,
    });

    const { data } = await axios.post<LoginSuccess>(
      'api/v1/auth/login',
      formData,
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      }
    );

    return data;
  },

  async refresh() {
    const { data } = await axios.get<LoginSuccess>('api/v1/auth/refresh_token');
    return data;
  },

  async logout() {
    const { data } = await axios.get<ApiSuccess>('api/v1/auth/logout');
    return data;
  },

  async update(username: string, password: string) {
    const { data } = await axios.post<Update>('api/v1/auth/update', {
      username,
      password,
    });

    return data;
  },
};
