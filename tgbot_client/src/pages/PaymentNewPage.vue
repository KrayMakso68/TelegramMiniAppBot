<script setup lang="ts">
import {useRouter} from "vue-router";
import TgSection from "components/TgSection.vue";
import {BackButton, MainButton, useWebAppNavigation} from "vue-tg";
import {PaymentService} from "src/api";
import {ref} from "vue";

const router = useRouter();
const {openLink} = useWebAppNavigation();

const input = ref<number>(0)

const newYoomoneyPayment = async (amount: number) => {
  let url = await PaymentService.newYoomoneyPayment(amount)
  if (url) {
    openLink(url);
  }
};
</script>

<template>
  <BackButton @click="() => router.back()"></BackButton>
  <MainButton text="PAY" @click="newYoomoneyPayment(120)"></MainButton>
  <q-page class="tg-text overflow-auto">
    <div class="q-gutter-y-md">
      <tg-section label="Новый платёж">
        <div class="q-ml-md q-mt-xl">
          <div>Пополнение на</div>
          <q-input
            v-model="input"
            borderless
            autofocus
          >
          </q-input>
        </div>
      </tg-section>
    </div>
  </q-page>


</template>

<style scoped>

</style>
