<script setup lang="ts">

interface Props {
  label: string;
  icon?: string;
  to?: string;
  size?: string;
}

withDefaults(defineProps<Props>(), {
  size: 'md'
})

// const emit = defineEmits<{
//   (e: 'click'): void;
// }>();
//
// const handleClick = () => {
//   emit('click');
// };
</script>

<template>
  <q-btn :to="to" :size="size" rounded stack flat unelevated no-caps draggable="false">
    <div class="flex flex-center column tg-inline-btn">
      <q-icon :size="size" :name=icon />
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
