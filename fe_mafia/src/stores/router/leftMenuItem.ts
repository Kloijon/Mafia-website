import { defineStore } from "pinia";

export const leftMenuItem = defineStore("leftMenuItem", {
  state: () => ({
    items: [
      {
        id: 1,
        icon: "src/assets/icons-left-menu/tournament.svg",
        name: "Турниры",
        path: "/tournaments"
      },
      {
        id: 2,
        icon: "src/assets/icons-left-menu/games.svg",
        name: "Игры",
        path: "/games"
      },
      {
        id: 3,
        icon: "src/assets/icons-left-menu/rating.svg",
        name: "Рейтинг",
        path: "/rating"
      },
      {
        id: 4,
        icon: "src/assets/icons-left-menu/info.svg",
        name: "О нас",
        path: "/about"
      },
    ]
  }),
});
