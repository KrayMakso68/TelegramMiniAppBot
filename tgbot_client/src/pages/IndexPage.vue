<script setup lang="ts">

</script>

<template>
  <q-page class="">
    <div class="column tg-text q-gutter-y-md">

      <div class="col column q-px-md q-pb-lg tg-text" style="background-color: var(--tg-bg-color);box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);">
        <transition name="jump-up" appear>
          <div class="text-h5">
            Привет,
          </div>
        </transition>
        <transition name="jump-right" appear>
          <div class="text-h4">
            Unknown User!
          </div>
        </transition>
      </div>

      <div class="col column q-pa-md" style="background-color: var(--tg-bg-color);">
        <div class="text-body2">fff</div>
        <q-list class="q-gutter-y-xs">
          <q-item v-for="n in 6" class="tg-list-item">
            <q-item-section>Single line item</q-item-section>
          </q-item>
        </q-list>
      </div>

      <div class="col bg-grey-8">
        ccc
      </div>
    </div>
  </q-page>
</template>

<style scoped>
.jump-up-enter-active {
  transition: transform 0.5s ease-in-out, opacity 0.5s;
}
.jump-up-enter-from {
  transform: translateY(-100%);
  opacity: 0;
}
.jump-up-enter-to {
  transform: translateY(0);
  opacity: 1;
}
.jump-right-enter-active {
  transition: transform 0.6s ease-in-out, opacity 0.5s;
}
.jump-right-enter-from {
  transform: translateX(-100%);
  opacity: 0;
}
.jump-right-enter-to {
  transform: translateX(0);
  opacity: 1;
}
</style>
