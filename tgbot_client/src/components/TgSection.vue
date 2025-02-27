<script setup lang="ts">
import {computed} from "vue";

interface Props {
  label?: string;
  customClass?: string;
}
const props = defineProps<Props>()

const labelClass = computed(() => props.customClass || 'tg-section-header');
</script>

<template>
  <div class="col tg-section" >
    <q-item-label v-if="label" :style="labelStyle" header :class="labelClass">
      {{ label }}
    </q-item-label>
    <slot></slot>
  </div>
</template>

<style scoped>

</style>
