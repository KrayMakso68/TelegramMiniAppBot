<script setup lang="ts">
import {computed} from "vue";

interface Props {
  label?: string;
  reload?: boolean;
  customLabelClass?: string;
}
const props = defineProps<Props>()

const labelClass = computed(() => props.customLabelClass || 'tg-section-header');

const emit = defineEmits<{
  (e: "reload"): void;
}>();
</script>

<template>
  <div class="tg-section" >
    <q-item v-if="label || reload" class="q-pa-none">

      <q-item-section v-if="label">
        <q-item-label header :class="labelClass">
          {{ label }}
        </q-item-label>
      </q-item-section>

      <q-item-section v-if="reload" side class="q-mr-md">
        <q-btn flat dense round icon="sync" @click="emit('reload')"/>
      </q-item-section>

    </q-item>

    <slot></slot>

  </div>
</template>

<style scoped>

</style>
