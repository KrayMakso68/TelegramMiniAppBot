<script setup lang="ts">
import {useRouter} from "vue-router";
import TgSection from "components/TgSection.vue";
import {BackButton, MainButton, useWebAppNavigation} from "vue-tg";
import {PaymentService} from "src/api";

const router = useRouter();
const {openLink} = useWebAppNavigation();

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
        <div>dsd</div>
      </tg-section>
    </div>
  </q-page>


</template>

<style scoped>

</style>
