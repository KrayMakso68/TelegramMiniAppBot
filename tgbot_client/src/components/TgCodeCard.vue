<script setup lang="ts">
import {copyToClipboard, useQuasar} from "quasar";

interface Props {
  title?: string | undefined,
  text: string
}

const props = defineProps<Props>()
const $q = useQuasar();

const onCopy = () => {
  copyToClipboard(props.text)
    .then(() => {
      $q.notify({
        type: "positive",
        message: "Текст скопирован!",
        timeout: 1000,
      });
    })
    .catch(() => {
      $q.notify({
        type: "negative",
        message: "Ошибка при копировании текста.",
        timeout: 1000,
      });
    });
};
</script>

<template>
  <q-card class="copy-card">

    <q-card-section class="q-pa-none q-pl-md transparent-background">
      <div class="text-caption text-no-wrap">
        {{ title }}
      </div>
    </q-card-section>

    <q-card-section class="q-py-none">
      <div class="text-content">
        <code>
          <pre>{{ text }}</pre>
        </code>
      </div>
    </q-card-section>

    <q-card-actions vertical class="q-pa-none">
      <q-btn style="color: var(--tg-button-color);"
             flat
             size="sm"
             icon="content_copy"
             @click="onCopy"
             label="Copy"
      />
    </q-card-actions>

  </q-card>
</template>

<style scoped>
.copy-card {
  width: 100%;
  max-width: 600px;
  background-color: var(--tg-section-bg-color);
  border-radius: 5px;
  border-left: 4px solid var(--tg-accent-text-color);
}

pre {
  color: var(--tg-link-color);
  font-size: 12px;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.transparent-background {
  position: relative;
  color: var(--tg-accent-text-color);
  z-index: 0;
}

.transparent-background::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: var(--tg-accent-text-color);
  border-top-right-radius: 4px;
  opacity: 0.25;
  z-index: -1;
}
</style>
