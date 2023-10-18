import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './index.css'
import axios from 'axios';

import Vue3EasyDataTable from 'vue3-easy-data-table';
import 'vue3-easy-data-table/dist/style.css';

/*
import Session from 'supertokens-web-js/recipe/session';

Session.addAxiosInterceptors(axios);

import SuperTokens from 'supertokens-web-js';

SuperTokens.init({
    appInfo: {
        apiDomain: "http://localhost:8000",
        apiBasePath: "/auth",
        appName: "...",
    },
    recipeList: [
        Session.init(),
    ]
});

*/
const app = createApp(App);//;
app.use(router).mount('#app')
app.component('EasyDataTable', Vue3EasyDataTable);

