<script setup lang="ts">
import lottie from 'lottie-web';
import {onMounted, ref} from "vue";

import {ConnectListItem} from "components/models";

interface Props {
  items?: ConnectListItem[]
}

withDefaults(defineProps<Props>(), {
  items: () => [],
})

const lottieContainer = ref<HTMLElement | null>(null);
onMounted(() => {
  if (lottieContainer.value) {
    lottie.loadAnimation({
      container: lottieContainer.value,
      renderer: 'svg',
      loop: true,
      autoplay: true,
      path: 'stickers/ResistanceDog.json'
    });
  }
});

</script>

<template>
  <q-list v-if="items.length > 0">
    <template v-for="(item, index) in items" :key="index">
      <q-item :to="item.link" v-ripple>
        <q-item-section avatar>
          <q-avatar :icon=item.icon class="tg-list-item-icon"/>
        </q-item-section>
        <q-item-section>
          {{ item.text }}
        </q-item-section>
      </q-item>
      <q-separator v-if="index < items.length - 1" inset="item" class="tg-separator" />
    </template>
  </q-list>


  <q-list v-else>
    <template v-for="index in 3" :key="index">
      <q-item v-ripple>
        <q-item-section avatar>
          <q-avatar>
            <q-skeleton size="25px" type="QAvatar"  />
          </q-avatar>
        </q-item-section>
        <q-item-section>
          <q-skeleton width="40%" type="text" />
        </q-item-section>
      </q-item>
      <q-separator v-if="index < 3" inset="item" class="tg-separator" />
    </template>
  </q-list>

  <div class="column q-px-xxl q-py-xl items-center justify-center">
    <div id="lottie-animation" ref="lottieContainer"></div>
    <div class="text-h6">Похоже, у вас нет подписок</div>
  </div>
</template>

<style scoped>
#lottie-animation {
  width: 50%;
}
</style>
