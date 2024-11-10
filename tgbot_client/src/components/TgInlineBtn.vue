<script setup lang="ts">

interface Props {
  icon?: string;
  to?: string;
  label: string;
}

defineProps<Props>();

const emit = defineEmits<{
  (e: 'click'): void;
}>();

const handleClick = () => {
  emit('click');
};
</script>

<template>
  <q-btn :to="to" rounded stack flat unelevated no-caps draggable="false">
    <div class="flex flex-center column tg-inline-btn">
      <q-icon size="md" :name=icon />
      <span>{{ label }}</span>
    </div>
  </q-btn>
</template>

<style scoped>
.tg-inline-btn {
  font-weight: 500;
  color: var(--tg-accent-text-color);
}
</style>
