<script setup lang="ts">
import SubscriptionsList from "components/SubscriptionsList.vue";
import UserWelcome from "components/UserWelcome.vue";
import TgSection from "components/TgSection.vue";
import WalletBalance from "components/WalletBalance.vue";
import HelpConnectList from "components/HelpConnectList.vue";

</script>

<template>
  <q-page class="tg-text overflow-auto">
    <div class="column q-gutter-y-md">

      <tg-section class="q-px-lg q-pb-md q-pb-lg">
        <user-welcome/>
      </tg-section>

      <tg-section label="Баланс кошелька">
        <wallet-balance/>
      </tg-section>

      <tg-section label="Подключения">
        <subscriptions-list/>
      </tg-section>

      <tg-section label="Как подключить?">
        <help-connect-list/>
      </tg-section>

    </div>
  </q-page>
</template>

<style scoped>

</style>
