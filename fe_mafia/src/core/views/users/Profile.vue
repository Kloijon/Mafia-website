<template>
  <v-container>
    <h1>Мой профиль</h1>
    <p>Здесь будет информация о текущем пользователе.</p>
  </v-container>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';
const authStore = useAuthStore();
// Можно отображать данные authStore.user
</script>