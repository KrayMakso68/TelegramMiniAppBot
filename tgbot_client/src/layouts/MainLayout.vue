<script setup lang="ts">
import {BackButton, SettingsButton} from 'vue-tg'
</script>

<template>
  <q-layout view="hHh lpR fFf">
    <BackButton visible="" ></BackButton>
    <SettingsButton></SettingsButton>
    <q-page-container>
      <router-view />
    </q-page-container>

  </q-layout>
</template>

<style scoped>
q-layout{

}
</style>
