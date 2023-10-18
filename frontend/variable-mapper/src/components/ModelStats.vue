<template>
    <div class="w-3/5" >
      
      <dl class="mt-5 grid grid-cols-1 gap-5 sm:grid-cols-3">
        <div v-for="item in stats" :key="item.name" class="overflow-hidden rounded-lg bg-white px-4 py-5 shadow sm:p-6">
          <dt class="truncate text-sm font-medium text-gray-500">{{ item.name }}</dt>
          <dd class="mt-1 text-3xl font-semibold tracking-tight text-gray-900">{{ item.stat }}</dd>
        </div>
      </dl>
      
      <br>
      <h3 class="text-xl font-medium leading-6 text-gray-900" id="ML">Model performance</h3>
      <dl class="mt-5 grid grid-cols-1 gap-5 sm:grid-cols-3">
        <div v-for="item in performance" :key="item.name" class="overflow-hidden rounded-lg bg-white px-4 py-5 shadow sm:p-6">
          <dt class="truncate text-sm font-medium text-gray-500">{{ item.name }}</dt>
          <dd class="mt-1 text-3xl font-semibold tracking-tight text-gray-900">{{ item.stat }}</dd>
        </div>
      </dl>
    </div>
  </template>
  
  <script lang="ts">
  export default{
    data : () =>{

    return {
        stats : [
  
  
    { name: 'Total No. Variables', stat: '1300' },
    { name: 'Total No. Variable Mappings', stat: '11034' },
    { name: 'Total No. Data Sources', stat: '27' },
  ], 
  performance : [
    {
      name: "Accuracy on test set", stat: "77.2%"
    }
  ], 

  
  }
}
}
  </script>