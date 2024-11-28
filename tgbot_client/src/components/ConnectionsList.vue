<script setup lang="ts">
import NotFoundBanner from "components/NotFoundBanner.vue";
import {onMounted, Ref, ref} from "vue";
import {Connect} from "src/api/types/subscribeTypes";
import {SubscriberService} from "src/api";

const loading  = ref<boolean>(true);
const connects: Ref<Connect[] | null> = ref<Connect[] | null>(null);

const loadConnects = async () => {
  connects.value = await SubscriberService.getUserConnects();
  loading.value = false;
};


onMounted(loadConnects);
</script>

<template>
  <q-slide-transition>
    <div>
      <q-list v-if="loading">
        <template v-for="index in 2" :key="index">
          <q-item v-ripple>
            <q-item-section avatar>
              <q-avatar>
                <q-skeleton type="QAvatar"/>
              </q-avatar>
            </q-item-section>

            <q-item-section>
              <q-item-label lines="1">
                <q-skeleton width="40%" type="text"/>
              </q-item-label>
              <q-item-label caption>
                <q-skeleton width="20%" type="text"/>
              </q-item-label>
            </q-item-section>

            <q-item-section side top>
                <q-avatar icon='navigate_next' class="tg-subtitle-text"/>
            </q-item-section>
          </q-item>
          <q-separator v-if="index < 2" inset="item" class="tg-separator"/>
        </template>
      </q-list>

      <q-list v-else-if="connects && connects.length">
        <template v-for="(connect, index) in connects" :key="index">
          <q-item
            :to="{ path: 'connect-info', query: connect }"
            v-ripple
            draggable="false"
          >
            <q-item-section avatar class="tg-list-item-icon">
              <q-avatar icon='vpn_lock' font-size="25px"/>
            </q-item-section>

            <q-item-section>
              <q-item-label lines="1">{{ connect.email }}</q-item-label>
              <q-item-label caption class="tg-subtitle-text">
                {{ connect.inboundName }}
              </q-item-label>
            </q-item-section>

            <q-item-section side>
              <template v-if="connect.active && !connect.remainingSeconds" >
                <q-badge outline color="amber-9" label='unlimit' />
              </template>
              <template v-else-if="!connect.active">
                <q-badge outline color="red" label='expired' />
              </template>
              <template v-else>
                <q-badge outline color="green" label='active' />
              </template>
            </q-item-section>

            <q-item-section side>
              <q-avatar icon='navigate_next' class="tg-subtitle-text"/>
            </q-item-section>
          </q-item>
          <q-separator v-if="index < connects?.length - 1" inset="item" class="tg-separator" />
        </template>
      </q-list>

      <not-found-banner v-else-if="connects" title="Похоже, у вас нет подписок!">
        <template #button>
          <q-btn class="tg-btn">Подключить</q-btn>
        </template>
      </not-found-banner>

      <not-found-banner v-else title="Ошибка получения подписок ;("/>
    </div>
  </q-slide-transition>
</template>

<style scoped>
.tg-list-item-icon {
  color: var(--tg-accent-text-color);
}
</style>
