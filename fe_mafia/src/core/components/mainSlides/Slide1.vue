<template>
  <div class="slide_element text-center">
    <div class="title">
      <p>Спортивная мафия</p>
      <p style="color: #951228">РХТУ</p>
    </div>
    <div class="logo">
      <img src="@/assets/logo/logo_white.svg" alt="logo" />
    </div>
    <div class="under-logo__text">
      <p>
        Спортивная мафия интеллектуальный спорт с чёткими правилами. Здесь нет
        места случайностям: победа зависит от логики и умения работать с людьми.
      </p>
    </div>
    <div class="arrow">
      <img src="@/assets/icons/arrowdown.svg" alt="arrow" />
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.slide_element {
  display: flex;
  min-height: 90vh;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
}

.title {
  font-size: clamp(32px, 8vw, 96px);

  p {
    margin: 0;
    line-height: 1.2;
  }
}

.logo {
  img {
    width: clamp(120px, 20vw, 400px);
    height: auto;
  }
}

.under-logo__text {
  width: min(70vw, 800px);
  max-width: 90%;
  margin: 0 auto;
  text-align: center;

  p {
    margin: 0;
    font-size: clamp(12px, 2vw, 20px);
    color: #e0e0e0;
    opacity: 0.5;
    line-height: 1.3;
  }
}

.arrow {
  img {
    width: clamp(24px, 5vw, 80px);
    height: auto;
  }
}

@media (min-height: 1000px) {
  .title {
    padding-top: 15vh;
  }
}

@media (min-height: 800px) and (max-height: 999px) {
  .title {
    padding-top: 10vh;
  }
}

@media (min-height: 600px) and (max-height: 799px) {
  .title {
    padding-top: 0vh;
  }
}
</style>
