<script setup lang="ts">

</script>

<template>
  <q-page padding>
    <q-btn
      label="Кнопка"
      class="tg-button"
    />
    <q-card :style="{ backgroundColor: 'var(--tg-bg-color)', color: 'var(--tg-text-color)' }">
      <q-card-section>
        <p style="color: var(--tg-hint-color)">Подсказка</p>
        <q-btn flat :style="{ color: 'var(--tg-link-color)' }">Ссылка</q-btn>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<style scoped>

</style>
