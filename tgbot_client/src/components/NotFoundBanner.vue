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
  <div class="column flex-center q-pb-md q-col-gutter-sm">
    <div class="col lottie-animation">
      <div ref="lottieContainer"/>
    </div>
    <div class="col col-8 text-center text-h6 tg-text">
      {{title}}
    </div>
    <div class="col col-8">
      <q-btn class="tg-btn">Подключить</q-btn>
    </div>
  </div>
</template>

<style scoped>
.lottie-animation {
  width: 150px;
}
</style>
