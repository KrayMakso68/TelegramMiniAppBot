<script setup lang="ts">
import {ref} from "vue";
import TgInlineBtn from "components/TgInlineBtn.vue";

const amount = ref<number | null>(500)
</script>

<template>
  <div class="row justify-start items-center q-px-lg q-py-xs q-gutter-sm">
    <div class="col-auto tg-subtitle-text">
      <div class="text-h4 text-weight-medium">₽</div>
    </div>
    <div v-if="amount" class="col-auto tg-text">
      <div class="text-h4 text-weight-regular">{{ amount }}</div>
    </div>
    <div v-else class="col-3 tg-text">
      <q-skeleton type="rect"/>
    </div>
  </div>
  <div class="flex row justify-evenly q-pa-sm q-gutter-sm">
    <tg-inline-btn to="test-colors" class="col" label="Пополнить" icon="add_circle"/>
    <tg-inline-btn to="" class="col" label="История" icon="history"/>
  </div>

</template>

<style scoped>

</style>
