<template>
  <v-app>
    <v-app-bar app color="white">
      <div class="d-flex align-center">
        <v-img alt="Recigen Logo" class="shrink mr-2" contain min-width="100" src="./assets/icons/logo_hd.png"
          transition="scale-transition" width="100" />
      </div>

      <v-spacer></v-spacer>


      <span class="mr-2 custom-font font-weight-black">Hi, Foodie!</span>
    </v-app-bar>

    <v-main>
      <ApiMain />
    </v-main>
  </v-app>
</template>

<script>
import ApiMain from './components/ApiMain';

export default {
  name: 'App',

  components: {
    ApiMain,
  },

  data: () => {
    return {
      sharedData: '',
    };
  },
};
</script>
