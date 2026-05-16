import { defineStore } from 'pinia';
import { post, get } from '@/helper/api';
import { API_URLS } from '@/helper/apiUrls';

export interface User {
  id: number;
  username: string;
  email: string;
  role: 'user' | 'admin';
  avatar?: string;
  tg_nickname?: string;
  rating?: number;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    token: localStorage.getItem('token') || null,
    isAuthenticated: !!localStorage.getItem('token'),
  }),
  getters: {
    isAdmin: (state) => state.user?.role === 'admin',
    username: (state) => state.user?.username || '',
  },
  actions: {
    async login(email: string, password: string) {
      const response = await post<{ user: User; token: string }>(
        API_URLS.auth.login,
        { email, password }
      );
      this.user = response.user;
      this.token = response.token;
      this.isAuthenticated = true;
      localStorage.setItem('token', response.token);
    },
    async logout() {
      try {
        await post(API_URLS.auth.logout, {});
      } catch (e) {
        console.warn('Logout request failed', e);
      }
      this.user = null;
      this.token = null;
      this.isAuthenticated = false;
      localStorage.removeItem('token');
    },
    async fetchCurrentUser() {
      if (!this.token) return;
      try {
        const user = await get<User>(API_URLS.auth.me);
        this.user = user;
      } catch (error) {
        this.logout();
      }
    },
  },
});