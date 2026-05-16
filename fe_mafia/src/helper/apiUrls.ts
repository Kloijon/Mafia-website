export const API_URLS = {
  posts: {
    list: "/posts/",

    getOne: (id: number) => `/posts/${id}/`,

    create: "/posts/",

    update: (id: number) => `/posts/${id}/`,

    delete: (id: number) => `/posts/${id}/`,
  },
  tournaments: {
    list: "/tournaments/",
    getOne: (id: number) => `/tournaments/${id}/`,

    create: "/tournaments/",

    update: (id: number) => `/tournaments/${id}/`,

    delete: (id: number) => `/tournaments/${id}/`,

    apply: (id: number) => `/tournaments/${id}/apply`,
  },
	// ! Поменять когда будет полный список url
  auth: {
    login: "/auth/login",

    logout: "/auth/logout",

    me: "/auth/me",

    register: "/auth/register",
  },
  users: {
    list: "/users",
    detail: (id: number) => `/users/${id}`,
  },
} as const;
