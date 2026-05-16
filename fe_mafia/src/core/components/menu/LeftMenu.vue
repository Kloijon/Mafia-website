<template>
  <div class="left-menu">
    <div class="left-menu__container">
      <div
        class="left-menu__item"
        v-for="item in left_menu.items"
        :key="item.id"
        :class="{ active: isActiveRoute(item.path) }"
        @click="navigateTo(item.path)"
      >
        <img
          class="left-menu__item-img"
          :src="iconMap[item.id]"
          :alt="item.name"
        />
        <div class="left-menu__item-name">
          {{ item.name }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter, useRoute } from "vue-router";
import { leftMenuItem } from "@/stores/router/leftMenuItem";
import tournamentIcon from "@/assets/icons-left-menu/tournament.svg";
import gamesIcon from "@/assets/icons-left-menu/games.svg";
import ratingIcon from "@/assets/icons-left-menu/rating.svg";
import infoIcon from "@/assets/icons-left-menu/info.svg";

const left_menu = leftMenuItem();
const router = useRouter();
const route = useRoute();

const iconMap: Record<number, string> = {
  1: tournamentIcon,
  2: gamesIcon,
  3: ratingIcon,
  4: infoIcon,
};

const isActiveRoute = (path: string): boolean => {
  return route.path === path;
};

const navigateTo = (path: string): void => {
  router.push(path);
};
</script>

<style lang="scss" scoped>
.left-menu {
  position: fixed;
  top: 0;
  left: 0;
  width: 280px;
  height: 100%;
  background-color: #2c2c2c;
  color: #e0e0e0;
  padding: 20px 0;
  z-index: 1000;
  overflow-y: auto;
}

.left-menu__container {
  display: flex;
  flex-direction: column;
  padding: 100px 0;
}

.left-menu__item {
  display: flex;
  flex-direction: row;
  align-items: center;
  width: 100%;
  padding: 12px 20px;
  gap: 14px;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }

  &.active {
    background-color: #6d1f2cc4;
    .left-menu__item-name {
      color: #951228;
      font-weight: 500;
    }

    .left-menu__item-img {
      opacity: 0.8;
    }
  }
}

.left-menu__item-img {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
  transition: all 0.2s ease;
}

.left-menu__item-name {
  font-size: 20px;
  font-weight: 400;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: all 0.2s ease;
}
</style>
