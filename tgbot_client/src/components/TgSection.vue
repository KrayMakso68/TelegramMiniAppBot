<script setup lang="ts">
import {computed} from "vue";

interface Props {
  label?: string;
  customClass?: string;
}
const props = defineProps<Props>()

const labelClass = computed(() => props.customClass || 'tg-section-header');

function reload() {
  console.log("Перезагрузка...");
  // Здесь можно вызвать метод обновления данных
}
</script>

<template>
  <div class="tg-section" >
<!--    <q-item-label v-if="label" header :class="labelClass">-->
<!--      {{ label }}-->
<!--    </q-item-label>-->
    <q-item class="q-pa-none">
      <q-item-section class="q-pa-none">
        <q-item-label v-if="label" header :class="labelClass">
          {{ label }}
        </q-item-label>
      </q-item-section>

      <q-item-section side>
        <q-btn flat dense round icon="refresh" @click="reload" />
      </q-item-section>
    </q-item>
    <slot></slot>
  </div>
</template>

<style scoped>

</style>
