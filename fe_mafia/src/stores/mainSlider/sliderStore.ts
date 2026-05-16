import { defineStore } from "pinia";
import Slide1 from "@/core/components/mainSlides/Slide1.vue";
import Slide2 from "@/core/components/mainSlides/Slide2.vue";
import Slide3 from "@/core/components/mainSlides/Slide3.vue";
import Slide4 from "@/core/components/mainSlides/Slide4.vue";

export const useSlidesStore = defineStore("slides", {
  state: () => ({
    slides: [
      { component: Slide1 },
      { component: Slide2 },
      { component: Slide3 },
      { component: Slide4 },
    ],
  }),
});
