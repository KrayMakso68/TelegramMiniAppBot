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
  <div class="column flex-center q-pb-lg">
    <div class="col q-pa-xs lottie-animation">
      <div ref="lottieContainer"/>
    </div>
    <div class="col text-center text-h6 tg-text">
      {{title}}
    </div>
  </div>
</template>

<style scoped>
.lottie-animation {
  width: 200px;
}
</style>
