<!-- This example requires Tailwind CSS v2.0+ -->
<template>
  <div class="bg-white">
    <div class="mx-auto py-12 px-4 max-w-7xl sm:px-6 lg:px-8 lg:py-24">
      <div class="grid grid-cols-1 gap-12 lg:grid-cols-3 lg:gap-8">
        <div class="space-y-5 sm:space-y-4">
          <h2 class="text-3xl font-bold tracking-tight sm:text-4xl sm:tracking-tight">Meet our team</h2>
          <p class="text-xl text-gray-500">This project is developed and maintained by Fraunhofer SCAI-BIO</p>
        </div>
        <div class="lg:col-span-2">
          <ul role="list" class="space-y-12 sm:grid sm:grid-cols-2 sm:gap-12 sm:space-y-0 lg:gap-x-8">
            <li v-for="person in people" :key="person.name">
              <div class="flex items-center space-x-4 lg:space-x-6">
                <img class="w-16 h-16 rounded-full lg:w-20 lg:h-20" :src="person.imageUrl" alt="" />
                <div class="font-medium text-lg leading-6 space-y-1">
                  <h3>{{ person.name }}</h3>
                  <p class="text-indigo-600">{{ person.role }}</p>
                  <p class="text-indigo-600">{{ person.email }}</p>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">

export default {

    mounted() {
        console.log(process.env);
    },
    data: () => {
        return {
            people: [
                {
                    name: 'Yasamin Salimi',
                    role: 'PhD Student Fraunhofer SCAI - Bio / Project Leader',
                    imageUrl: process.env.BASE_URL + "Yasamin.jpg"
                        ,
                    email: "yasamin.salimi@scai.fraunhofer.de"
                },
                {
                    name: "Philipp Wegner", 
                    role: "PhD Student DZNE",
                    
                    imageUrl: "https://data-steward.bio.scai.fraunhofer.de/data-steward/img/picture-philipp.3bc2e27e.jpg", 
                    email: "philipp.wegner@dzne.de"

                },
                {
                    name: "Helena Balabin", 
                    role: "PhD Student KU Leuven",
                    
                    imageUrl: process.env.BASE_URL + "helena.jpg", 
                    email: "helena.balabin@kuleuven.be"

                },
                {
                    name: "Prof. Dr. Martin Hofmann-Apitius",
                    role: "Head of Department Fraunhofer SCAI - Bio",
                    
                    imageUrl: process.env.BASE_URL + "martin.jpg",
                    email: "martin.hofmann-apitius@scai.fraunhofer.de"

                }
            ]
        }
    }
}

</script>