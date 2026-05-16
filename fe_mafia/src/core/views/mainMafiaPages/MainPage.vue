<template>
  <div class="main-conteiner" @wheel.prevent="handleWheel" ref="container">
    <div
      v-for="(slide, index) in slidesStore.slides"
      :key="index"
      class="slide"
    >
      <component :is="slide.component" v-bind="slide.props || {}" />
    </div>
  </div>
  <WebGLFluidSmoke />
</template>

<script setup>
import { ref } from "vue";
import { useSlidesStore } from "@/stores/mainSlider/sliderStore";
import WebGLFluidSmoke from "@/core/SmokeElement/WebGLFluidSmoke.vue";

const container = ref(null);
const currentIndex = ref(0);
const slidesStore = useSlidesStore();
let isScrolling = false;

const scrollToSlide = (index) => {
  if (container.value) {
    container.value.scrollTo({
      top: index * window.innerHeight,
      behavior: "smooth",
    });
  }
};

const handleWheel = (event) => {
  if (isScrolling) return;

  isScrolling = true;

  if (event.deltaY > 0 && currentIndex.value < slidesStore.slides.length - 1) {
    currentIndex.value++;
    scrollToSlide(currentIndex.value);
  } else if (event.deltaY < 0 && currentIndex.value > 0) {
    currentIndex.value--;
    scrollToSlide(currentIndex.value);
  }

  setTimeout(() => {
    isScrolling = false;
  }, 500);
};
</script>

<style scoped>
.main-conteiner {
  height: 100vh;
  overflow-y: scroll;
  scroll-snap-type: y mandatory;
}
.slide {
  height: 100vh;
  scroll-snap-align: start;
}
</style>
