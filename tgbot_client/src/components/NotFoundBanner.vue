<script setup lang="ts">
import {onMounted, ref} from "vue";
import lottie from "lottie-web";

interface Props {
  title?: string;
  path?: string;
}

const props = withDefaults(defineProps<Props>(), {
  title: 'Не найдено',
  path: 'stickers/ResistanceDog.json'
})

const lottieContainer = ref<HTMLElement | null>(null);
onMounted(() => {
  if (lottieContainer.value) {
    lottie.loadAnimation({
      container: lottieContainer.value,
      renderer: 'svg',
      loop: true,
      autoplay: true,
      path: props.path
    });
  }
});
</script>

<template>
  <div class="column q-px-xxl q-py-xl items-center justify-center">
    <div id="lottie-animation" ref="lottieContainer"></div>
    <div class="text-h6">{{title}}</div>
  </div>
</template>

<style scoped>
#lottie-animation {
  width: 50%;
}
</style>
