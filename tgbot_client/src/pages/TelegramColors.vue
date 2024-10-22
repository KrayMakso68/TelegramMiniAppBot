<script setup lang="ts">
import { BackButton } from "vue-tg";
import { useRouter} from "vue-router";

const router = useRouter();

</script>

<template>
  <BackButton @click="() => router.back()"></BackButton>
  <q-page padding class="q-gutter-sm">
    <!--    <q-btn-->
    <!--      label="Кнопка"-->
    <!--      class="tg-button"-->
    <!--    />-->
    <q-card :style="{ backgroundColor: 'var(--tg-bg-color)' }">
      <q-card-section>
        <p class="tg-text">1) --tg-bg-color</p>
      </q-card-section>
    </q-card>
    <q-card :style="{ backgroundColor: 'var(--tg-text-color)' }">
      <q-card-section>
        <p class="tg-text">2) --tg-text-color</p>
      </q-card-section>
    </q-card>
    <q-card :style="{ backgroundColor: 'var(--tg-hint-color)' }">
      <q-card-section>
        <p class="tg-text">3) --tg-hint-color</p>
      </q-card-section>
    </q-card>
    <q-card :style="{ backgroundColor: 'var(--tg-link-color)' }">
      <q-card-section>
        <p class="tg-text">4) --tg-link-color</p>
      </q-card-section>
    </q-card>
    <q-card :style="{ backgroundColor: 'var(--tg-button-color)' }">
      <q-card-section>
        <p class="tg-text">5) --tg-button-color</p>
      </q-card-section>
    </q-card>
    <q-card :style="{ backgroundColor: 'var(--tg-button-text-color)' }">
      <q-card-section>
        <p class="tg-text">6) --tg-button-text-color</p>
      </q-card-section>
    </q-card>
    <q-card :style="{ backgroundColor: 'var(--tg-secondary-bg-color)' }">
      <q-card-section>
        <p class="tg-text">7) --tg-secondary-bg-color</p>
      </q-card-section>
    </q-card>
    <q-card :style="{ backgroundColor: 'var(--tg-header-bg-color)' }">
      <q-card-section>
        <p class="tg-text">8) --tg-header-bg-color</p>
      </q-card-section>
    </q-card>
    <q-card :style="{ backgroundColor: 'var(--tg-bottom-bar-bg-color)' }">
      <q-card-section>
        <p class="tg-text">9) --tg-bottom-bar-bg-color</p>
      </q-card-section>
    </q-card>
    <q-card :style="{ backgroundColor: 'var(--tg-accent-text-color)' }">
      <q-card-section>
        <p class="tg-text">10) --tg-accent-text-color</p>
      </q-card-section>
    </q-card>
    <q-card :style="{ backgroundColor: 'var(--tg-section-bg-color)' }">
      <q-card-section>
        <p class="tg-text">11) --tg-section-bg-color</p>
      </q-card-section>
    </q-card>
    <q-card :style="{ backgroundColor: 'var(--tg-section-header-text-color)' }">
      <q-card-section>
        <p class="tg-text">12) --tg-section-header-text-color</p>
      </q-card-section>
    </q-card>
    <q-card :style="{ backgroundColor: 'var(--tg-section-separator-color)' }">
      <q-card-section>
        <p class="tg-text">13) --tg-section-separator-color</p>
      </q-card-section>
    </q-card>
    <q-card :style="{ backgroundColor: 'var(--tg-subtitle-text-color)' }">
      <q-card-section>
        <p class="tg-text">14) --tg-subtitle-text-color</p>
      </q-card-section>
    </q-card>
    <q-card :style="{ backgroundColor: 'var(--tg-destructive-text-color)' }">
      <q-card-section>
        <p class="tg-text">15) --tg-destructive-text-color</p>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<style scoped>

</style>
