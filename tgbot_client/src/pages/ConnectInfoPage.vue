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
  <BackButton @click="() => router.back()"></BackButton>
  <q-page padding>

      <div class="copy-container">
        <q-card flat class="copy-card">

          <q-card-section
            class="q-pa-none q-pl-md"
            style="background-color: var(--tg-button-color); border-top-left-radius: 0px; color: var(--tg-accent-text-color);"
          >
            <div class="text-caption text-no-wrap">
              Connection url
            </div>
          </q-card-section>

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
    <tg-section label="test" class="q-mt-lg">
      <div>
        fdfd
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
  background-color: var(--tg-section-bg-color);
  border-radius: 4px;
  border-left: 3px solid var(--tg-accent-text-color);
}

.text-content pre {
  font-size: 12px;
  color: #333;
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
