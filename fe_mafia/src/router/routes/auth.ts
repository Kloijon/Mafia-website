export const authRoutes = [
	//! Раскоментировать meta когда узнаем api
  {
    path: "/games",
    name: "Games",
    component: () => import("@/core/views/gamesTournaments/GamesPage.vue"),
    // meta: { requiresAuth: true },
  },
  {
    path: "/tournaments/:id",
    name: "TournamentDetail",
    component: () => import("@/core/views/gamesTournaments/TournamentDetail.vue"),
    // meta: { requiresAuth: true, preload: ["tournamentDetail"] },
  },
  {
    path: "/user/:id",
    name: "UserDetail",
    component: () => import("@/core/views/users/UserDetail.vue"),
    // meta: { requiresAuth: true, preload: ["userDetail"] },
  },
  {
    path: "/profile",
    name: "Profile",
    component: () => import("@/core/views/users/Profile.vue"),
    // meta: { requiresAuth: true },
  },
];
