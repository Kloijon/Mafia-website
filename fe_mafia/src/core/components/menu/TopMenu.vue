<template>
  <div class="top-menu__container">
    <div class="top-menu__left">
      <button
        class="burger-button"
        @click="toggleMenu"
        :class="{ active: isShowLeftMenu }"
        aria-label="Меню"
      >
        <span></span>
        <span></span>
        <span></span>
      </button>

      <div class="top-menu__logo">
        <img
          src="@/assets/logo/logo.svg"
          alt="logo"
          @click="() => router.push('/')"
        />
      </div>
    </div>

		<!--TODO По кнопке сделать всплывающие меню с формой заполнения-->
    <div class="top-menu__right">
      <!--TODO Сделать связь с тем есть ли аунтификация у пользователя-->
			<div class="top-menu__login">
				<p>Войти</p>
				<img src="@/assets/icons/log_in.svg" alt="login">
			</div>
      <!-- <div class="top-menu__avatar">
        <div class="avatar">LogoAvatar</div>
      </div> -->
    </div>

    <Transition name="slide">
      <LeftMenu v-if="isShowLeftMenu" @close="closeMenu" />
    </Transition>

    <Transition name="fade">
      <div v-if="isShowLeftMenu" class="overlay" @click="closeMenu" />
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import LeftMenu from "./LeftMenu.vue";
import { useRouter } from "vue-router";

const router = useRouter();

const isShowLeftMenu = ref<boolean>(false);

const toggleMenu = (): void => {
  isShowLeftMenu.value = !isShowLeftMenu.value;
};

const closeMenu = (): void => {
  isShowLeftMenu.value = false;
};
</script>

<style lang="scss" scoped>
.top-menu__container {
  height: 10vh;
  width: 100%;
  background-color: #343434;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.top-menu__left {
  display: flex;
  align-items: center;
  gap: 20px;
	margin-left: 20px;
}

.burger-button {
  position: relative;
  z-index: 1001;
  width: 30px;
  height: 24px;
  background: transparent;
  border: none;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 0;

  span {
    display: block;
    width: 100%;
    height: 3px;
    background-color: #e0e0e0;
    border-radius: 2px;
    transition: all 0.3s ease;
  }

  &.active {
    span:first-child {
      transform: translate(70px, 21px);
    }
    span:nth-child(2) {
      transform: translate(35px, 10.5px);
    }
    span:last-child {
      transform: translate(0);
    }
  }

  &:hover {
    opacity: 0.8;
  }
}

.top-menu__logo {
  cursor: pointer;
  img {
    height: 75px;
    width: auto;
    object-fit: contain;
  }
}

.top-menu__right {
  display: flex;
  align-items: center;
  padding: 0 3em;
}

.top-menu__login {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  padding: 8px 16px;
  border-radius: 8px;
  transition: all 0.2s ease;  
  p {
    color: #e0e0e0;
    font-size: 20px;
    font-weight: 500;
    margin: 0;
  }
  
  img {
    width: 24px;
    height: 24px;
    filter: brightness(0) invert(1);
  }
  
  &:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }
  
  &:active {
    background-color: #9512283c;
  }
}

.top-menu__avatar {
  cursor: pointer;
  transition: opacity 0.2s ease;
  .avatar {
    width: 40px;
    height: 40px;
  }
}

// Анимация для меню
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(-100%);
}

.slide-enter-to,
.slide-leave-from {
  transform: translateX(0);
}

// Анимация для оверлея
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.fade-enter-to,
.fade-leave-from {
  opacity: 1;
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
  cursor: pointer;
}
</style>
