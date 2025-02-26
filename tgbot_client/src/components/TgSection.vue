<script setup lang="ts">
import {computed} from "vue";

interface Props {
  label?: string;
  labelSize?: string;
}
const props = defineProps<Props>()

const labelStyle = computed(() => ({
  fontSize: props.labelSize || "15px", // Значение по умолчанию
}));
</script>

<template>
  <div class="col tg-section" >
    <q-item-label v-if="label" :style="labelStyle" header class="tg-section-header">
      {{ label }}
    </q-item-label>
    <slot></slot>
  </div>
</template>

<style scoped>

</style>
