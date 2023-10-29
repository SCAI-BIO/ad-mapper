<template>
  <div class="container mx-auto pt-6">
    <form class="space-y-6" @submit="submitForm">
      <div class="bg-white shadow px-4 py-5 sm:rounded-lg sm:p-6">
        <div class="md:grid md:grid-cols-3 md:gap-6">
          <div class="md:col-span-1">
            <h3 class="text-lg font-medium leading-6 text-gray-900">Upload your variables as .csv </h3>

            <div class="mb-4">
              <label for="variable_col" class="block text-sm font-medium text-gray-700 popover-elem">Variable column-name</label>
              <div class="absolute bg-gray-100 border border-gray-300 p-4 rounded shadow hidden">
                
              </div>
              <div class="mt-1">
                <input type="text" name="variable_col" id="variable_col" v-model="variableCol"
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                  placeholder="VARIABLES" />
              </div>
            </div>
            <div class="mb-4">
              <label for="description_col" class="block text-sm font-medium text-gray-700 popover-elem">Definition
                column-name</label>
                <div class="absolute bg-gray-100 border border-gray-300 p-4 rounded shadow hidden">
                
              </div>
              <div class="mt-1">
                <input type="text" name="description_col" id="description_col" v-model="descriptionCol"
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                  placeholder="DESCRIPTIONS" />
              </div>
            </div>
            <div class="mb-4">
              <label for="delimiter" class="block text-sm font-medium text-gray-700 popover-elem">Delimiter</label>
              <div class="absolute bg-gray-100 border border-gray-300 p-4 rounded shadow hidden">
                
              </div>
              <div class="mt-1">
                <select name="delimiter" id="delimiter" v-model="delimiter"
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
               >
                  <option value=";">;</option>
                  <option value=",">,</option>
                  <option value="\t">\t</option>
                </select>
              </div>
            </div>
          
            <div class="mb-4">
              <label for="k" class="block text-sm font-medium text-gray-700 popover-elem">K (Number of candidates)</label>
              <div class="absolute bg-gray-100 border border-gray-300 p-4 rounded shadow hidden">
                
              </div>
              <div class="mt-1">
                <input type="number" name="k" id="k" v-model="k"
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                   />
              </div>
            </div>
            <div class="mb-4">
              <label for="returnAll" class="block text-sm font-medium text-gray-700 popover-elem">Return all mappings</label>
              <div class="absolute bg-gray-100 border border-gray-300 p-4 rounded shadow hidden">
                
              </div>
              <div class="mt-1">
                <select name="returnAll" id="returnAll" v-model="returnAll"
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
               >
                  <option value="true">True</option>
                  <option value="false">False</option>
                </select>
              </div>
            </div>
            <div class="mb-4">
              <label for="w1" class="block text-sm font-medium text-gray-700 popover-elem">W1 (AI-based model)</label>
              <div class="absolute bg-gray-100 border border-gray-300 p-4 rounded shadow hidden">
                
              </div>
              <div class="mt-1">
                <input type="float" name="w1" id="w1" v-model="w1"
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                  />
              </div>
            </div>
            <div class="mb-4">
              <label for="w2" class="block text-sm font-medium text-gray-700 popover-elem">W2 (String matching)</label>
              <div class="absolute bg-gray-100 border border-gray-300 p-4 rounded shadow hidden">
                
              </div>
              <div class="mt-1">
                <input type="float" name="w2" id="w2" v-model="w2"
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                  />
              </div>
            </div>
            

          </div>
          <div class="mt-5 space-y-6 md:mt-0 md:col-span-2" @drop="dropCSVFile">
            <div>
              <!--<label class="block text-sm font-medium text-gray-700">.csv file</label>-->
              <div class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
                <div class="space-y-1 text-center">
                  <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48"
                    aria-hidden="true">
                    <path
                      d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                      stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                  <div class="flex text-sm text-gray-600">
                    <label for="fileUpload"
                      class="relative cursor-pointer bg-white rounded-md font-medium text-indigo-600 hover:text-indigo-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-indigo-500">
                      <span>Upload a file</span>
                      <input id="fileUpload" @change="uploadChange"  name="fileUpload" type="file" class="sr-only" />
                    </label>
                    <p class="pl-1">or drag and drop</p>
                  </div>
                  <!--<p class="text-xs text-gray-500">CSV up to 10MB</p>-->
                  <!--<p class="text-xs text-gray-500">Separator: ;</p>-->
                  <p class="text-s text-black-500">{{ fileName }}</p>
                </div>
              </div>
              <div class="flex justify-end mt-12">
      <button type="submit" class="ml-auto bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded">Submit
      </button>
      </div>
            </div>
          </div>
        </div>
      </div>
     
    </form>
    <div class="flex justify-center items-center m-6">
      <div id="loader" v-show="loading" class="mx-auto">
        <h5>Loading...</h5>
      </div>
      <div id="response" name="response" class="w-3/4 p-4 bg-white border border-gray-300 shadow-lg rounded-lg overflow-auto" v-show="respShow">
        
        
        <pre v-if="error">
          {{ status_code }}
   
          {{ responseContent }}
        </pre>
        <div v-else>
        <a class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" :href="download">Download mapped .csv</a>
        <pre>
          {{ responseContent }}
        </pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import axios from 'axios';




export default {

  data: function(){
    return {
      variableCol: "",
      descriptionCol: "",
      delimiter: ";",
      responseContent: "",
      loading: false,
      respShow: false,
      download: "", 
      fileName: "", 
      w1: 1.0,
      w2: 0.0,
      k: 10,
      error: false, 
      returnAll: false, 
      status_code: 200
    };
  },

  mounted: function(){
      const popover_helpers = [
    {
      name: "Variable column-name",
      description: "The name of the column in your .csv file that contains the variable names."
    },
    {
      name: "Definition column-name",
      description: "The name of the column in your .csv file that contains the variable definitions."
    },
    {
      name: "Delimiter",
      description: "The delimiter used in your .csv file."
    },
    {
      name: "K (Number of candidates)",
      description: "The number of candidates generated by the AI-based model. More candidates may yield a more accurate prdiction, but also increases compute time."
    },
    {
      name: "Return all mappings",
      description: "If set to true, all known mappings onto to predicted target variable will be returned. If set to false, only the target will be returned."
    },
    {
      name: "W1 (AI-based model)",
      description: "The weight of the AI-based model. Final class probability will be determined by W1 * AI-based model + W2 * string matching."
    },
    {
      name: "W2 (String matching)",
      description: "The weight of the string matching algorithm. Final class rpoability will be determined by W1 * AI-based model + W2 * string matching."
    }
  ];
    const popover_elems = document.querySelectorAll('.popover-elem');
    //var i=0;
    popover_elems.forEach( (elem, i) => {
      elem.addEventListener('mouseover', () => {
        elem.nextElementSibling.classList.remove('hidden');
        elem.nextElementSibling.innerHTML = popover_helpers[i].description;
      });
      elem.addEventListener('mouseout', () => {
        elem.nextElementSibling.classList.add('hidden');
      });
    });
  },

  methods: {
    submitForm: function(e){
      this.error =false;
      this.loading = true;
      this.respShow = false;
      this.responseContent = "";
      e.preventDefault();
      var file = document.getElementById("fileUpload");
      if (file.files.length === 0) {
      alert('Please select a file.');
      return;
  }
  const formData = new FormData();
  formData.append('csvFile', file.files[0]);
  formData.append('variableColumnName', this.variableCol);
  formData.append('definitionColumnName', this.descriptionCol);

  axios.post(`${process.env.VUE_APP_API}/v2/csv-mapper?variableColumnName=${this.variableCol}&definitionColumnName=${this.descriptionCol}&k=${this.k}&w_1=${this.w1}&w_2=${this.w2}&return_all_mappings=${this.returnAll}&delimiter=${this.delimiter}`, formData, {
  }).then((response) => {
    this.responseContent = response.data;
    this.download = response.data.file;
    this.loading = false;
    this.respShow = true;
      console.log(response);
    }).catch((error) => {
      console.log(error);
      this.error = true;
      this.respShow = true;
      this.responseContent = error.response.data;
      this.loading = false;
      this.status_code = error.response.status;
    })
  }, 

  uploadChange: function(e){
    var file = e.target.files[0];
    console.log(file);
    this.fileName = file.name;
  }, 
  dropCSVFile: function(e){
    e.preventDefault();
    var file = e.dataTransfer.files[0];
    console.log(file);
    this.fileName = file.name;
    document.getElementById("fileUpload").files = e.dataTransfer.files;
  }
}
}
</script>
