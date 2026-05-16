<template>
  <v-container>
    <h1>Профиль пользователя</h1>
    <div v-if="usersStore.selectedUser">
      <p>Имя: {{ usersStore.selectedUser.username }}</p>
      <p>Рейтинг: {{ usersStore.selectedUser.rating }}</p>
    </div>
    <div v-else>Загрузка...</div>
  </v-container>
</template>

<script setup lang="ts">
import { useUsersStore } from '@/stores/users';
import { useRoute } from 'vue-router';

const route = useRoute();
const usersStore = useUsersStore();

const userId = Number(route.params.id);
if (userId && !usersStore.selectedUser) {
  usersStore.fetchUserById(userId);
}
</script>