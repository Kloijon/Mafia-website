import { defineStore } from "pinia";
import { get, post, patch, del } from "@/helper/api";
import { API_URLS } from "@/helper/apiUrls";

export interface Post {
  id: number;
  title: string;
  content: string;
  image?: string;
  post_type: "announcement" | "news";
  published_at: string;
  created_at: string;
}

export const usePostsStore = defineStore("posts", {
  state: () => ({
    posts: [] as Post[],
    currentPost: null as Post | null,
    loading: false,
  }),
  actions: {
		// Получение списка постов
    async fetchPosts() {
      this.loading = true;
      try {
        const data = await get<Post[]>(API_URLS.posts.list);
        this.posts = data;
      } finally {
        this.loading = false;
      }
    },
		// Получение конкретного поста
    async fetchPostById(id: number) {
      this.loading = true;
      try {
        const data = await get<Post>(API_URLS.posts.getOne(id));
        this.currentPost = data;
      } finally {
        this.loading = false;
      }
    },
		// Создание поста для администратора
    async createPost(data: Omit<Post, "id" | "created_at" | "published_at">) {
      const newPost = await post<Post>(API_URLS.posts.create, data);
      this.posts.unshift(newPost);
    },
		// Обновления поста
    async updatePost(id: number, data: Partial<Post>) {
      const updated = await patch<Post>(API_URLS.posts.update(id), data);
      const index = this.posts.findIndex((p) => p.id === id);
      if (index !== -1) this.posts[index] = updated;
      if (this.currentPost?.id === id) this.currentPost = updated;
    },
		// Удаление поста
    async deletePost(id: number) {
      await del(API_URLS.posts.delete(id));
      this.posts = this.posts.filter((p) => p.id !== id);
      if (this.currentPost?.id === id) this.currentPost = null;
    },
  },
});
