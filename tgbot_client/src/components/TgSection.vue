<script setup lang="ts">
interface Props {
  label?: string
}
defineProps<Props>()

</script>

<template>
  <div class="col tg-section" >
    <q-item-label v-if="label" header class="tg-section-header">
      {{ label }}
    </q-item-label>
    <slot></slot>
  </div>
</template>

<style scoped>

</style>
