<script setup lang="ts">

import {BackButton, MainButton} from "vue-tg";
import TgSection from "components/TgSection.vue";
import {useRouter} from "vue-router";

const router = useRouter();

</script>

<template>
  <BackButton @click="() => router.back()"></BackButton>
  <MainButton text="хуй" @click="newPayment"></MainButton>

  <q-page class="tg-text overflow-auto">

    <div class="q-gutter-y-md">
      <tg-section label="Новая подписка">
<!--        <div class="q-mx-md q-mt-xl q-pb-lg">-->
<!--          <div style="font-size: 16px;" class="tg-subtitle-text">Сумма пополнения</div>-->
<!--          <q-input-->
<!--            class="payment-input hide-spin-buttons"-->
<!--            input-class="input"-->
<!--            type="number"-->
<!--            borderless-->
<!--            clearable-->
<!--            autofocus-->
<!--            prefix="₽"-->
<!--            mask="#.##"-->
<!--            error-message="Cумма от 2₽ до 15000₽"-->
<!--            :error="!isValid"-->
<!--            v-model="inputValue"-->
<!--          />-->
<!--          <q-separator class="tg-separator"></q-separator>-->
<!--          <q-select-->
<!--            v-model="selectValue"-->
<!--            :loading="isLoading"-->
<!--            :options="options"-->
<!--            borderless-->
<!--            dark-->
<!--            class="payment-type q-mt-sm"-->
<!--            clearable-->
<!--            label="Способ оплаты"-->
<!--          />-->
<!--        </div>-->
        <div>
          <q-input borderless v-model="text" label="Label (stacked)" stack-label style="border: 1.5px solid var(--tg-hint-color); border-radius: 14px; padding-left: 10px;" />
        </div>
      </tg-section>
    </div>

  </q-page>
</template>

<style scoped>

</style>
