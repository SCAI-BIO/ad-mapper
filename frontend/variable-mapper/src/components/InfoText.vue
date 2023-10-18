<template>
    <div class="bg-white">
      <!-- Header -->
      <div class="relative bg-gray-800 pb-32">
        <div class="absolute inset-0">
          <img class="h-full w-full object-cover" src="https://images.unsplash.com/photo-1496096265110-f83ad7f96608?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2940&q=80" alt="" />
          <div class="absolute inset-0 bg-gray-800 mix-blend-multiply" aria-hidden="true" />
        </div>
        <div class="relative mx-auto max-w-7xl py-24 px-4 sm:py-32 sm:px-6 lg:px-8">
          <h1 class="text-4xl font-bold tracking-tight text-white md:text-5xl lg:text-6xl">About</h1>
          <p class="mt-6 max-w-3xl text-xl text-gray-300">{{ aboutText }}</p>
        </div>
      </div>
  
      <!-- Overlapping cards -->
      <section class="relative z-10 mx-auto -mt-32 max-w-7xl px-4 pb-32 sm:px-6 lg:px-8" aria-labelledby="contact-heading">
        <div class="grid grid-cols-1 gap-y-20 lg:grid-cols-3 lg:gap-y-0 lg:gap-x-8">
          <div v-for="link in supportLinks" :key="link.name" class="flex flex-col rounded-2xl bg-white shadow-xl">
            <div class="relative flex-1 px-6 pt-16 pb-8 md:px-8">
         
              <h3 class="text-xl font-medium text-gray-900">{{ link.name }}</h3>
              <p class="mt-4 text-base text-gray-500">{{ link.description }}</p>
            </div>
            <div class="rounded-bl-2xl rounded-br-2xl bg-gray-50 p-6 md:px-8">
              <a :href="link.href" class="text-base font-medium text-indigo-700 hover:text-indigo-600">Learn more<span aria-hidden="true"> &rarr;</span></a>
            </div>
          </div>
        </div>
      </section>
    </div>
  </template>
  
  <script lang="ts">
  //import { LifebuoyIcon, NewspaperIcon, PhoneIcon } from '@heroicons/vue/24/outline'

  //import { DesktopComputerIcon } from "@vue-hero-icons/solid" ;
  
  const supportLinks = [
    {
      name: 'CDM',
      href: '#CDM',
      description:
        "The AD-Mapper's Common Data Model (CDM) is a comprehensive repository, featuring cross-mappings from 27 unique sources, which include 23 cohort studies and 3 external CDMs and an ontology. This comprehensive model spans multiple data modalities and offers precise variable mapping, connecting a total of 1300 variables seamlessly.",
      icon: null,
    },
    {
      name: 'Machine Learning',
      href: '#ML',
      description:
        "The backend of the service is equipped with multiple large language models, meticulously fine-tuned for mapping AD data variables. This integration markedly elevates the precision of variable mapping within the system.",
      icon: null,
    },
    {
      name: 'Custom APIs',
      href: `${process.env.VUE_APP_API}/docs`,
      description:
        "In addition to its user-friendly interface, this tool provides robust RESTful APIs, enabling third-party services to leverage the capabilities of the mapping assistant tool.",
      icon: null,
    },
  ]
  export default{

  data: () =>{
    return {
        supportLinks,
        aboutText: "The AD-Mapper developed by Fraunhofer SCAI empowers clinical data scientists with a robust AI-based software component, enabling the normalization of clinical data variables using a unified Central Common Data Model (CDM)."
    }
  }
}
  </script>