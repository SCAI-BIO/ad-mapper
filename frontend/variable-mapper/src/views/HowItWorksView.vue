<template>
  <div class="container lg mx-auto">
    <form id="mainForm" class="bg-grey mt-6" @submit="submitForm">
      <h3 class="text-3xl flex justify-center">Map a single variable</h3>
    <div class="grid grid-cols-3 gap-4 mt-6">
      <div class="justify-self-end" >
        <label for="var" class="block text-sm font-medium text-gray-700">Variable name</label>
    <div class="mt-1">
      <input type="text" name="var" id="var" v-model="variableName" class="block w-small rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" placeholder="Patient_age" />
    </div>
      </div>
      <div>
        <label for="var_description" class="block text-sm font-medium text-gray-700">Variable description</label>
    <div class="mt-1">
      <input type="text" name="var_description" id="var_description" v-model="variableDescription" class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm" placeholder="The patient's age in years." />
    </div>
    
      </div>
      <div class="mt-1 flex justify-start">
      
      <button type="submit" class="w-48 justify-self-end items-center rounded-md border border-transparent bg-indigo-100 px-4 py-2 text-base font-medium text-indigo-700 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">Map variable</button>
    </div>
    </div>
    </form>

    <div class="flex justify-center items-center m-6">
      <div id="loader" v-show="loading" class="mx-auto">
        <h5>Loading...</h5>
      </div>
      <div id="response" name="response" class="w-3/4 p-4 bg-white border border-gray-300 shadow-lg rounded-lg overflow-auto" v-show="respShow">
        <pre>
        {{responseContent}}
        </pre>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios';

export default {

  data: function () {
    return {
      variableName: '',
      loading: false,
      variableDescription: '',
      responseContent: 'Response',
      respShow: false,
      respShowCSV: false
      
    };
  },

  methods: {
    submitForm: function (e) {
      e.preventDefault();
      this.respShow = false;
      this.loading = true;
      var variableName = this.variableName;
      var variableDescription = this.variableDescription;
      var api_url = process.env.VUE_APP_API;
      //console.log(process.env)
      var url = `${api_url}/v2/ai-mapper?variable_name=${variableName}&variable_description=${variableDescription}&k=10&w_1=1&w_2=0`;

      axios.get(url).then((response) => {

          this.responseContent = response.data;
          this.respShow = true;
          this.loading = false;

        }).catch(err =>{
          this.loading = false;
          this.respShow = true;
          this.responseContent = err;
        });
       
    }
   
  }
}
 </script>
