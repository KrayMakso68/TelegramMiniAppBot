<script setup lang="ts">
import {BackButton} from "vue-tg";
import {useRouter} from "vue-router";
import {Connect} from "src/api/types/subscribeTypes";
import {ConnectInfo} from "src/api/types/panelTypes";
import TgSection from "components/TgSection.vue";
import TgCodeCard from "components/TgCodeCard.vue";
import {Ref, ref} from "vue";
import {PanelService} from "src/api";

const router = useRouter();
const props = defineProps<Connect>();

const connectInfo: Ref<ConnectInfo | null> = ref<ConnectInfo | null>(null)

const loadInfo = async () => {
  if (!connectInfo.value) {
    connectInfo.value = await PanelService.getConnectInfoByEmail(props.email)
  }
};
</script>

<template>
  <BackButton @click="() => router.back()"></BackButton>
  <q-page class="tg-text overflow-auto">
    <div class="q-gutter-y-md">
      <tg-section>
        <div class="q-pa-md">
          <div class="text-subtitle2" style="color: var(--tg-subtitle-text-color);">
            Подключение
          </div>
          <div class="text-h4 text-weight-bold" style="color: var(--tg-section-header-text-color);">
            {{email}}
          </div>
        </div>
        <div class="q-pa-sm">
          <tg-code-card title="Connection url" :text=connectUrl />
        </div>
      </tg-section>

      <tg-section>
        <q-expansion-item
          icon="query_stats"
          header-class="q-pl-lg"
          label="Подробная информация"
          @show="loadInfo"
        >
          <q-card style="background-color: var(--tg-section-bg-color);">
            <q-card-section>
              <div class="column">

                <div class="col row items-center">
                  <div class="col-3">Name:</div>
                  <div class="col-auto">
                     <q-chip dense color="teal" text-color="white">
                      {{connectInfo?.email}}
                    </q-chip>
                  </div>
                </div>
                <div class="col row">
                  <div class="col-3">Active:</div>
                  <div class="col-auto">{{connectInfo?.enable}}</div>
                </div>
                <div class="col row">
                  <div class="col-3">Expiry time:</div>
                  <div class="col-auto">{{connectInfo?.expiryTime}}</div>
                </div>
                <div class="col row items-center">
                  <div class="col-3">
                    Download:
                  </div>
                  <div class="col-3">
                    <q-circular-progress
                      indeterminate
                      rounded
                      size="50px"
                      color="blue"
                      class=""
                    />

                  </div>
                  <div class="col-3">
                    Upload:
                  </div>
                  <div class="col-3">
                    <q-circular-progress
                      show-value
                      value="30"
                      rounded
                      size="50px"
                      color="blue"
                      class=""
                    >
                      {{30}} GB
                    </q-circular-progress>
                  </div>
                </div>
              </div>
              <div class="col row">

              </div>
              <div class="col row">

              </div>
            </q-card-section>
          </q-card>
        </q-expansion-item>
      </tg-section>
    </div>
  </q-page>
</template>

<style scoped>

</style>
