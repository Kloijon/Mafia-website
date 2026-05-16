import MainPage from "@/core/views/mainMafiaPages/MainPage.vue";
import AboutPage from "@/core/views/mainMafiaPages/AboutPage.vue";
import RatingPage from "@/core/views/gamesTournaments/RatingPage.vue";
import TournamentsPage from "@/core/views/gamesTournaments/TournamentsPage.vue";
//! Раскоментировать meta когда узнаем api
export const publicRoutes = [
  {
    path: "/",
    name: "Main",
    component: MainPage,
    // meta: { preload: ["posts"] },
  },
  {
    path: "/about",
    name: "About",
    component: AboutPage,
  },
  {
    path: "/rating",
    name: "Rating",
    component: RatingPage,
    // meta: { preload: ["users"] },
  },
  {
    path: "/tournaments",
    name: "Tournaments",
    component: TournamentsPage,
    // meta: { preload: ["tournaments"] },
  },
];
