<script setup lang="ts">

import {BackButton, SettingsButton} from "vue-tg";
import { useWebAppTheme } from "vue-tg";

const {  } = useWebAppTheme()
</script>

<template>
<!--  <BackButton visible="" ></BackButton>-->
<!--  <SettingsButton></SettingsButton>-->
  <q-page padding class="q-gutter-sm">
<!--    <q-btn-->
<!--      label="Кнопка"-->
<!--      class="tg-button"-->
<!--    />-->
    <q-card :style="{ backgroundColor: 'var(--tg-bg-color)' }">
      <q-card-section>
        <p style="color: var(--tg-hint-color)">1) --tg-bg-color</p>
      </q-card-section>
    </q-card>
    <q-card :style="{ backgroundColor: 'var(--tg-text-color)' }">
      <q-card-section>
        <p style="color: var(--tg-hint-color)">2) --tg-text-color</p>
      </q-card-section>
    </q-card>
    <q-card :style="{ backgroundColor: 'var(--tg-hint-color)' }">
      <q-card-section>
        <p style="color: var(--tg-hint-color)">3) --tg-hint-color</p>
      </q-card-section>
    </q-card>
    <q-card :style="{ backgroundColor: 'var(--tg-link-color)' }">
      <q-card-section>
        <p style="color: var(--tg-hint-color)">4) --tg-link-color</p>
      </q-card-section>
    </q-card>
    <q-card :style="{ backgroundColor: 'var(--tg-button-color)' }">
      <q-card-section>
        <p style="color: var(--tg-hint-color)">5) --tg-button-color</p>
      </q-card-section>
    </q-card>
    <q-card :style="{ backgroundColor: 'var(--tg-button-text-color)' }">
      <q-card-section>
        <p style="color: var(--tg-hint-color)">6) --tg-button-text-color</p>
      </q-card-section>
    </q-card>
    <q-card :style="{ backgroundColor: 'var(--tg-secondary-bg-color)' }">
      <q-card-section>
        <p style="color: var(--tg-hint-color)">7) --tg-secondary-bg-color</p>
      </q-card-section>
    </q-card>
    <q-card :style="{ backgroundColor: 'var(--tg-header-bg-color)' }">
      <q-card-section>
        <p style="color: var(--tg-hint-color)">8) --tg-header-bg-color</p>
      </q-card-section>
    </q-card>
    <q-card :style="{ backgroundColor: 'var(--tg-bottom-bar-bg-color)' }">
      <q-card-section>
        <p style="color: var(--tg-hint-color)">9) --tg-bottom-bar-bg-color</p>
      </q-card-section>
    </q-card>
    <q-card :style="{ backgroundColor: 'var(--tg-accent-text-color)' }">
      <q-card-section>
        <p style="color: var(--tg-hint-color)">10) --tg-accent-text-color</p>
      </q-card-section>
    </q-card>
    <q-card :style="{ backgroundColor: 'var(--tg-section-bg-color)' }">
      <q-card-section>
        <p style="color: var(--tg-hint-color)">11) --tg-section-bg-color</p>
      </q-card-section>
    </q-card>
    <q-card :style="{ backgroundColor: 'var(--tg-section-header-text-color)' }">
      <q-card-section>
        <p style="color: var(--tg-hint-color)">12) --tg-section-header-text-color</p>
      </q-card-section>
    </q-card>
    <q-card :style="{ backgroundColor: 'var(--tg-section-separator-color)' }">
      <q-card-section>
        <p style="color: var(--tg-hint-color)">13) --tg-section-separator-color</p>
      </q-card-section>
    </q-card>
    <q-card :style="{ backgroundColor: 'var(--tg-subtitle-text-color)' }">
      <q-card-section>
        <p style="color: var(--tg-hint-color)">14) --tg-subtitle-text-color</p>
      </q-card-section>
    </q-card>
    <q-card :style="{ backgroundColor: 'var(--tg-destructive-text-color)' }">
      <q-card-section>
        <p style="color: var(--tg-hint-color)">15) --tg-destructive-text-color</p>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<style scoped>

</style>
