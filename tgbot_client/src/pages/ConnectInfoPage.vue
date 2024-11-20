<script setup lang="ts">
import {BackButton} from "vue-tg";
import {useRouter} from "vue-router";
import {Connect} from "src/api/types/subscribeTypes";
import TgSection from "components/TgSection.vue";
import TgCodeCard from "components/TgCodeCard.vue";

const router = useRouter();
defineProps<Connect>()
</script>

<template>
  <BackButton @click="() => router.back()"></BackButton>
  <q-page class="tg-text overflow-auto">
    <div class="q-gutter-y-md">
      <tg-section>
        <div class="text-h5 text-center">
          {{email}}
        </div>
      </tg-section>

      <tg-code-card title="Connection url" :text=connectUrl class=""/>

      <tg-section label="Расход трафика">
        dsfsd
      </tg-section>

    </div>
  </q-page>
</template>

<style scoped>

</style>
