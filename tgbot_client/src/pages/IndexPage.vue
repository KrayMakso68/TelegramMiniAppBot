<template>
  <q-page class="row items-center justify-evenly text-white">
    <example-component
      title="Example component"
      active
      :todos="todos"
      :meta="meta"
    ></example-component>
    <TestGetWebAppData></TestGetWebAppData>
<!--    <BiometricManager @init="handleInit" />-->
    <MainButton text="Открой меня" @click="() => showAlert('Hello!')" />
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Todo, Meta } from 'components/models';
import ExampleComponent from 'components/ExampleComponent.vue';
import TestGetWebAppData from "components/TestGetWebAppData.vue";

import {MainButton, useWebAppPopup, BiometricManager, useWebAppBiometricManager} from 'vue-tg'

const { showAlert } = useWebAppPopup()

defineOptions({
  name: 'IndexPage'
});

// const handleInit = () => {
//     const { requestBiometricAccess,  } = useWebAppBiometricManager()
//     requestBiometricAccess({reason: 'The bot uses biometrics for testing purposes.'})
// }

const todos = ref<Todo[]>([
  {
    id: 1,
    content: 'ct1'
  },
  {
    id: 2,
    content: 'ct2'
  },
  {
    id: 3,
    content: 'ct3'
  },
  {
    id: 4,
    content: 'ct4'
  },
  {
    id: 5,
    content: 'ct5'
  }
]);

const meta = ref<Meta>({
  totalCount: 1200
});
</script>
