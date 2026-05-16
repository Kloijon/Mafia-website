import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { usePostsStore } from "@/stores/posts";
import { useTournamentsStore } from "@/stores/tournaments";
import { useUsersStore } from "@/stores/users";
import { publicRoutes } from "./routes/public";
import { authRoutes } from "./routes/auth";
// import { adminRoutes } from "./routes/admin";
// ! Пока админа нету продумать как будет реализовываться добавленгие и изменение всего говна
const routes = [
  ...publicRoutes,
  ...authRoutes,
  // ...adminRoutes,
  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: () => import("@/core/views/NotFound.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Глобальная проверка авторизации и роли
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();

  // Если есть токен, но пользователь ещё не загружен – загружаем
  if (authStore.token && !authStore.user) {
    await authStore.fetchCurrentUser();
  }

  // требуется авторизация
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next({ name: "Main" });
  }

  // требуется роль админа
  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    return next({ name: "Main" });
  }

  next();
});

// Хук предзагрузки данных
router.beforeResolve(async (to, from) => {
  const preloadTasks = to.meta.preload as string[] | undefined;
  if (!preloadTasks?.length) return;

  const postsStore = usePostsStore();
  const tournamentsStore = useTournamentsStore();
  const usersStore = useUsersStore();

  const promises: Promise<any>[] = [];

  for (const task of preloadTasks) {
    switch (task) {
      case "posts":
        if (!postsStore.posts.length) promises.push(postsStore.fetchPosts());
        break;
      case "tournaments":
        if (!tournamentsStore.tournaments.length)
          promises.push(tournamentsStore.fetchTournaments());
        break;
      case "tournamentDetail":
        if (to.params.id) {
          const id = Number(to.params.id);
          promises.push(tournamentsStore.fetchTournamentById(id));
        }
        break;
      case "users":
        if (!usersStore.users.length) promises.push(usersStore.fetchAllUsers());
        break;
      case "userDetail":
        if (to.params.id) {
          const id = Number(to.params.id);
          promises.push(usersStore.fetchUserById(id));
        }
        break;
      default:
        break;
    }
  }

  await Promise.all(promises);
});

export default router;
