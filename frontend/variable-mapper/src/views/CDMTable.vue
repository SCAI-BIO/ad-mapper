<template>
<div class="px-12 py-12">
    <div class="mt-5 sm:mt-6 mb-6">
        <a type="button"
          class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
         :href="download">
          Download CDM
      </a>
      </div>

    <div class="max-h-screen overflow-y-scroll">
        <EasyDataTable
    :headers="headers"
    :items="items"
    border-cell
    alternating
    :fixed-header="true"
    :table-height="height"

    
  />
    </div>
    </div>
</template>

<script>
import axios from 'axios';
//import type { Header, Item } from "vue3-easy-data-table";
export default {
    data: function(){
        return {
            headers: [],
            items: [], 
            height: 500,
            download: `${process.env.VUE_APP_API}/download-cdm`,
        }
    },
    mounted: function(){
        // set height acording to screen 
        this.height = window.innerHeight - 200;
        this.getData();
    },
    methods: {
        getData: function(){
            var headers = this.headers;
            var items = this.items;
            
            var api_url = process.env.VUE_APP_API;
            //console.log(process.env)
            var url = `${api_url}/get-cdm-as-json`
            axios.get(url)
            .then(function(response){
                var tabledata = response.data;
                var keys = Object.keys(tabledata[0]);
                keys.forEach((key) =>{
                    var header;
                    if (key == "Feature"){
                        header = {
                            text: key, 
                            value: key,
                            fixed: true,
                            width: 150,
                        }
                    }
                    else{
                    header = {
                        text: key,
                        value: key, 
                        
                    }
                }
                    headers.push(header);
                });
                tabledata.forEach((row) =>{
                    var item= {};
                    keys.forEach((key) =>{
                        item[key] = row[key];
                    });
                    items.push(item);
                
            });
            })
            .catch(function(error){
                console.log(error);
            });
        }
    }
}
</script>

<style>

</style>