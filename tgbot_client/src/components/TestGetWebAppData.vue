<script setup lang="ts">
import { ref } from "vue";
import { useWebApp } from "vue-tg";
import { getUser } from "../api/userService"
import { login } from "../api/authService"
import { User } from "src/api/types/userTypes";


const {initData} = useWebApp();

const data = ref(initData);
const user = ref<User | null>(null);
const logindata = ref()
const error = ref();

const loadUser = async () => {
  try {
    user.value = await getUser();
  } catch (e) {
    error.value = (e as Error)
  }
};
const logIn = async () => {
  try {
    const response = await login();
    logindata.value = {response}
  } catch (e) {
    error.value = (e as Error)
  }
}

</script>

<template>
  <div>
    <q-card class="my-card text-black">
      <q-card-section>
        стринг:
        {{ data }}
      </q-card-section>
      <q-card-section>
        логин:
        {{ logindata }}
      </q-card-section>
      <q-card-section>
        юзер:
        {{ user }}
      </q-card-section>
      <q-card-section>
        ошибка:
        {{ error }}
      </q-card-section>
      <q-card-actions>
        <q-btn flat @click="logIn">Login</q-btn>
        <q-btn flat @click="loadUser">Получить пользователя</q-btn>
      </q-card-actions>
    </q-card>
  </div>
</template>

<style scoped>
.my-card {
  width: 100%;
  max-width: 250px
}
</style>
