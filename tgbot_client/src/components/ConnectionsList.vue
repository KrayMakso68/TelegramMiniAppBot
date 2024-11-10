<script setup lang="ts">
import NotFoundBanner from "components/NotFoundBanner.vue";
import {onMounted, ref} from "vue";
import {Connect} from "src/api/types/subscribeTypes";
import {SubscriberService} from "src/api";

const loading  = ref<boolean>(true);
const connects = ref<Connect[] | null>(null);

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
        <template v-for="index in 3" :key="index">
          <q-item v-ripple>
            <q-item-section avatar>
              <q-avatar>
                <q-skeleton size="25px" type="QAvatar"  />
              </q-avatar>
            </q-item-section>
            <q-item-section>
              <q-skeleton width="40%" type="text" animation-speed="2500" />
            </q-item-section>
          </q-item>
          <q-separator v-if="index < 3" inset="item" class="tg-separator" />
        </template>
      </q-list>

      <q-list v-else-if="connects && connects.length">
        <template v-for="(item, index) in connects" :key="index">
          <q-item :to="'test-colors'" v-ripple draggable="false">
            <q-item-section avatar>
              <q-avatar icon='vpn_lock' class="tg-list-item-icon"/>
            </q-item-section>
            <q-item-section>
              {{ item.email }}
            </q-item-section>
          </q-item>
          <q-separator v-if="index < connects.length - 1" inset="item" class="tg-separator" />
        </template>
      </q-list>

      <not-found-banner v-else title="Похоже, у вас нет подписок!"/>
    </div>
  </q-slide-transition>
</template>

<style scoped>

</style>
