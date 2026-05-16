import { defineStore } from "pinia";
import { markRaw } from "vue";
import Slide1 from "@/core/views/mainMafiaPages/components/mainSlides/Slide1.vue";
import Slide2 from "@/core/views/mainMafiaPages/components/mainSlides/Slide2.vue";
import Slide3 from "@/core/views/mainMafiaPages/components/mainSlides/Slide3.vue";
import Slide4 from "@/core/views/mainMafiaPages/components/mainSlides/Slide4.vue";

export const useSlidesStore = defineStore("slides", {
  state: () => ({
    slides: [
      { component: markRaw(Slide1) },
      { component: markRaw(Slide2) },
      { component: markRaw(Slide3) },
      { component: markRaw(Slide4) },
    ],
  }),
});
