<script setup lang="ts">

import TgSection from "components/TgSection.vue";
import PaymentsList from "components/PaymentsList.vue";
import {BackButton} from "vue-tg";
import { useRouter} from "vue-router";

const router = useRouter();
</script>

<template>
  <BackButton @click="() => router.back()"></BackButton>
  <q-page class="tg-text overflow-auto">
    <div class="column">

      <tg-section label="История операций" class="column">
        <payments-list/>
      </tg-section>

    </div>
  </q-page>
</template>

<style scoped>

</style>
