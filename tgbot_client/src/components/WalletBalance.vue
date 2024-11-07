<script setup lang="ts">
import {ref} from "vue";

const amount = ref<number | null>(null)
</script>

<template>
  <div class="row justify-start items-center q-px-lg q-gutter-sm">
    <div class="col-auto tg-subtitle-text">
      <div class="text-h4 text-weight-regular">₽</div>
    </div>
    <div v-if="amount" class="col-auto tg-text">
      <div class="text-h4 text-weight-regular">{{ amount }}</div>
    </div>
    <div v-else class="col-3 tg-text">
      <q-skeleton type="rect"/>
    </div>
  </div>
</template>

<style scoped>

</style>
