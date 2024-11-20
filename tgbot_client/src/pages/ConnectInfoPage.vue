<script setup lang="ts">
import {BackButton} from "vue-tg";
import {useRouter} from "vue-router";
import {Connect} from "src/api/types/subscribeTypes";
import TgSection from "components/TgSection.vue";
import TgCodeCard from "components/TgCodeCard.vue";

const router = useRouter();
defineProps<Connect>();

const loadInfo = () => {

};
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
      <div class="q-px-xs">
        <tg-code-card title="Connection url" :text=connectUrl />
      </div>



        <q-expansion-item
        style="background-color: var(--tg-section-bg-color); border-radius: 5px"
        icon="query_stats"
        label="Подробная информация"
        @show="loadInfo"
      >
        <q-card>
          <q-card-section>
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quidem, eius reprehenderit eos corrupti
            commodi magni quaerat ex numquam, dolorum officiis modi facere maiores architecto suscipit iste
            eveniet doloribus ullam aliquid.
          </q-card-section>
        </q-card>
      </q-expansion-item>


    </div>
  </q-page>
</template>

<style scoped>

</style>
