<script setup lang="ts">
import { SettingsButton } from 'vue-tg'
import { useRouter } from 'vue-router';

const router = useRouter()
</script>

<template>
  <q-layout view="hHh lpR fFf">
    <SettingsButton  @click="() => router.push('test-colors')"></SettingsButton>
    <q-page-container class="tg-background">
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<style scoped>

</style>
