<template>
  <div class="slide_element">
    <div class="text-content">
      <h1>Правила <span class="highlight">спортивной</span> мафии</h1>
      <p class="description">
        За столом — 10 игроков. Они получают карты, которые определяют их роль:
        мирные жители, мафия, а также дон (глава мафии) и шериф (единственный,
        кто может узнать роль другого игрока). Игра проходит в чередовании
        дневных и ночных фаз. Ночью мафия «убивает» одного из мирных, а шериф
        может проверить одного игрока на принадлежность к мафии. Днём все
        участники обсуждают, кто, по их мнению, является мафией, и открытым
        голосованием выгоняют одного подозреваемого из игры.
      </p>
      <button class="rules-btn">Подробнее →</button>
    </div>

    <div class="cards-container">
      <div class="card-item card-4">
        <img src="@/assets/decor/black.png" alt="mafia" />
      </div>

      <div class="card-item card-3">
        <img src="@/assets/decor/red.png" alt="peaceful" />
      </div>

      <div class="card-item card-2">
        <img src="@/assets/decor/don.png" alt="don" />
      </div>

      <div class="card-item card-1">
        <img src="@/assets/decor/sheriff.png" alt="sheriff" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts"></script>

<style scoped>
.slide_element {
  display: flex;
  min-height: 90vh;
  align-items: center;
  justify-content: space-between;
  padding: 0 100px;
  position: relative;
  overflow: hidden;
}

.text-content {
  max-width: 750px;
	margin-bottom: 350px;
  z-index: 10;
}

.text-content h1 {
  max-width: 550px;
  font-size: 56px;
  margin-bottom: 25px;
  font-weight: 300;
}

.text-content .highlight {
  color: #951228;
}

.text-content .description {
  font-size: 18px;
  line-height: 1.6;
  margin-bottom: 20px;
}

.rules-btn {
  background: transparent;
  border: 1px solid #951228;
  color: #951228;
  padding: 12px 35px;
  border-radius: 10px;
  cursor: pointer;
  font-size: 16px;
  font-family: inherit;
  transition: 0.3s;
}

.rules-btn:hover {
  background: #951228;
  color: white;
}

.cards-container {
  position: relative;
  width: 550px;
  height: 450px;
  transform: translateX(20vh) translateY(8vh) rotate(-60deg);
}

.card-item {
  position: absolute;
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.3s ease;
}

.card-item img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-1 {
  width: 390px;
  height: 490px;
  top: 40px;
  left: 220px;
  transform: rotate(12deg);
  z-index: 4;
}

.card-2 {
  width: 350px;
  height: 430px;
  top: 60px;
  left: 140px;
  transform: rotate(0deg);
  z-index: 3;
}

.card-3 {
  width: 340px;
  height: 420px;
  top: 30px;
  left: 70px;
  transform: rotate(-10deg);
  z-index: 2;
}

.card-4 {
  width: 330px;
  height: 410px;
  top: 0;
  left: 0;
  transform: rotate(-20deg) translateX(-20px);
  z-index: 1;
}
.card-1:hover {
  transform: rotate(12deg) translateX(-50px) translateY(-50px);
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.card-2:hover {
  transform: rotate(0deg) translateX(-50px) translateY(-50px);
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.card-3:hover {
  transform: rotate(-10deg) translateX(-50px) translateY(-50px);
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.card-4:hover {
  transform: rotate(-20deg) translateX(-50px) translateY(-50px);
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}
</style>
