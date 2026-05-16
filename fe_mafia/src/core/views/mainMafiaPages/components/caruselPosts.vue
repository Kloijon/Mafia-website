<template>
  <v-container>
    <h1>Шаблон карусели постов</h1>
  </v-container>
</template>

<script setup lang="ts">
import { usePostsStore } from "@/stores/posts";
const postsStore = usePostsStore();
</script>
