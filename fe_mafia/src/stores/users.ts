import { defineStore } from "pinia";
import { get } from "@/helper/api";
import { API_URLS } from "@/helper/apiUrls";
import type { User } from "./auth";

//TODO Сделать геттеры для получение поьзщователй и сеттеры для изменения лоудинга на стороне компонента 
export const useUsersStore = defineStore("users", {
  state: () => ({
    users: [] as User[],
    selectedUser: null as User | null,
    loading: false,
  }),
  actions: {
		// Получение всех пользователей
    async fetchAllUsers() {
      this.loading = true;
      try {
        const data = await get<User[]>(API_URLS.users.list);
        this.users = data;
      } finally {
        this.loading = false;
      }
    },
		// Получение конкретного пользоваетля
    async fetchUserById(id: number) {
      this.loading = true;
      try {
        const user = await get<User>(API_URLS.users.detail(id));
        this.selectedUser = user;
      } finally {
        this.loading = false;
      }
    },
    clearSelectedUser() {
      this.selectedUser = null;
    },
  },
});
