<template>
  
    <NavigationHeader/>
   

  <router-view />
</template>

<style>

</style>
<script lang="ts">
import NavigationHeader from './components/NavigationHeader.vue'
export default{
  components: {NavigationHeader}
}
</script>

