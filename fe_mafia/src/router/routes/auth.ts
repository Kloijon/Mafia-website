export const authRoutes = [
	//! Раскоментировать meta когда узнаем api
  {
    path: "/games",
    name: "Games",
    component: () => import("@/core/views/GamesPage.vue"),
    // meta: { requiresAuth: true },
  },
  {
    path: "/tournaments/:id",
    name: "TournamentDetail",
    component: () => import("@/core/views/TournamentDetail.vue"),
    // meta: { requiresAuth: true, preload: ["tournamentDetail"] },
  },
  {
    path: "/user/:id",
    name: "UserDetail",
    component: () => import("@/core/views/UserDetail.vue"),
    // meta: { requiresAuth: true, preload: ["userDetail"] },
  },
  {
    path: "/profile",
    name: "Profile",
    component: () => import("@/core/views/Profile.vue"),
    // meta: { requiresAuth: true },
  },
];
