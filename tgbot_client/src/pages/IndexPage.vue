<script setup lang="ts">
import {ref} from "vue";
import ConnectionsList from "components/ConnectionsList.vue";
import {ConnectListItem} from "components/models";
import UserWelcome from "components/UserWelcome.vue";
import TgSection from "components/TgSection.vue";
import NotFoundBanner from "components/NotFoundBanner.vue";
import WalletBalance from "components/WalletBalance.vue";

const items = ref<ConnectListItem[]>([
  { text: 'Item 1', icon: 'vpn_lock', link: 'test-colors' },
  { text: 'Item 2', icon: 'vpn_key', link: 'test-colors' },
  { text: 'Item 3', icon: 'vpn_lock', link: 'test-colors' },
])
</script>

<template>
  <q-page class="tg-text">
    <div class="column q-gutter-y-md">

      <tg-section class="q-px-lg q-pb-md q-pb-lg">
        <user-welcome/>
      </tg-section>

      <tg-section label="Баланс кошелька">
        <wallet-balance/>
      </tg-section>

      <tg-section label="Подключения" class="column">
        <connections-list :items="items"/>
        <not-found-banner title="Похоже, у вас нет подписок!"/>
      </tg-section>

      <tg-section label="test">

      </tg-section>
    </div>
  </q-page>
</template>

<style scoped>

</style>
