<script setup lang="ts">
import {BackButton} from "vue-tg";
import {useRouter} from "vue-router";
import {Connect} from "src/api/types/subscribeTypes";
import {copyToClipboard, useQuasar} from "quasar";
import TgSection from "components/TgSection.vue";


const $q = useQuasar();
const router = useRouter();

const props = defineProps<Connect>()


const onCopy = () => {
  copyToClipboard(props.connectUrl)
    .then(() => {
      $q.notify({
        type: "positive",
        message: "Текст скопирован!",
        timeout: 2000,
      });
    })
    .catch(() => {
      $q.notify({
        type: "negative",
        message: "Ошибка при копировании текста.",
        timeout: 2000,
      });
    });
};
</script>

<template>
  <BackButton @click="() => router.back()"></BackButton>
  <q-page padding>
    <tg-section label="Connection url">
      <div class="copy-container">
        <q-card square class="copy-card" style="background-color: var(--tg-section-bg-color)">
          <q-card-section class="q-py-none">
            <div class="text-content">
              <code>
                <pre style="color: var(--tg-link-color);">{{ connectUrl }}</pre>
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
      </div>
    </tg-section>
  </q-page>
</template>

<style scoped>
.copy-container {
  display: flex;
  justify-content: center;
}

.copy-card {
  width: 100%;
  max-width: 600px;
  background-color: #f9f9f9;

}

.text-content pre {
  font-size: 12px;
  color: #333;
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
