<template>
  <div class="slide_element">
    <div class="vertical_text">
      <span>Г</span>
      <span>о</span>
      <span>р</span>
      <span>о</span>
      <span>д</span>
      <span>&nbsp</span>
      <span>З</span>
      <span>а</span>
      <span>с</span>
      <span>ы</span>
      <span>п</span>
      <span>а</span>
      <span>е</span>
      <span>т</span>
    </div>

    <div class="main_title">
      <h1>Триада <span class="highlight">Менделеева</span></h1>
      <p class="subtext">
        Cтуденческий клуб спортивной мафии<br />
        Российского химико-технологического университета имени Д.И. Менделеева
        (РХТУ).<br />
        Мы — сообщество студентов, объединённых любовью к интеллектуальным
        играм, стратегическому мышлению и живому общению.
      </p>

      <div class="social_icons">
        <span class="social_label">Подробнее:</span>
        <a href="tg" class="social_link">
          <img src="@/assets/social/telegram.svg" alt="Телеграмм" />
        </a>
        <a href="vk" class="social_link">
          <img src="@/assets/social/vk.svg" alt="ВКонтакте" />
        </a>
      </div>
    </div>

    <div class="city">
      <img src="@/assets/decor/city.png" alt="city" />
    </div>

    <div class="bottom_text">
      <span>ПРОСЫПАЕТСЯ МАФИЯ</span>
    </div>
  </div>
</template>

<script setup lang="ts">
// Логика страницы турниров
</script>

<style scoped>
.slide_element {
  display: flex;
  min-height: 90vh;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
  background-color: #1a1a1a;
}

.city {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.city img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: left bottom;
  opacity: 0.4;
}

.vertical_text {
  position: absolute;
  left: 20px;
  top: 10%;
  z-index: 2;
  color: #951228;
  font-family: serif;
  font-size: 24px;
  line-height: 1;
  letter-spacing: 10px;
  writing-mode: vertical-lr;
  text-orientation: upright;
}

.main_title {
  position: absolute;
  right: 15%;
  top: 30%;
  z-index: 2;
  max-width: 500px;
  text-align: left;
}

.main_title h1 {
  font-size: 48px;
  font-weight: 300;
  margin-bottom: 20px;
}

.main_title .highlight {
  color: #951228;
}

.main_title .subtext {
  font-size: 16px;
  line-height: 1.5;
  opacity: 0.8;
  margin-bottom: 30px;
}

.social_icons {
  display: flex;
  align-items: center;
  gap: 15px;
}

.social_label {
  font-size: 14px;
  opacity: 0.6;
  margin-right: 5px;
}

.social_link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  transition:
    background-color 0.3s ease,
    transform 0.2s ease;
}

.social_link img {
  width: 24px;
  height: 24px;
  filter: brightness(0) saturate(100%) invert(100%);
  opacity: 0.6;
}

.social_link:hover {
  background-color: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

.social_link:hover img {
  opacity: 1;
}

.bottom_text {
  position: absolute;
  bottom: 30px;
  right: 0;
  left: 0;
  text-align: center;
  z-index: 2;
  letter-spacing: 5px;
  color: #951228;
  font-weight: bold;
  font-size: 18px;
}
</style>
