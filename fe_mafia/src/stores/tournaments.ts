import { defineStore } from "pinia";
import { get, post, patch, del } from "@/helper/api";
import { API_URLS } from "@/helper/apiUrls";

export interface Tournament {
  id: number;
  title: string;
  description: string;
  image?: string;
  start_time: string;
  place: string;
}

export const useTournamentsStore = defineStore("tournaments", {
  state: () => ({
    tournaments: [] as Tournament[],
    currentTournament: null as Tournament | null,
    loading: false,
  }),
  actions: {
		// Получение всех турниров
    async fetchTournaments() {
      this.loading = true;
      try {
        const data = await get<Tournament[]>(API_URLS.tournaments.list);
        this.tournaments = data;
      } finally {
        this.loading = false;
      }
    },
		// Получение конкретного турнира
    async fetchTournamentById(id: number) {
      this.loading = true;
      try {
        const data = await get<Tournament>(API_URLS.tournaments.getOne(id));
        this.currentTournament = data;
      } finally {
        this.loading = false;
      }
    },
		// Создание турнира
    async createTournament(data: Omit<Tournament, "id">) {
      const newTournament = await post<Tournament>(
        API_URLS.tournaments.create,
        data,
      );
      this.tournaments.unshift(newTournament);
    },
		// Обновление турнира
    async updateTournament(id: number, data: Partial<Tournament>) {
      const updated = await patch<Tournament>(
        API_URLS.tournaments.update(id),
        data,
      );
      const index = this.tournaments.findIndex((t) => t.id === id);
      if (index !== -1) this.tournaments[index] = updated;
      if (this.currentTournament?.id === id) this.currentTournament = updated;
    },
		// Удлание турнира
    async deleteTournament(id: number) {
      await del(API_URLS.tournaments.delete(id));
      this.tournaments = this.tournaments.filter((t) => t.id !== id);
      if (this.currentTournament?.id === id) this.currentTournament = null;
    },
		// Отправка заявки на турнир
    async applyForTournament(tournamentId: number) {
      return await post(API_URLS.tournaments.apply(tournamentId), {});
    },
  },
});
