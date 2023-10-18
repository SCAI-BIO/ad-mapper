<template>
  <div>
    <div class="grid-cols-1">
      <div class="flex justify-center mb-12 mt-12 flex-col ">
        <p class="text-3xl mx-auto my-3 font-sans">{{ mainText1 }}</p> 
        
        <p class="text-3xl mx-auto my-3 font-sans">{{ mainText2 }}</p>
      </div> 
      <div class ="mb-24">
        <InfoText />
      </div>
      <div class="flex justify-center mb-24">
      <ModelStats />
      </div>
      <div class="flex justify-center mb-24">

      </div>
      <div>
        <MainFooter />
      </div>
  </div>
    </div>
    
</template>

<script lang="ts">
import ModelStats from '../components/ModelStats.vue';
import InfoText from '../components/InfoText.vue';
import MainFooter from '../components/MainFooter.vue';


export default{
  components: { ModelStats, InfoText, MainFooter }, 
  data() {
    return {
      mainText1: "Elevate Your Alzheimer's Dementia Research with AD-Mapper",
      mainText2: "Where Speed Meets Semantic Harmonization"
    }
  },
}
</script>


