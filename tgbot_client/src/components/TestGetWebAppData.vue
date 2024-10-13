<script setup lang="ts">
import {ref} from "vue";
import {useWebApp} from "vue-tg"

const data = ref()
const {initData} = useWebApp()

interface WebAppUser {
    id: number;
    is_bot?: boolean; // Опциональное поле
    first_name: string;
    last_name?: string; // Опциональное поле
    username?: string; // Опциональное поле
    language_code?: string; // Опциональное поле
    is_premium?: boolean; // Опциональное поле
    added_to_attachment_menu?: boolean; // Опциональное поле
    allows_write_to_pm?: boolean; // Опциональное поле
    photo_url?: string; // Опциональное поле
}

interface WebAppChat {
    id: number;
    type: string;
    title: string;
    username?: string; // Опциональное поле
    photo_url?: string; // Опциональное поле
}

interface WebAppInitData {
    query_id?: string; // Опциональное поле
    user?: WebAppUser; // Опциональное поле
    receiver?: WebAppUser; // Опциональное поле
    chat?: WebAppChat; // Опциональное поле
    chat_type?: string; // Опциональное поле
    chat_instance?: string; // Опциональное поле
    start_param?: string; // Опциональное поле
    can_send_after?: number; // Исправлено с can_sand_after на can_send_after
    auth_date: number;
    hash: string;
}

function parseInitData(initData: string): WebAppInitData {
    const params = new URLSearchParams(initData);

    const user = params.has('user') ? JSON.parse(params.get('user')!) : undefined;

    return {
        query_id: params.get('query_id') || undefined,
        user: user,
        receiver: user, // Если receiver аналогичен user, иначе измените логику
        chat: params.has('chat') ? JSON.parse(params.get('chat')!) : undefined,
        chat_type: params.get('chat_type') || undefined,
        chat_instance: params.get('chat_instance') || undefined,
        start_param: params.get('start_param') || undefined,
        can_send_after: params.has('can_send_after') ? parseInt(params.get('can_send_after')!) : undefined,
        auth_date: parseInt(params.get('auth_date')!),
        hash: params.get('hash')!
    };
}
// data.value = parseInitData(initData);
data.value = initData

</script>

<template>
  <div class="full-width">
    <q-card class="my-card text-black">
      <q-card-section>
        {{ data }}
      </q-card-section>
    </q-card>
  </div>
</template>

<style scoped>

</style>
