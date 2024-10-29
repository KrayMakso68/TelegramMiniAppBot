<script setup lang="ts">
import {ConnectListItem} from "components/models";

interface Props {
  items?: ConnectListItem[]
}

withDefaults(defineProps<Props>(), {
  items: () => [],
})

</script>

<template>
  <q-list v-if="items.length > 0">
    <template v-for="(item, index) in items" :key="index">
      <q-item :to="item.link" v-ripple draggable="false">
        <q-item-section avatar>
          <q-avatar :icon=item.icon class="tg-list-item-icon"/>
        </q-item-section>
        <q-item-section>
          {{ item.text }}
        </q-item-section>
      </q-item>
      <q-separator v-if="index < items.length - 1" inset="item" class="tg-separator" />
    </template>
  </q-list>


  <q-list v-else>
    <template v-for="index in 3" :key="index">
      <q-item v-ripple>
        <q-item-section avatar>
          <q-avatar>
            <q-skeleton size="25px" type="QAvatar"  />
          </q-avatar>
        </q-item-section>
        <q-item-section>
          <q-skeleton width="40%" type="text" />
        </q-item-section>
      </q-item>
      <q-separator v-if="index < 3" inset="item" class="tg-separator" />
    </template>
  </q-list>
</template>

<style scoped>

</style>
