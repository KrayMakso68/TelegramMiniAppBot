<script setup lang="ts">
import {computed, getCurrentInstance, nextTick, onMounted, ref} from "vue";
import {PanelService} from "src/api";

interface Props {
  label?: string;
  customLabelClass?: string;
}
const props = defineProps<Props>()
const labelClass = computed(() => props.customLabelClass || 'tg-section-header');

</script>

<template>
  <div class="tg-section" >
    <q-item v-if="label" class="q-pa-none">
      <q-item-section v-if="label">
        <q-item-label header :class="labelClass">
          {{ label }}
        </q-item-label>
      </q-item-section>
    </q-item>

    <slot></slot>

  </div>
</template>

<style scoped>

</style>
