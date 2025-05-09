<script setup lang="ts">

</script>

<template>
  <q-list dense class="tg-text">
    <q-item to="help/mobile">
      <q-item-section avatar class="tg-list-item-icon">
        <q-avatar icon='phone_iphone' font-size="24px"/>
      </q-item-section>

      <q-item-section>
        <q-item-label>IPhone / Android</q-item-label>
      </q-item-section>

      <q-item-section side>
        <q-avatar icon='navigate_next' class="tg-subtitle-text"/>
      </q-item-section>
    </q-item>

    <q-item to="help/desktop">
      <q-item-section avatar class="tg-list-item-icon">
        <q-avatar icon='desktop_windows' font-size="24px"/>
      </q-item-section>

      <q-item-section>
        <q-item-label>Windows / Mac</q-item-label>
      </q-item-section>

      <q-item-section side>
        <q-avatar icon='navigate_next' class="tg-subtitle-text"/>
      </q-item-section>
    </q-item>

  </q-list>
</template>

<style scoped>

</style>
