import { defineStore } from 'pinia';

export interface Game {
  id: number;
  name: string;
  // другие поля по необходимости
}

export const useGamesStore = defineStore('games', {
  state: () => ({
    games: [] as Game[],
    loading: false,
  }),
  actions: {
    async fetchGames() {
      this.loading = true;
      // Заглушка
      // const data = await get<Game[]>(API_URLS.games.list);
      // this.games = data;
      await new Promise(resolve => setTimeout(resolve, 500));
      this.games = [
        { id: 1, name: 'Пример игры 1' },
        { id: 2, name: 'Пример игры 2' },
      ];
      this.loading = false;
    },
  },
});