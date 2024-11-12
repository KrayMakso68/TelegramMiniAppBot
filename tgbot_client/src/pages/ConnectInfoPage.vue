<script setup lang="ts">
import {BackButton} from "vue-tg";
import { useRouter} from "vue-router";
import {Connect} from "src/api/types/subscribeTypes";

const router = useRouter();

defineProps<Connect>()
</script>

<template>
  <BackButton @click="() => router.back()"></BackButton>
  <q-page padding class="text-green-6 ">
    <div class="column">
      <q-card class="col row">
        <q-card-section>
          {{email}}
        </q-card-section>
      </q-card>
    </div>
    <div class="column">
      <q-card class="col row">
        <q-card-section>
          {{inboundName}}
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<style scoped>

</style>
